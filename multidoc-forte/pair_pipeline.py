import argparse
import itertools
from pathlib import Path

from forte.pipeline import Pipeline
from forte.processors.writers import PackNameMultiPackWriter

from processors.evidence_questions import QuestionCreator
from readers.event_reader import TwoDocumentPackReader
from utils import set_logging


def read_doc_pairs(inp_path: Path):
    doc_pairs = []
    with open(inp_path, "r") as rf:
        for line in rf:
            group_docs = line.strip().split()
            for doc1, doc2 in itertools.combinations(group_docs, 2):
                doc_pairs.append((f"{doc1}.json", f"{doc2}.json"))

    return doc_pairs


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="generate MultiPack using pre-defined document pairs")
    parser.add_argument("--packs-dir", type=Path, help="input directory path (packs)")
    parser.add_argument("--multipacks-dir", type=Path, help="output directory path (multipacks)")
    parser.add_argument(
        "--doc-groups", type=Path, help="relative path to info about document clusters",
    )
    parser.add_argument("--overwrite", action="store_true", help="overwrite existing multipacks")

    args = parser.parse_args()

    set_logging()

    # read the document grouping
    pairs = read_doc_pairs(args.doc_groups)
    print(f"# document pairs: {len(pairs)}")

    pair_pipeline = Pipeline()
    pair_pipeline.set_reader(TwoDocumentPackReader())

    # Create event relation suggestions
    # pair_pipeline.add(SameLemmaSuggestionProvider())

    # Create coreference questions
    pair_pipeline.add(QuestionCreator())

    # Write out the events.
    args.multipacks_dir.mkdir(exist_ok=True)

    pair_pipeline.add(
        PackNameMultiPackWriter(),
        {
            "output_dir": str(args.multipacks_dir),
            "indent": 2,
            "overwrite": args.overwrite,
            "drop_record": True,
        },
    )

    pair_pipeline.initialize()
    pair_pipeline.run(str(args.packs_dir), pairs)
