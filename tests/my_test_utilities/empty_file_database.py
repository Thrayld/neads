import pathlib
import shutil
import weakref

from neads.database import FileDatabase


DB_DIR = pathlib.Path(__file__).parent / 'file_database'
_finalizer = None


def get():
    _do_delete()

    FileDatabase.create(DB_DIR)
    db = FileDatabase(DB_DIR)

    global _finalizer
    _finalizer = weakref.finalize(db, _do_delete)
    return db


def delete():
    _finalizer()  # noqa


def _do_delete():
    if DB_DIR.is_dir():
        shutil.rmtree(DB_DIR)
