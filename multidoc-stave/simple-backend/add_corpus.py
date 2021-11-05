"""
Load new packs and multipacks to the database
"""

from argparse import ArgumentParser
from pathlib import Path
import json
import logging

from db_utils import add_pack, add_multipack

if __name__ == "__main__":

    logging.basicConfig(
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
        handlers=[logging.StreamHandler()],
    )

    parser = ArgumentParser(description="add new packs/multipacks")
    parser.add_argument("dir", type=Path, help="directory with /multi and /packs")
    parser.add_argument("--pack-onto", default="initial_data/pack_ontology.json")
    parser.add_argument("--multi-onto", default="initial_data/multi_ontology.json")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="overwrites existing packs. This will erase any existing annotations on these multipacks.",
    )

    args = parser.parse_args()

    with open(args.pack_onto, "r") as rf:
        pack_onto = json.load(rf)

    pack_dir = args.dir / "packs"
    for pack in pack_dir.iterdir():
        with open(pack, "r") as rf:
            textPack = json.load(rf)
        packID = textPack["py/state"]["_meta"]["py/state"]["_pack_id"]
        packName = textPack["py/state"]["_meta"]["py/state"]["pack_name"]
        logging.info("adding datapack: %s" % packName)
        add_pack(packName, textPack, pack_onto, packID, overwrite=args.overwrite)

    with open(args.multi_onto, "r") as rf:
        multi_onto = json.load(rf)

    multipack_dir = args.dir / "multi"
    for multi in multipack_dir.iterdir():
        with open(multi, "r") as rf:
            textPack = json.load(rf)
        packID = textPack["py/state"]["_meta"]["py/state"]["_pack_id"]
        packName = textPack["py/state"]["_meta"]["py/state"]["pack_name"]
        logging.info("adding multipack: %s" % packName)
        add_multipack(packName, textPack, multi_onto, packID, overwrite=args.overwrite)
