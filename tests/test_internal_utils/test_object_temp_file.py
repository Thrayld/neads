import gc
import unittest
import os


from neads._internal_utils.object_temp_file import ObjectTempFile


class TestObjectTempFileWithGivenName(unittest.TestCase):
    def setUp(self) -> None:
        self.path = __file__ + '_tmp_file'
        self.file = ObjectTempFile(path=self.path)
        self.object = [1, '10', {}]

    def tearDown(self) -> None:
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_save_load(self):
        self.file.save(self.object)

        actual = self.file.load()

        self.assertEqual(self.object, actual)

    def test_repeated_load(self):
        self.file.save(self.object)

        actual_1 = self.file.load()
        actual_2 = self.file.load()
        actual_3 = self.file.load()

        self.assertEqual(self.object, actual_1)
        self.assertEqual(self.object, actual_2)
        self.assertEqual(self.object, actual_3)

    def test_dispose(self):
        self.file.dispose()

        self.assertFalse(os.path.exists(self.path))

    def test_save_after_dispose(self):
        self.file.dispose()

        self.assertRaises(
            RuntimeError,
            self.file.save,
            self.object
        )

    def test_load_after_dispose(self):
        self.file.dispose()

        self.assertRaises(
            RuntimeError,
            self.file.load
        )

    def test_double_dispose(self):
        self.file.dispose()
        self.file.dispose()

        self.assertFalse(os.path.exists(self.path))

    def test_load_before_save(self):
        self.assertRaises(
            RuntimeError,
            self.file.load
        )

    def test_implicit_dispose(self):
        self.file = None
        gc.collect()

        self.assertFalse(os.path.exists(self.path))

    def test_is_disposed_negative(self):
        self.file.save(self.object)

        self.assertFalse(self.file.is_disposed)

    def test_is_disposed_positive(self):
        self.file.save(self.object)
        self.file.dispose()

        self.assertTrue(self.file.is_disposed)


class TestObjectTempFileOther(unittest.TestCase):
    def test_creation_with_given_generator(self):
        gen = lambda: __file__ + '_generated_tmp_file'
        ObjectTempFile.PATH_GENERATOR = gen

        # Expects to just not die immediately
        file = ObjectTempFile()
        file = None

        self.assertFalse(os.path.exists(gen()))

    def test_creation_with_implicit_generator(self):
        # Expects to just not die immediately
        file = ObjectTempFile()

        # Access private member is not a nice thing to do, but necessary in
        # this little case
        file_path = file._path  # noqa

        file = None

        self.assertFalse(os.path.exists(file_path))


if __name__ == '__main__':
    unittest.main()
