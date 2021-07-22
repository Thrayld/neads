import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / 'README.rst').read_text()


def parse_requirements_file(filename):
    with open(filename, encoding="utf-8") as fid:
        requires = [l.strip() for l in fid.readlines() if l]

    return requires


install_requires = parse_requirements_file('requirements.txt')

data = ['requirements.txt', 'README.rst']

setup(
    name='neads',
    version='1.0.2',
    description='Neads is a modular tool for modelling of dynamical systems '
                'with complex internal structure by complex networks.',
    long_description=README,
    long_description_content_type='text/x-rst',
    url='https://github.com/Thrayld/neads',
    author='Tomáš Hons',
    author_email='Hons.T.m@seznam.cz',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Information Analysis'
    ],
    packages=[
        'neads',
        'neads._internal_utils',
        'neads._internal_utils.serializers',
        'neads.activation_model',
        'neads.activation_model.symbolic_objects',
        'neads.activation_model.symbolic_objects.concrete_composite_objects',
        'neads.database',
        'neads.evaluation_manager',
        'neads.evaluation_manager.single_thread_evaluation_manager',
        'neads.evaluation_manager.single_thread_evaluation_manager.evaluation_algorithms',
        'neads.plugins',
        'neads.plugins.analyzers',
        'neads.plugins.builders',
        'neads.plugins.dynamic_pairs',
        'neads.plugins.dynamic_pairs.evolution',
        'neads.plugins.editors',
        'neads.plugins.filters',
        'neads.plugins.loaders',
        'neads.plugins.preprocessors',
        'neads.plugins.surrogates_related',
        'neads.sequential_choices_model',
        'neads.sequential_choices_model.choices_step',
        'neads.sequential_choices_model.dynamic_step',
        'neads.sequential_choices_model.scm_plugins',
        'neads.tutorials',
        'neads.utils',
    ],
    install_requires=install_requires,
    data_files=data,
)
