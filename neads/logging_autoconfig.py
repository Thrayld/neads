import logging
import sys


def configure_logging(level=logging.WARN):
    """Provide basic configuration of logging module used by neads.

    The method assures that all the eligible log messages (whose severity is
    at least the given level) are send to standard output in some format
    (in subjectively better format then the default).

    Note that only first call of the method has any effect.

    Please use your own logging configuration, if this is not suitable for you.

    Parameters
    ----------
    level
        The least level at which the messages are logged.
    """

    logging.basicConfig(
        level=level,
        format='%(asctime)-s %(name)-26s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M',
        stream=sys.stdout
    )
