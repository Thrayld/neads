import abc


class DataNotFound(Exception):
    pass


class IDatabase(abc.ABC):
    # TODO: should be implement enter, exit pattern? .. yes

    # TODO: also add finalizer (via weakref)

    @abc.abstractmethod
    def __enter__(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def __exit__(self):
        raise NotImplementedError()

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
