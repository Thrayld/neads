"""For pairs of plugins used as separator and extractor in SCM's DynamicStep.

Usually, there is one extractor and various ways to make the separator, as the
extraction is often the same, but the proper separation is the interesting
part.

Thus, each use case have itself directory with (again) usually one extractor
and many separators.
"""

from neads.plugin_database.dynamic_pairs.evolution import *
