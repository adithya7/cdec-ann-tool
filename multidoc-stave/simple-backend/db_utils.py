import sqlite3
import json
from nlpviewer_backend.utils import gen_hash
import uuid
import logging


def add_pack(name, textPack, ontology, packID, overwrite=False):
    """
	textPack must be a string of json
	ontology must be a string of json
	"""
    con = sqlite3.connect("db.sqlite3")
    sqlite3.register_adapter(uuid.UUID, lambda u: u.hex)
    cursor = con.cursor()
    textPack = json.dumps(textPack)
    ontology = json.dumps(ontology)

    # check if the document is already in the db
    # result = cursor.execute(
    #     "SELECT * FROM nlpviewer_backend_document WHERE packID=:id", {"id": uuid.UUID(int=packID)},
    # )
    result = cursor.execute(
        "SELECT * FROM nlpviewer_backend_document WHERE name=:packName", {"packName": name},
    )
    if result.fetchone() is not None:
        if overwrite:
            logging.warning("overwriting pack %s in the db" % name)
        else:
            logging.warning("pack %s already present in db, skipping" % name)
            con.close()
            return

    cursor.execute(
        "INSERT OR REPLACE INTO nlpviewer_backend_document(textPack, ontology, packID, name) \
	            VALUES(?,?,?,?)",
        (textPack, ontology, uuid.UUID(int=packID), name),
    )
    con.commit()
    con.close()


def add_multipack(name, textPack, ontology, packID, overwrite=False):
    """
	textPack must be a string of json
	ontology must be a string of json
	"""
    con = sqlite3.connect("db.sqlite3")
    sqlite3.register_adapter(uuid.UUID, lambda u: u.hex)
    cursor = con.cursor()
    textPack = json.dumps(textPack)
    ontology = json.dumps(ontology)
    idHash = gen_hash(name)

    logging.info("visit <HOST_URL>:<PORT>/?tasks=%s to annotate the document" % idHash)

    # result = cursor.execute(
    #     "SELECT * FROM nlpviewer_backend_crossdoc WHERE packID=:id", {"id": uuid.UUID(int=packID)},
    # )
    result = cursor.execute(
        "SELECT * FROM nlpviewer_backend_crossdoc WHERE name=:packName", {"packName": name},
    )
    if result.fetchone() is not None:
        if overwrite:
            logging.warning("overwriting multipack %s in the db" % name)
            cursor.execute("DELETE FROM nlpviewer_backend_crossdoc WHERE idHash=:value", {"value": idHash})
        else:
            logging.warning("multipack %s already present in db, skipping" % name)
            con.close()
            return

    cursor.execute(
        "INSERT OR REPLACE INTO nlpviewer_backend_crossdoc(textPack, ontology, packID, name, idHash) \
            VALUES(?,?,?,?,?)",
        (textPack, ontology, uuid.UUID(int=packID), name, idHash),
    )
    con.commit()
    con.close()
    return idHash
