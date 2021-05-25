class DataNotFound(Exception):
    pass


class Database:
    # TODO: should be implement enter, exit pattern?

    def open(self):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

    def save(self, data, data_definition):
        raise NotImplementedError()

    def load(self, data_definition):
        raise NotImplementedError()
