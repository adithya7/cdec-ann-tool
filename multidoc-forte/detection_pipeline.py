import argparse
from pathlib import Path
import yaml

from forte.pipeline import Pipeline
from forte.processors.writers import PackNameJsonPackWriter
from forte.processors import CoNLLNERPredictor
from forte.common.configuration import Config

from processors.openie_processor import AllenNLPEventProcessor
from processors.stanfordnlp_processor import StandfordNLPProcessor
from readers.event_reader import DocumentReaderJson

from utils import set_logging

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="run detection pipeline")
    parser.add_argument(
        "--json-dir", type=Path, help="input json directory path",
    )
    parser.add_argument("--packs-dir", type=Path, help="output path to write packs")

    args = parser.parse_args()

    ner_config_model = yaml.safe_load(
        open(Path(__file__).parent.resolve() / "configs/ner_config_model.yml", "r")
    )

    set_logging()

    detection_pipeline = Pipeline()

    # Read JSON documents
    # Specifically looks for three fields, `text`, `title` and `date`.
    detection_pipeline.set_reader(DocumentReaderJson())

    # Call stanfordnlp.
    detection_pipeline.add(StandfordNLPProcessor())

    # add NER detection
    ner_config = Config({}, default_hparams=None)
    ner_config.add_hparam("config_model", ner_config_model)
    detection_pipeline.add(CoNLLNERPredictor(), config=ner_config)

    # Call the event detector.
    detection_pipeline.add(AllenNLPEventProcessor())

    # Write out the processed documents as `packs`.
    args.packs_dir.mkdir(exist_ok=True)

    detection_pipeline.add(
        PackNameJsonPackWriter(),
        {"output_dir": str(args.packs_dir), "indent": 2, "overwrite": True, "drop_record": True,},
    )

    detection_pipeline.initialize()

    detection_pipeline.run(str(args.json_dir))
