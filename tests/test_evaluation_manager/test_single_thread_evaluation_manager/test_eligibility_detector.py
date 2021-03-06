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
        act_1 = ag.add_activation(ar_plugins.const, 10)
        aed = ActivationEligibilityDetector(act_1)

        actual = aed.is_eligible

        expected = None
        self.assertEqual(expected, actual)

    def test_is_eligible_simple_true(self):
        ag = SealedActivationGraph()
        act_1 = ag.add_activation(ar_plugins.const, 10)
        act_1.trigger_on_descendants = mock.Mock()

        act_2 = ag.add_activation(ar_plugins.add, act_1.symbol, 15)  # noqa
        # This activation should not cause a problem, as it does not have a
        # trigger

        aed = ActivationEligibilityDetector(act_1)

        actual = aed.is_eligible

        expected = True
        self.assertEqual(expected, actual)

    def test_is_eligible_simple_false(self):
        ag = SealedActivationGraph()
        act_1 = ag.add_activation(ar_plugins.const, 10)
        act_1.trigger_on_descendants = mock.Mock()

        act_2 = ag.add_activation(ar_plugins.add, act_1.symbol, 15)  # This
        # activation causes the ineligibility
        act_2.trigger_on_result = mock.Mock()

        aed = ActivationEligibilityDetector(act_1)

        actual = aed.is_eligible

        expected = False
        self.assertEqual(expected, actual)

    def test_activation_property(self):
        ag = SealedActivationGraph()
        act_1 = ag.add_activation(ar_plugins.const, 10)
        aed = ActivationEligibilityDetector(act_1)

        actual = aed.activation

        expected = act_1
        self.assertEqual(expected, actual)

    def test_update_with_not_related_activation(self):
        ag = SealedActivationGraph()
        act_1 = ag.add_activation(ar_plugins.const, 10)
        act_1.trigger_on_descendants = mock.Mock()

        act_2 = ag.add_activation(ar_plugins.add, act_1.symbol, 15)  # This
        # activation causes the ineligibility
        act_2.trigger_on_result = mock.Mock()

        act_3 = ag.add_activation(ar_plugins.const, 25)
        act_3.trigger_on_result = mock.Mock()

        aed = ActivationEligibilityDetector(act_1)
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
        act_1 = ag.add_activation(ar_plugins.const, 10)
        act_1.trigger_on_descendants = mock.Mock()

        act_2 = ag.add_activation(ar_plugins.add, act_1.symbol, 15)
        act_2.trigger_on_result = mock.Mock()

        aed = ActivationEligibilityDetector(act_1)
        assert not aed.is_eligible

        # 'Invoking' act_2's trigger which makes act_1 eligible
        del act_2.trigger_on_result

        # Update
        aed.update(act_2, [])

        # Check
        actual = aed.is_eligible

        expected = True
        self.assertEqual(expected, actual)

    def test_update_other_non_invoked_descendant_stays(self):
        ag = SealedActivationGraph()
        act_1 = ag.add_activation(ar_plugins.const, 10)
        act_1.trigger_on_descendants = mock.Mock()

        act_2 = ag.add_activation(ar_plugins.add, act_1.symbol, 15)
        act_2.trigger_on_result = mock.Mock()

        act_3 = ag.add_activation(ar_plugins.sub, act_1.symbol, 15)
        act_3.trigger_on_result = mock.Mock()

        aed = ActivationEligibilityDetector(act_1)
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
        act_1 = ag.add_activation(ar_plugins.const, 10)
        act_1.trigger_on_descendants = mock.Mock()

        def act_2_trigger(data):  # noqa
            act_3 = ag.add_activation(ar_plugins.sub, act_2.symbol, 15)
            act_3.trigger_on_result = mock.Mock()
            return [act_3]

        act_2 = ag.add_activation(ar_plugins.add, act_1.symbol, 15)
        act_2.trigger_on_result = act_2_trigger

        aed = ActivationEligibilityDetector(act_1)
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
        act_1 = ag.add_activation(ar_plugins.const, 10)

        def act_trigger():
            act_1.trigger_on_descendants = mock.Mock()
            return []

        act_1.trigger_on_descendants = act_trigger

        aed = ActivationEligibilityDetector(act_1)
        assert aed.is_eligible

        # Calling act_1's trigger with re-set a new act_1's trigger
        tm = act_1.trigger_on_descendants
        del act_1.trigger_on_descendants
        new_acts = tm()

        # Update
        aed.update(act_1, new_acts)

        # Check
        actual = aed.is_eligible

        expected = True
        self.assertEqual(expected, actual)

    def test_update_with_reset_trigger_on_descendants_not_eligible_again(self):
        ag = SealedActivationGraph()
        act_1 = ag.add_activation(ar_plugins.const, 10)

        def act_trigger():
            act_1.trigger_on_descendants = mock.Mock()
            act_2 = ag.add_activation(ar_plugins.add, act_1.symbol, 15)
            act_2.trigger_on_result = mock.Mock()
            return [act_2]

        act_1.trigger_on_descendants = act_trigger

        aed = ActivationEligibilityDetector(act_1)
        assert aed.is_eligible

        # Calling act_1's trigger with re-set a new act_1's trigger but also
        # creates act_2 with a trigger which makes act_1 ineligible
        tm = act_1.trigger_on_descendants
        del act_1.trigger_on_descendants
        new_acts = tm()

        # Update
        aed.update(act_1, new_acts)

        # Check
        actual = aed.is_eligible

        expected = False
        self.assertEqual(expected, actual)


