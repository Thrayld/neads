import unittest
import inspect

from neads.activation_model.plugin import Plugin, PluginID, PluginException


class TestPlugin(unittest.TestCase):
    def setUp(self) -> None:
        def f(x, y):  # noqa
            return x + y

        self.f_x_y = f
        self.pl_id = PluginID('my_plugin', 0)
        self.plugin = Plugin(self.pl_id, self.f_x_y)

    def test_init_not_plugin_id(self):
        self.assertRaises(
            TypeError,
            Plugin,
            'not a plugin id type',
            self.f_x_y
        )

    def test_init_method_not_callable(self):
        self.assertRaises(
            TypeError,
            Plugin,
            self.pl_id,
            'self.f_x_y'
        )

    def test_signature(self):
        actual = self.plugin.signature

        expected = inspect.signature(self.f_x_y)
        self.assertEqual(expected, actual)

    def test_id(self):
        actual = self.plugin.id

        expected = self.pl_id
        self.assertEqual(expected, actual)

    def test_call(self):
        actual = self.plugin(10, 20)

        expected = 30
        self.assertEqual(expected, actual)

    def test_call_bad_arguments_for_signature(self):
        self.assertRaises(
            TypeError,
            self.plugin,
            10, 20, 30
        )

    def test_call_plugin_raises_exception(self):
        self.assertRaises(
            PluginException,
            self.plugin,
            10, 'string'
        )




if __name__ == '__main__':
    unittest.main()
