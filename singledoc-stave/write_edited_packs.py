"""
Load sqlite3 database from stave single-document interface (post correction).
This module updates packs to use expert corrected events.
"""

import argparse
import logging
from pathlib import Path
import shutil
import sqlite3


def get_pack_names(dir_path: Path):
    pack_names = []
    for pack_path in dir_path.iterdir():
        pack_names += [pack_path.stem]
    return pack_names


def get_corrected_pack(pack_name: str, stave_db_path: str, project_name: str) -> str:
    conn = sqlite3.connect(stave_db_path)
    cursor = conn.cursor()

    # select pack_name from project_name
    result = cursor.execute(
        "SELECT * FROM nlpviewer_backend_project WHERE name=:project_name", {"project_name": project_name},
    ).fetchone()
    project_id = result[0]
    for value in cursor.execute(
        "SELECT textPack from nlpviewer_backend_document WHERE project_id=:id and name=:pack_name",
        {"id": project_id, "pack_name": pack_name + ".json"},
    ):
        return value[0]


if __name__ == "__main__":

    logging.basicConfig(
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
        handlers=[logging.StreamHandler()],
    )

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "stave_db", type=Path, help="path to read single document sqlite3 database from stave"
    )
    parser.add_argument("inp_packs", type=Path, help="path to automatically generated packs")
    parser.add_argument("out_packs", type=Path, help="path to write corrected packs")
    parser.add_argument("--project-name", type=str, help="target project name in sqlite3 database")
    parser.add_argument("--overwrite", action="store_true", help="overwrite existing output packs")
    parser.add_argument(
        "--copy",
        action="store_true",
        help="to copy the automatically generated packs, if the pack is not in the sqlite db",
    )

    args = parser.parse_args()

    logging.info(f"loading automatically generated packs from {args.inp_packs}")
    pack_names = get_pack_names(args.inp_packs)

    logging.info(f"writing corrected packs to {args.out_packs}")
    args.out_packs.mkdir(exist_ok=True, parents=True)

    for pack_name in pack_names:
        corrected_pack = get_corrected_pack(pack_name, args.stave_db, args.project_name)

        if corrected_pack is None:
            logging.warning(f"document {pack_name} not in the database!")
            if args.copy:
                logging.info(f"copying the automatically generated pack {pack_name}")
                shutil.copy(args.inp_packs / f"{pack_name}.json", args.out_packs)
            continue

        out_path = args.out_packs / f"{pack_name}.json"
        if out_path.is_file() and not args.overwrite:
            logging.warning(
                f"pack {pack_name}  already exists in the output folder {args.out_packs}, skipping! use --overwrite option to force rewrite"
            )
            continue
        elif args.overwrite:
            logging.warning(f"overwriting pack {pack_name}!!")

        logging.info(f"writing {pack_name}.json...")
        with open(out_path, "w") as wf:
            wf.write(corrected_pack)
