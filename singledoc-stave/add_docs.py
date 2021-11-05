import argparse
import logging
import sqlite3
from pathlib import Path


def add_pack(
    name: str, textPack: str, ontology: str, db_path: Path, project_name: str = None, overwrite: bool = False,
):
    """
    add new pack into single doc stave
    """
    con = sqlite3.connect(db_path)
    cursor = con.cursor()

    # searching for document in the db
    result = cursor.execute(
        "SELECT * FROM nlpviewer_backend_document WHERE name=:pack_name", {"pack_name": name},
    ).fetchone()
    if result is not None:
        if overwrite:
            print("warning! overwriting pack %s in the db, you will lose the previous work" % name)
            cursor.execute(
                "DELETE FROM nlpviewer_backend_document WHERE name=:pack_name", {"pack_name": name},
            )
        else:
            print("pack %s already exists in the db, skipping" % name)
            pack_id = result[0]
            return pack_id

    if project_name is None:
        print("adding pack %s" % name)
        cursor.execute(
            "INSERT or REPLACE INTO nlpviewer_backend_document(name, textPack) VALUES(?,?)", (name, textPack),
        )
    else:
        # getting project id
        result = cursor.execute(
            "SELECT * FROM nlpviewer_backend_project WHERE name=:project_name",
            {"project_name": project_name},
        ).fetchone()
        if result is not None:
            # project exists
            project_id, *_ = result
        else:
            # create new project
            print("creating project %s" % project_name)
            cursor.execute(
                "INSERT INTO nlpviewer_backend_project(ontology, name, project_type) VALUES(?,?,?)",
                (ontology, project_name, "single_pack"),
            )
            project_id, *_ = cursor.execute(
                "SELECT * FROM nlpviewer_backend_project WHERE name=:project_name",
                {"project_name": project_name},
            ).fetchone()

        print("adding pack %s to project %s" % (name, project_name))
        cursor.execute(
            "INSERT or REPLACE INTO nlpviewer_backend_document(name, textPack, project_id) VALUES(?,?,?)",
            (name, textPack, project_id),
        )

    result = cursor.execute(
        "SELECT * FROM nlpviewer_backend_document WHERE name=:pack_name", {"pack_name": name},
    ).fetchone()
    pack_id = result[0]

    con.commit()
    con.close()

    return pack_id


if __name__ == "__main__":

    logging.basicConfig(
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
        handlers=[logging.StreamHandler()],
    )

    parser = argparse.ArgumentParser(description="add new documents to stave single doc db")
    parser.add_argument("stave_db_path", type=Path, help="path to stave db")
    parser.add_argument("packs", type=Path, help="path to directory with packs")
    parser.add_argument("ontology", type=Path, help="path to ontology json")
    parser.add_argument("--url", type=str, default=None, help="URL prefix for stave")
    parser.add_argument("--project", type=str, default=None, help="project name")
    parser.add_argument("--overwrite", action="store_true", help="overwrite existing files in the db")

    args = parser.parse_args()

    with open(args.ontology, "r") as rf:
        ontology = rf.read()

    for pack_path in args.packs.iterdir():
        with open(pack_path, "r") as rf:
            pack = rf.read()

        pack_id = add_pack(
            pack_path.name,
            pack,
            ontology,
            args.stave_db_path,
            project_name=args.project,
            overwrite=args.overwrite,
        )

        if args.url is not None:
            logging.info(f"the document is now available at: {args.url}/{pack_id}")
