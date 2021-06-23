import unittest

import unittest.mock as mock

from neads.activation_model import SealedActivationGraph
from neads.evaluation_manager.single_thread_evaluation_manager\
    .eligibility_detector import EligibilityDetector, \
    ActivationEligibilityDetector

import tests.my_test_utilities.arithmetic_plugins as ar_plugins


class TestActivationEligibilityDetector(unittest.TestCase):
    # Sadly, the graph cannot be partially created in setUp method, as the
    # EligibilityDetectors require already created graph, which is modified
    # only via trigger methods

    def test_is_eligible_without_trigger_on_descendants(self):
        ag = SealedActivationGraph()
        act = ag.add_activation(ar_plugins.const, 10)
        aed = ActivationEligibilityDetector(act)

        actual = aed.is_eligible

        expected = None
        self.assertEqual(expected, actual)

    def test_is_eligible_simple_true(self):
        ag = SealedActivationGraph()
        act = ag.add_activation(ar_plugins.const, 10)
        act.trigger_on_descendants = mock.Mock()

        act_2 = ag.add_activation(ar_plugins.add, act.symbol, 15)  # noqa
        # This activation should not cause a problem, as it does not have a
        # trigger

        aed = ActivationEligibilityDetector(act)

        actual = aed.is_eligible

        expected = True
        self.assertEqual(expected, actual)

    def test_is_eligible_simple_false(self):
        ag = SealedActivationGraph()
        act = ag.add_activation(ar_plugins.const, 10)
        act.trigger_on_descendants = mock.Mock()

        act_2 = ag.add_activation(ar_plugins.add, act.symbol, 15)  # This
        # activation causes the ineligibility
        act_2.trigger_on_result = mock.Mock()

        aed = ActivationEligibilityDetector(act)

        actual = aed.is_eligible

        expected = False
        self.assertEqual(expected, actual)

    def test_activation_property(self):
        ag = SealedActivationGraph()
        act = ag.add_activation(ar_plugins.const, 10)
        aed = ActivationEligibilityDetector(act)

        actual = aed.activation

        expected = act
        self.assertEqual(expected, actual)

    def test_update_with_not_related_activation(self):
        ag = SealedActivationGraph()
        act = ag.add_activation(ar_plugins.const, 10)
        act.trigger_on_descendants = mock.Mock()

        act_2 = ag.add_activation(ar_plugins.add, act.symbol, 15)  # This
        # activation causes the ineligibility
        act_2.trigger_on_result = mock.Mock()

        act_3 = ag.add_activation(ar_plugins.const, 25)
        act_3.trigger_on_result = lambda res: None

        aed = ActivationEligibilityDetector(act)
        assert not aed.is_eligible

        # 'Invoking' act_3's trigger with completely no effect
        del act_3.trigger_on_result

        # Update
        aed.update(act_3, [])

        # Check
        actual = aed.is_eligible

        expected = False
        self.assertEqual(expected, actual)

    def test_update_make_eligible(self):
        ag = SealedActivationGraph()
        act = ag.add_activation(ar_plugins.const, 10)
        act.trigger_on_descendants = mock.Mock()

        act_2 = ag.add_activation(ar_plugins.add, act.symbol, 15)
        act_2.trigger_on_result = mock.Mock()

        aed = ActivationEligibilityDetector(act)
        assert not aed.is_eligible

        # 'Invoking' act_2's trigger which makes act eligible
        del act_2.trigger_on_result

        # Update
        aed.update(act_2, [])

        # Check
        actual = aed.is_eligible

        expected = True
        self.assertEqual(expected, actual)

    def test_update_other_non_invoked_descendant_stays(self):
        ag = SealedActivationGraph()
        act = ag.add_activation(ar_plugins.const, 10)
        act.trigger_on_descendants = mock.Mock()

        act_2 = ag.add_activation(ar_plugins.add, act.symbol, 15)
        act_2.trigger_on_result = mock.Mock()

        act_3 = ag.add_activation(ar_plugins.sub, act.symbol, 15)
        act_3.trigger_on_result = mock.Mock()

        aed = ActivationEligibilityDetector(act)
        assert not aed.is_eligible

        # 'Invoking' act_3's trigger but the act_2's trigger stays
        del act_3.trigger_on_result

        # Update
        aed.update(act_3, [])

        # Check
        actual = aed.is_eligible

        expected = False
        self.assertEqual(expected, actual)

    def test_update_new_non_invoked_descendant_is_created(self):
        ag = SealedActivationGraph()
        act = ag.add_activation(ar_plugins.const, 10)
        act.trigger_on_descendants = mock.Mock()

        def act_2_trigger(data):  # noqa
            act_3 = ag.add_activation(ar_plugins.sub, act_2.symbol, 15)
            act_3.trigger_on_result = mock.Mock()
            return [act_3]

        act_2 = ag.add_activation(ar_plugins.add, act.symbol, 15)
        act_2.trigger_on_result = act_2_trigger

        aed = ActivationEligibilityDetector(act)
        assert not aed.is_eligible

        # Calling act_2's trigger which creates act_3 with a trigger
        tm = act_2.trigger_on_result
        del act_2.trigger_on_result
        new_acts = tm(10 + 15)

        # Update
        aed.update(act_2, new_acts)

        # Check
        actual = aed.is_eligible

        expected = False
        self.assertEqual(expected, actual)

    def test_update_with_reset_trigger_on_descendants_eligible_again(self):
        ag = SealedActivationGraph()
        act = ag.add_activation(ar_plugins.const, 10)

        def act_trigger():
            act.trigger_on_descendants = mock.Mock()
            return []

        act.trigger_on_descendants = act_trigger

        aed = ActivationEligibilityDetector(act)
        assert aed.is_eligible

        # Calling act's trigger with re-set a new act's trigger
        tm = act.trigger_on_descendants
        del act.trigger_on_descendants
        new_acts = tm()

        # Update
        aed.update(act, new_acts)

        # Check
        actual = aed.is_eligible

        expected = True
        self.assertEqual(expected, actual)

    def test_update_with_reset_trigger_on_descendants_not_eligible_again(self):
        ag = SealedActivationGraph()
        act = ag.add_activation(ar_plugins.const, 10)

        def act_trigger():
            act.trigger_on_descendants = mock.Mock()
            act_2 = ag.add_activation(ar_plugins.add, act.symbol, 15)
            act_2.trigger_on_result = mock.Mock()
            return [act_2]

        act.trigger_on_descendants = act_trigger

        aed = ActivationEligibilityDetector(act)
        assert aed.is_eligible

        # Calling act's trigger with re-set a new act's trigger but also
        # creates act_2 with a trigger which makes act ineligible
        tm = act.trigger_on_descendants
        del act.trigger_on_descendants
        new_acts = tm()

        # Update
        aed.update(act, new_acts)

        # Check
        actual = aed.is_eligible

        expected = False
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
