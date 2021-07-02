import pathlib
import shutil

from neads.database import FileDatabase


DB_DIR = pathlib.Path(__file__) / 'file_database'


def get():
    FileDatabase.create(DB_DIR)
    return FileDatabase(DB_DIR)


def delete():
    shutil.rmtree(DB_DIR)
