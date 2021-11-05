# Edit Mentions

The default pipeline uses automatically tagged event mentions. However, to ensure the final dataset is of good quality, we recommend adding a expert validation phase to correct any incorrect or missing event mentions.

For this purpose, you can make use of the single-document version of stave annotation tool.

## Setup Stave

Note: This is different from the multidoc-stave used for cross-document annotation.

```bash
bash run_setup_singledoc_stave.sh
```

Run backend server,

```bash
cd stave/simple-backend
conda activate singledoc-stave
./start-dev.sh
```

Run frontend server (from `singledoc-stave/stave` directory.),

```bash
conda activate singledoc-stave
yarn && yarn start
```

Visit http://localhost:3000 to access the interface. The default username/password are admin/admin. Once logged in, you will be able to create new project and add documents. See [adding new documents](#upload_documents_to_edit) below for instructions to programmatically upload documents.

Note that, by default, the backend server runs on port 8000. To run on a different port (say 8888), make the following two changes,

1. Edit `start-dev.sh` to specify the new port.

```bash
# python manage.py runserver
python manage.py runserver 0.0.0.0:8888
```

2. Edit frontend configuration with the above updated info. Make the following change in `src/setupProxy.js`,

```python
# target: 'http://127.0.0.1:8000',
target: 'http://127.0.0.1:8888',
```

3. If you face an issue with ALLOWED_HOSTS, edit the field in `simple_backend/nlpviewer_backend/settings.py`

## Upload Documents to Edit

```bash
conda activate singledoc-stave
python add_docs.py \
    stave/simple-backend/db.sqlite3 \
    ../sample_data/packs \
    ../multidoc-forte/full.json \
    --project mention_editing
```

To better organize the documents on stave, you can specify a project name using `--project` argument. You can then visit http://localhost:3000/projects and select the project ("mention_editing" in above example) to browse through all the documents added under that project.

## Edit

Once a pack (aka document) is loaded onto the stave interface, an expert can view the existing event mentions and decide to add/remove mentions.

* To see the existing annotations, check the _second_ `EventMention` box on the left. The first EventMention corresponds to the default `forte.onto.base_ontology.EventMention`, whereas the second EventMention corresponds to our custom `edu.cmu.EventMention`.

* Now, you should be able to view the automatically tagged mentions. You can perform the following actions,

    - _Remove mention_: Click on the mention and choose "remove" from the right window.
    - _Add mention_: Click "Add annotation" on the top bar, and then highlight the text span corresponding to the new mention. On the right window, choose "Legend Type" as `edu.cmu.EventMention` and select "confirm".

Browse through all the documents to make any necessary edits to the event mentions.

## Collect Updated Documents

The newly edited packs (aka documents) can be loaded from the sqlite3 db and written into JSON format. This allows for recreating multipacks for cross-document annotation.

```bash
conda activate singledoc-stave
# collect edited packs
python write_edited_packs.py \
    stave/simple-backend/db.sqlite3 \
    ../sample_data/packs \
    ../sample_data/edited_packs \
    --project-name mention_editing
```

Regenerate multipacks using the new packs.

```bash
cd ..
conda activate multidoc-forte
python multidoc-forte/pair_pipeline.py \
    --packs-dir sample_data/edited_packs \
    --multipacks-dir sample_data/multipacks \
    --doc-groups sample_data/doc_groups.txt \
    --overwrite
```

Upload the new multipacks to the Multidoc Stave interface. **Note**: this removes any previous cross-document annotations involving these edited documents.

```bash
cd multidoc-stave/simple-backend
conda activate multidoc-stave
python add_corpus.py \
    ../../sample_data/multipacks/ \
    --overwrite
```
