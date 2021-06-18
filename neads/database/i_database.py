import abc


class DataNotFound(Exception):
    pass


class IDatabase(abc.ABC):
    # TODO: also add finalizer (via weakref)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()

    @abc.abstractmethod
    def open(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def close(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def save(self, data, data_definition):
        raise NotImplementedError()

    @abc.abstractmethod
    def load(self, data_definition):
        raise NotImplementedError()
