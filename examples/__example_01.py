import logging

import neads as nd
from examples import example_01

DATA_PATH = 'C:\\Users\\Honst\\BP\\evaluations\\my_df'
DATABASE_PATH = 'C:\\Users\\Honst\\BP\\evaluations\\my_example_01'

nd.configure_logging(logging.DEBUG)

nd.FileDatabase.create(DATABASE_PATH)
db = nd.FileDatabase(DATABASE_PATH)

scm = example_01.get_example(DATA_PATH)
manager = nd.SingleThreadEvaluationManager(db)
results = manager.evaluate(scm.create_graph())

result_tree = list(results.values())[0]