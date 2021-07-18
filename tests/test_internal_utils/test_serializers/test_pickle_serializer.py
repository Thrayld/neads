from tests.test_internal_utils.test_serializers.test_serializer \
    import BaseTestClassWrapper
from neads._internal_utils.serializers.pickle_serializer import PickleSerializer


class TestPickleSerializer(BaseTestClassWrapper.BaseTestSerializer):
    """Tests serializer based on the pickle protocol."""

    def get_serializer(self):
        return PickleSerializer()
