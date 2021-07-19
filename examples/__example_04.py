import shutil

import matplotlib.pyplot as plt

import neads as nd
from examples import example_04


DATA_PATH = 'C:\\Users\\Honst\\BP\\evaluations\\my_df'
DATABASE_PATH = 'C:\\Users\\Honst\\BP\\evaluations\\my_example_04'

shutil.rmtree(DATABASE_PATH)

nd.FileDatabase.create(DATABASE_PATH)
db = nd.FileDatabase(DATABASE_PATH)

manager = nd.SingleThreadEvaluationManager(db)


def run(grid):
    scm = example_04.get_example(DATA_PATH, grid)
    results = manager.evaluate(scm.create_graph())
    result_tree = list(results.values())[0]

    values = result_tree.query(([0]*2) + [None] + ([0]*3), data=True)

    _, axs = plt.subplots()
    axs.plot(values)

    axs.set_title(grid.capitalize() + ' grid')
    axs.set_xlabel('Intervals')
    axs.set_ylabel('Average clustering coefficient')
    plt.show()


run('coarse')
run('medium')
run('fine')