class TestEligibilityDetector(unittest.TestCase):
    def test_eligible_and_tracked_activations_simple(self):
        ag = SealedActivationGraph()
        act_1 = ag.add_activation(ar_plugins.const, 10)
        act_1.trigger_on_descendants = mock.Mock()

        act_2 = ag.add_activation(ar_plugins.add, act_1.symbol, 15)
        act_2.trigger_on_result = mock.Mock()

        act_3 = ag.add_activation(ar_plugins.const, 100)
        act_3.trigger_on_descendants = mock.Mock()

        ed = EligibilityDetector(ag)

        actual_eligible = ed.eligible_activations
        actual_tracked = ed.tracked_activations

        expected_eligible = [act_3]
        expected_tracked = expected_eligible + [act_1]
        self.assertCountEqual(expected_eligible, actual_eligible)
        self.assertCountEqual(expected_tracked, actual_tracked)

    def test_graph_property(self):
        ag = SealedActivationGraph()
        ed = EligibilityDetector(ag)

        actual = ed.graph

        expected = ag
        self.assertEqual(expected, actual)

    def test_update_without_creating_node_with_trigger(self):
        ag = SealedActivationGraph()
        act_1 = ag.add_activation(ar_plugins.const, 10)
        act_1.trigger_on_descendants = mock.Mock()

        act_2 = ag.add_activation(ar_plugins.add, act_1.symbol, 15)

        def act_2_trigger(data):
            act_3 = ag.add_activation(ar_plugins.sub, act_2.symbol, 30)
            return [act_3]

        act_2.trigger_on_result = act_2_trigger

        act_4 = ag.add_activation(ar_plugins.const, 100)
        act_4.trigger_on_descendants = mock.Mock()

        ed = EligibilityDetector(ag)

        # Calling act_2's trigger, new act_3 has no trigger, thus act_1 is
        # eligible
        # Act_4 is still outside the action and remains eligible
        tm = act_2.trigger_on_result
        del act_2.trigger_on_result
        new_acts = tm(25)

        # Update
        ed.update(act_2, new_acts)

        actual_eligible = ed.eligible_activations
        actual_tracked = ed.tracked_activations

        expected_eligible = [act_1, act_4]
        expected_tracked = expected_eligible
        self.assertCountEqual(expected_eligible, actual_eligible)
        self.assertCountEqual(expected_tracked, actual_tracked)

    def test_update_with_creating_node_with_trigger(self):
        ag = SealedActivationGraph()
        act_1 = ag.add_activation(ar_plugins.const, 10)
        act_1.trigger_on_descendants = mock.Mock()

        act_2 = ag.add_activation(ar_plugins.add, act_1.symbol, 15)

        def act_2_trigger(data):
            act_3 = ag.add_activation(ar_plugins.sub, act_2.symbol, 30)
            act_3.trigger_on_descendants = mock.Mock()
            return [act_3]

        act_2.trigger_on_result = act_2_trigger

        act_4 = ag.add_activation(ar_plugins.const, 100)
        act_4.trigger_on_descendants = mock.Mock()

        ed = EligibilityDetector(ag)

        # Calling act_2's trigger, new act_3 has a trigger, thus act_1 is
        # ineligible
        # Act_4 is still outside the action and remains eligible
        tm = act_2.trigger_on_result
        del act_2.trigger_on_result
        new_acts = tm(25)  # Single Activation act_3

        # Update
        ed.update(act_2, new_acts)

        actual_eligible = ed.eligible_activations
        actual_tracked = ed.tracked_activations

        expected_eligible = [act_4] + new_acts
        expected_tracked = expected_eligible + [act_1]
        self.assertCountEqual(expected_eligible, actual_eligible)
        self.assertCountEqual(expected_tracked, actual_tracked)

    def test_update_after_trigger_on_descendants_invocation_and_reset(self):
        ag = SealedActivationGraph()
        act_1 = ag.add_activation(ar_plugins.const, 10)
        act_1.trigger_on_descendants = mock.Mock()

        act_2 = ag.add_activation(ar_plugins.add, act_1.symbol, 15)

        def act_2_trigger():
            act_3 = ag.add_activation(ar_plugins.sub, act_2.symbol, 30)
            act_2.trigger_on_descendants = mock.Mock()
            return [act_3]

        act_2.trigger_on_descendants = act_2_trigger

        act_4 = ag.add_activation(ar_plugins.const, 100)
        act_4.trigger_on_descendants = mock.Mock()

        ed = EligibilityDetector(ag)

        # Calling act_2's trigger, new act_3 has no trigger, however, act_2's
        # trigger is re-set, thus act_1 is ineligible
        # Act_4 is still outside the action and remains eligible
        tm = act_2.trigger_on_descendants
        del act_2.trigger_on_descendants
        new_acts = tm()  # Single Activation act_3

        # Update
        ed.update(act_2, new_acts)

        actual_eligible = ed.eligible_activations
        actual_tracked = ed.tracked_activations

        expected_eligible = [act_2, act_4]
        expected_tracked = expected_eligible + [act_1]
        self.assertCountEqual(expected_eligible, actual_eligible)
        self.assertCountEqual(expected_tracked, actual_tracked)

    def test_update_remove_eligibility_of_previously_eligible_node(self):
        ag = SealedActivationGraph()
        act_1 = ag.add_activation(ar_plugins.const, 10)
        act_1.trigger_on_descendants = mock.Mock()

        act_2 = ag.add_activation(ar_plugins.add, act_1.symbol, 15)

        def act_2_trigger():
            act_3 = ag.add_activation(ar_plugins.sub, act_4.symbol, 30)
            act_3.trigger_on_result = mock.Mock()
            return [act_3]

        act_2.trigger_on_descendants = act_2_trigger

        act_4 = ag.add_activation(ar_plugins.const, 100)
        act_4.trigger_on_descendants = mock.Mock()

        ed = EligibilityDetector(ag)

        # Calling act_2's trigger, new act_3 with a trigger is descendant of
        # act_4, thus act_4 is ineligible
        # Only act_1 is then eligible
        tm = act_2.trigger_on_descendants
        del act_2.trigger_on_descendants
        new_acts = tm()  # Single Activation act_3

        # Update
        ed.update(act_2, new_acts)

        actual_eligible = ed.eligible_activations
        actual_tracked = ed.tracked_activations

        expected_eligible = [act_1]
        expected_tracked = expected_eligible + [act_4]
        self.assertCountEqual(expected_eligible, actual_eligible)
        self.assertCountEqual(expected_tracked, actual_tracked)

    def test_update_with_graphs_trigger(self):
        ag = SealedActivationGraph()

        act_1 = ag.add_activation(ar_plugins.const, 10)
        act_1.trigger_on_descendants = mock.Mock()

        def ag_trigger():
            act_2 = ag.add_activation(ar_plugins.sub, act_1.symbol, 30)
            act_2.trigger_on_descendants = mock.Mock()
            return [act_2]

        ag.trigger_method = ag_trigger

        ed = EligibilityDetector(ag)

        # Calling ag's trigger, new act_2 with a trigger is descendant of
        # act_1, thus act_1 is ineligible
        # Only act_2 is then eligible
        tm = ag.trigger_method
        del ag.trigger_method
        new_acts = tm()  # Single Activation act_3

        # Update
        ed.update(ag, new_acts)

        actual_eligible = ed.eligible_activations
        actual_tracked = ed.tracked_activations

        expected_eligible = new_acts
        expected_tracked = expected_eligible + [act_1]
        self.assertCountEqual(expected_eligible, actual_eligible)
        self.assertCountEqual(expected_tracked, actual_tracked)

    def test_update_result_assign_descendants_to_itself(self):
        ag = SealedActivationGraph()

        act_1 = ag.add_activation(ar_plugins.const, 10)

        def act_1_trigger(data):
            act_1.trigger_on_descendants = mock.Mock()
            return []

        act_1.trigger_on_result = act_1_trigger

        ed = EligibilityDetector(ag)

        # Calling ag's trigger, new act_2 with a trigger is descendant of
        # act_1, thus act_1 is ineligible
        # Only act_2 is then eligible
        tm = act_1.trigger_on_result
        del act_1.trigger_on_result
        new_acts = tm(10)  # Single Activation act_3

        # Update
        ed.update(act_1, new_acts)

        actual_eligible = ed.eligible_activations
        actual_tracked = ed.tracked_activations

        expected_eligible = [act_1]
        expected_tracked = [act_1]
        self.assertCountEqual(expected_eligible, actual_eligible)
        self.assertCountEqual(expected_tracked, actual_tracked)


if __name__ == '__main__':
    unittest.main()
