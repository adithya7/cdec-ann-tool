"""
Process the SQLite database written by multidoc-stave interface and write annotations in JSON format.
"""

import argparse
from collections import defaultdict
import json
import logging
import numpy as np
from pathlib import Path
import re
from typing import Dict, Tuple

from forte.pipeline import Pipeline
from forte.data.data_pack import DataPack
from forte.data.multi_pack import MultiPack
from forte.processors.base import MultiPackProcessor
from ft.onto.base_ontology import Token, Sentence
from forte.data.readers.stave_readers import StaveMultiDocSqlReader

from edu.cmu import EventMention, CrossEventRelation


class CorefEventCollector(MultiPackProcessor):

    COREF_QUESTIONS = [
        [
            "Place: Do you think the two events happen at the same place?",
            ["Exactly the same", "The places overlap", "Not at all", "Cannot determine",],
        ],
        [
            "Time: Do you think the two events happen at the same time?",
            ["Exactly the same", "They overlap in time", "Not at all", "Cannot determine",],
        ],
        [
            "Participants: Do you think the two events have the same participants?",
            ["Exactly the same", "They share some participants", "Not at all", "Cannot determine",],
        ],
        [
            "Inclusion: Do you think one of the events is part of the other?",
            [
                "Yes, the left event is part of right one",
                "Yes, the right event is part of left one",
                "No, they are exactly the same",
                "Cannot determine",
            ],
        ],
    ]

    def __init__(self, out_path: Path = None):
        super().__init__()
        self.documents: Dict[int, DataPack] = {}
        self.events: Dict[Tuple[int, int], EventMention] = {}
        self.event_sents = {}
        self.mention_pairs = []
        self.docpair2links = defaultdict(list)
        self.out_anns_path = out_path / "anns"
        self.out_docs_path = out_path / "docs"
        self.mention_pair_set = set()

    def _load_doc(self, input_pack: MultiPack, pack_id):
        """
        load the specified document and its events from a MultiPack
        """

        doc: DataPack = input_pack.get_pack_at(input_pack.get_pack_index(str(pack_id)))
        pack_name = doc.pack_name

        if pack_name not in self.documents:
            self.documents[pack_name] = doc
            for mention in doc.get(EventMention):
                self.events[(pack_name, mention.span.begin, mention.span.end)] = mention
                for sent in doc.get(Sentence):
                    if (sent.span.begin <= mention.span.begin) and (sent.span.end >= mention.span.end):
                        self.event_sents[(pack_name, mention.span.begin, mention.span.end)] = sent

        return doc

    def _process(self, input_pack: MultiPack):
        """
        Iterate through the annotator and their cross-document relations from the database
        """
        for stave_annotator in input_pack.get_all_creator():
            annotator = re.search(r"^stave\.(.*)$", stave_annotator).group(1)

            for relation in input_pack.get(CrossEventRelation, stave_annotator):
                if relation.rel_type != "coref":
                    continue

                parent_pack = self._load_doc(input_pack, relation.parent_pack_id())
                child_pack = self._load_doc(input_pack, relation.child_pack_id())
                parent_mention = relation.get_parent()
                child_mention = relation.get_child()

                if parent_pack is None or child_pack is None:
                    continue

                mention_pair = (
                    annotator,
                    (parent_pack.pack_name, parent_mention.span.begin, parent_mention.span.end),
                    (child_pack.pack_name, child_mention.span.begin, child_mention.span.end),
                )
                if mention_pair not in self.mention_pair_set:
                    self.mention_pair_set.add(mention_pair)
                    self.mention_pairs.append(
                        (
                            annotator,
                            (parent_pack.pack_name, parent_mention.span.begin, parent_mention.span.end),
                            (child_pack.pack_name, child_mention.span.begin, child_mention.span.end),
                            relation.coref_answers,
                        )
                    )
                    self.docpair2links[(parent_pack.pack_name, child_pack.pack_name)].append(
                        (
                            annotator,
                            (parent_pack.pack_name, parent_mention.span.begin, parent_mention.span.end),
                            (child_pack.pack_name, child_mention.span.begin, child_mention.span.end),
                            relation.coref_answers,
                        )
                    )

    def _load_links(self):

        docpair2anns = defaultdict(set)
        for link in self.mention_pairs:
            docpair2anns[(link[1][0], link[2][0])].add(link[0])

        # NOTE: above computation skips annotators who provided zero coreference links for a given document pair.
        # This is due to database missing any entries for that annotator on the document pair.
        # Therefore, there should be a separate mechanism to keep track of annotators for each document pair.
        # One option is to use the unique codes generated upon the finish of each document pair.
        # This code is displayed to the annotator after the task on the annotation interface.
        # Use this unique code to keep track of annotators.
        # See the main README.md for more details

        n_anns2doc_pairs = defaultdict(list)
        n_anns2count = defaultdict(int)
        for docpair, anns in docpair2anns.items():
            n_anns2doc_pairs[len(anns)].append(docpair)
            n_anns2count[len(anns)] += 1

        logging.info("--------------------------------------------------")
        logging.info("distribution of # annotators per document pair")
        logging.info(n_anns2count)
        logging.info("--------------------------------------------------")

        mp2idx = defaultdict(lambda: len(mp2idx))
        idx2mp = {}
        ann2idx = defaultdict(lambda: len(ann2idx))
        idx2ann = {}
        mp2txt = {}
        for (doc1, doc2), anns in docpair2anns.items():
            doc1_pack: DataPack = self.documents[doc1]
            doc2_pack: DataPack = self.documents[doc2]
            for m1 in doc1_pack.get(EventMention):
                for m2 in doc2_pack.get(EventMention):
                    mp = (
                        (doc1, m1.span.begin, m1.span.end),
                        (doc2, m2.span.begin, m2.span.end),
                    )
                    idx2mp[mp2idx[mp]] = mp
                    mp2txt[mp2idx[mp]] = (m1.text, m2.text)

            for ann in anns:
                idx2ann[ann2idx[ann]] = ann

        # 0: not-annotated
        ann_table = np.zeros((len(idx2mp), len(idx2ann)))
        Q_DEFAULT = -2
        ann_table_qs = [
            np.full((len(idx2mp), len(idx2ann)), Q_DEFAULT),
            np.full((len(idx2mp), len(idx2ann)), Q_DEFAULT),
            np.full((len(idx2mp), len(idx2ann)), Q_DEFAULT),
            np.full((len(idx2mp), len(idx2ann)), Q_DEFAULT),
        ]
        for (doc1, doc2), anns in docpair2anns.items():
            doc1_pack: DataPack = self.documents[doc1]
            doc2_pack: DataPack = self.documents[doc2]
            for ann in anns:
                for m1 in doc1_pack.get(EventMention):
                    for m2 in doc2_pack.get(EventMention):
                        mp = (
                            (doc1, m1.span.begin, m1.span.end),
                            (doc2, m2.span.begin, m2.span.end),
                        )
                        # default is non-coreference
                        ann_table[mp2idx[mp]][ann2idx[ann]] = -1

        for ann, m1, m2, answers in self.mention_pairs:
            # coreference
            ann_table[mp2idx[(m1, m2)]][ann2idx[ann]] = 1
            for idx, ans in enumerate(answers):
                ann_table_qs[idx][mp2idx[(m1, m2)]][ann2idx[ann]] = ans

        return idx2mp, mp2idx, idx2ann, ann2idx, mp2txt, ann_table, ann_table_qs

    def _get_ann_sent(self, sent: Sentence, mention: EventMention) -> str:
        """
        return the surrounding sentence with the given event mention highlighted in special tags, <E> and </E>
        """
        begin = mention.span.begin - sent.span.begin
        end = mention.span.end - sent.span.begin
        sent_str = sent.text[:begin] + "<E> " + sent.text[begin:end] + " </E>" + sent.text[end:]
        return sent_str

    def write_anns(
        self, mp_indices, idx2mp, idx2ann, ann2idx, mp2txt, ann_table, ann_table_qs,
    ):
        """
        Write the annotations to a readable JSON file
        Params:
            - file_path: output JSON path
            - mp_indices: a list of mention-pair indices
            - idx2mp: mapping from mention-pair index to mention-pair
            - idx2ann: mapping from annotator index to annotator name
            - ann2idx: inverse mapping of idx2ann
            - mp2txt: text spans for the mention-pair
            - ann_table: a two-dimensional array with mention-pairs indexed as rows, annotators indexed as columns
            - ann_table_qs: a three-dimensional array indexed as (follow-up question, mention_pair, annotator)
        """
        out_data = []
        for mp_idx in mp_indices:
            mp = idx2mp[mp_idx]
            mp_anns = np.nonzero(ann_table[mp_idx])[0]
            mp_anns = [idx2ann[ann_idx] for ann_idx in mp_anns]
            sent1 = self._get_ann_sent(self.event_sents[mp[0]], self.events[mp[0]])
            sent2 = self._get_ann_sent(self.event_sents[mp[1]], self.events[mp[1]])
            coref_anns = [idx2ann[x] for x in np.nonzero(ann_table[mp_idx] == 1)[0]]
            # MCQ responses by coref annotators
            coref_anns_dict = defaultdict(list)
            for ann in coref_anns:
                for q_idx in range(4):
                    coref_anns_dict[ann] += [int(ann_table_qs[q_idx][mp_idx][ann2idx[ann]])]

            null_coref_anns = [idx2ann[x] for x in np.nonzero(ann_table[mp_idx] == -1)[0]]
            if len(coref_anns) > 0:
                # at least one coreference annotation
                out_data.append(
                    {
                        "doc_pair": "pair_%s_and_%s" % (mp[0][0], mp[1][0]),
                        "anns": mp_anns,
                        "mention_spans": mp,
                        "mention_txt": mp2txt[mp_idx],
                        "sentences": (sent1, sent2),
                        "coref_annotators": coref_anns,
                        "null_coref_annotators": null_coref_anns,
                        "coref_question_responses": coref_anns_dict,
                    }
                )

        self.out_anns_path.mkdir(exist_ok=True)
        with open(self.out_anns_path / "coref_pairs.json", "w") as wf:
            json.dump(out_data, wf, indent=2)

    def write_docs(self):
        """
        Write each text document in a JSON format.
        Each output file contains,
            - entire text of the document
            - sentences (with their text, begin offset and end offset)
            - mentions (with their text, begin offset, end offset and tagged parent sentence)
        """
        if self.out_docs_path is None:
            return

        self.out_docs_path.mkdir(exist_ok=True)
        for pack_name, doc_pack in self.documents.items():
            doc_data = {}
            doc_data["text"] = doc_pack.text
            doc_data["sentences"] = []
            doc_data["mentions"] = []
            for sent in doc_pack.get(Sentence):
                doc_data["sentences"] += [{"text": sent.text, "begin": sent.span.begin, "end": sent.span.end}]
            for mention in doc_pack.get(EventMention):
                doc_data["mentions"] += [
                    {
                        "text": mention.text,
                        "begin": mention.span.begin,
                        "end": mention.span.end,
                        "sentence": self._get_ann_sent(
                            self.event_sents[(pack_name, mention.span.begin, mention.span.end)],
                            self.events[(pack_name, mention.span.begin, mention.span.end)],
                        ),
                    }
                ]

            with open(self.out_docs_path / f"{pack_name}.json", "w") as wf:
                json.dump(doc_data, wf, indent=2)

    def finish(self, _):
        logging.info("--------------------------------------------------")
        logging.info(f"# documents: {len(self.documents)}")
        logging.info(f"# mentions: {len(self.events)}")

        """ document level statistics """
        sents = []
        tokens = []
        for _, doc_pack in self.documents.items():
            sents += [len([x for x in doc_pack.get(Sentence)])]
            tokens += [len([x for x in doc_pack.get(Token)])]
        logging.info(f"avg. sentences per document: {np.mean(sents):.2f} ({np.std(sents):.3f})")
        logging.info(f"avg. tokens per document: {np.mean(tokens):.2f} ({np.std(tokens):.3f})")
        logging.info("--------------------------------------------------")

        idx2mp, mp2idx, idx2ann, ann2idx, mp2txt, ann_table, ann_table_qs = self._load_links()

        self.write_anns(
            idx2mp.keys(), idx2mp, idx2ann, ann2idx, mp2txt, ann_table, ann_table_qs,
        )
        self.write_docs()


if __name__ == "__main__":

    logging.basicConfig(
        format="%(message)s", level=logging.INFO, handlers=[logging.StreamHandler()],
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("--stave-db", type=str, required=True, help="path to stave sqlite3 db")
    parser.add_argument(
        "--out-dir",
        type=Path,
        required=True,
        help="path to output directory. Writes two subfolders, /anns and /docs",
    )
    args = parser.parse_args()

    if args.out_dir:
        args.out_dir.mkdir(exist_ok=True)

    pipeline = Pipeline()
    pipeline.set_reader(StaveMultiDocSqlReader(), config={"stave_db_path": args.stave_db})
    pipeline.add(CorefEventCollector(args.out_dir))

    pipeline.run()
