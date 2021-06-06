from tests.test_utilities.test_serializer import BaseTestClassWrapper
from neads.utilities.serializers.pickle_serializer import PickleSerializer


class TestPickleSerializer(BaseTestClassWrapper.BaseTestSerializer):
    """Tests serializer based on the pickle protocol."""

    def get_serializer(self):
        return PickleSerializer()
