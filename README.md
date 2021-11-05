# Annotation Toolkit for Cross-document Tasks

This toolkit was used to collect the [CDEC-WN dataset](https://github.com/adithya7/cdec-wikinews). For text processing pipeline, we build upon the [Forte](https://github.com/asyml/forte) toolkit. We also adapt the [Stave](https://github.com/asyml/stave) toolkit by adding the ability to annotate pairs of text documents.

## Setup

Requires `npm` (tested with version 6.14.4) before running the setup.

```bash
# setup multidoc-forte
bash run_setup_forte.sh
# setup multidoc-stave
bash run_setup_stave.sh
```

## Usage

The cross-document annotation interface (under [multidoc-stave](multidoc-stave)) expects data in MultiPack format. The text processing pipeline (under [multidoc-forte](multidoc-forte)) processes raw text documents to generate packs (`DataPack`) and multipacks (`MultiPack`). See [forte documentation](https://asyml-forte.readthedocs.io/en/latest/code/data.html#) for details on pack and multipack formats.

### Text Processing Pipeline

Convert raw text into `DataPack` format. This step involves tokenization, lemmatization, POS tagging, dependency parsing, NER and OpenIE. Refer to the [forte documentation](https://asyml-forte.readthedocs.io/en/latest/code/data.html#forte.data.data_pack.DataPack) to understand the `DataPack` format. The goal of this pipeline to identify event mentions from the text documents.

```bash
conda activate multidoc-forte
# loads JSON files from sample_data/json and writes processed packs to sample_data/packs
python multidoc-forte/detection_pipeline.py \
    --json-dir sample_data/json \
    --packs-dir sample_data/packs

# load packs and document group info to write multipacks to sample_data/multipacks
python multidoc-forte/pair_pipeline.py \
    --packs-dir sample_data/packs \
    --multipacks-dir sample_data/multipacks \
    --doc-groups sample_data/doc_groups.txt
```

### Annotate Document Pairs

Load packs and multipacks onto the multidoc interface and run the annotation server.

```bash
conda activate multidoc-stave
cd multidoc-stave/simple-backend

python manage.py migrate
# keep it running
python manage.py runserver 0.0.0.0:8004

# use --overwrite option to rewrite previously added packs/multipacks (sample_data/packs, sample_data/multipacks)
conda activate multidoc-stave
python add_corpus.py ../../sample_data/multipacks
```

To see a sample task, visit http://localhost:8004/?tasks=ceab189e1e1c78c25e2900afbd925c114df34fb3c82983916f5236ea3b9db204. Accept the template consent form, read the instructions and type in your id (or any identifiable string) in the "Turk ID" box.

We hash the name of each document pair (`pair_36185_and_36231` in above sample task) to generate a unique task ID. See [Multi-doc Stave](multidoc-stave/README.md) for more features of the annotation interface.

### Collect Data

After annotating document pairs on the interface, you can use script `multidoc-forte/process_db.py` to post-process the sqlite3 database. This sample script writes the annotations in a more readable JSON format. See the output folders `stave_data/docs` and `stave_data/anns` for the text documents and the annotated mention pairs respectively.

```bash
conda activate multidoc-forte
# run in root directory
python multidoc-forte/process_db.py \
    --stave-db multidoc-stave/simple-backend/db.sqlite3 \
    --out-dir stave_data
```

## Editing Event Mentions

Above pipeline uses an OpenIE tool to detect event mentions from text documents. This output might contain errors, including missed mentions. To edit these automatically tagged documents, see [singledoc-stave](singledoc-stave/README.md).

## Citation

If you find this toolkit helpful in your research, consider citing our work.

```bib
@inproceedings{pratapa-etal-2021-cross,
    title = "Cross-document Event Identity via Dense Annotation",
    author = "Pratapa, Adithya  and
      Liu, Zhengzhong  and
      Hasegawa, Kimihiro  and
      Li, Linwei  and
      Yamakawa, Yukari  and
      Zhang, Shikun  and
      Mitamura, Teruko",
    booktitle = "Proceedings of the 25th Conference on Computational Natural Language Learning",
    month = nov,
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.conll-1.39",
    pages = "496--517",
}
```

We also recommend citing the original [stave](https://github.com/asyml/stave) and [forte](https://github.com/asyml/forte) toolkits that formed the basis for this project.

## License

This toolkit is based on stave and forte toolkits, and is also available under Apache License 2.0.

## Issues

For any questions, issues or requests, please create a GitHub Issue.
