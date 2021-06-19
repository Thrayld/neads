from tests.test_utils.test_serializers.test_serializer \
    import BaseTestClassWrapper
from neads.utils.serializers.pickle_serializer import PickleSerializer


class TestPickleSerializer(BaseTestClassWrapper.BaseTestSerializer):
    """Tests serializer based on the pickle protocol."""

    def get_serializer(self):
        return PickleSerializer()
