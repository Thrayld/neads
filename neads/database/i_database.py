class DataNotFound(Exception):
    pass


class IDatabase:
    # TODO: should be implement enter, exit pattern? .. yes

    # TODO: also add finalizer (via weakref)

    def __enter__(self):
        raise NotImplementedError()

    def __exit__(self):
        raise NotImplementedError()

    def open(self):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

    def save(self, data, data_definition):
        raise NotImplementedError()

    def load(self, data_definition):
        raise NotImplementedError()
