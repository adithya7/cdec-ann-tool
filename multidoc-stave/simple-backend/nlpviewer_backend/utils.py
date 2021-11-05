import hashlib
from pathlib import PurePath

# return a mapping from external id to file names
def read_index_file(index_file):
    extid_to_name = {}
    with open(index_file) as f:
        for line in f:
            pairs = line.strip().split()
            external_id = int(pairs[0])
            file_name = PurePath(pairs[1]).stem
            extid_to_name[external_id] = file_name
    return extid_to_name


def gen_secret_code(tasks_session):
    """
	input is crossdochash1-crossdochash2-crossdochash3
	"""
    string = tasks_session + "-cdecanntool"
    return hashlib.sha256(str.encode(string)).hexdigest()


def gen_hash(name):
    name = str(name)
    return hashlib.sha256(str.encode(name)).hexdigest()

