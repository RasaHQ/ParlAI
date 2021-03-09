import random
from typing import List, Dict, Text, Any, Union, Tuple, Callable, Optional
import os
import json
import re

from parlai.core.agents import Agent
from parlai.core.opt import Opt
from parlai.core.params import ParlaiParser
from parlai.mturk.core.shared_utils import AssignState, print_and_log
from parlai.mturk.tasks.woz.knowledgebase import api
from parlai.mturk.tasks.woz.backend.commands import (
    QueryCommand,
    GuideCommand,
    DialogueCompletedCommand,
    UtterCommand,
    SilentCommand,
)


class NonMTurkAgent(Agent):
    def __init__(self, options: Opt) -> None:
        super(NonMTurkAgent, self).__init__(options, shared=None)

    def get_messages(self) -> List[Dict[Text, Any]]:
        # Note: Messages must contain a 'text' field
        return []

    def clear_messages(self) -> None:
        pass  # ToDo: Implement

    def is_final(self):
        return AssignState.STATUS_NONE

    def get_status(self):
        return AssignState.STATUS_NONE

    def set_status(self, *args, **kwargs) -> None:
        pass

    @property
    def worker_id(self):
        return None

    @property
    def assignment_id(self):
        return None  # ToDo: Implement

    @property
    def feedback(self):
        return None  # ToDo: Implement

    def submitted_hit(self) -> bool:
        return True


class WOZKnowledgeBaseAgent(NonMTurkAgent):
    """
    Agent that represents a knowledge base.
    """

    @staticmethod
    def add_cmdline_args(parser: ParlaiParser) -> None:
        """Add command line arguments for this agent."""
        pass

    def __init__(self, options: Opt):
        super().__init__(options)
        self.role = "KnowledgeBase"
        self.id = "KnowledgeBase"
        self._messages = []

    def observe(self, message: Union[Dict[Text, Any], QueryCommand]) -> None:
        if isinstance(message, QueryCommand):
            self.observation = message
        else:
            super(WOZKnowledgeBaseAgent, self).observe(message)

    def act(self) -> Dict[Text, Any]:
        """Generates a response to the last observation.

        Returns:
            Message with reply
        """

        if self.observation is None:
            return {"text": "Knowledge base invoked without observation."}

        constraints = self.observation.constraints
        api_name = self.observation.api_name
        try:
            items, count = api.call_api(api_name, constraints=constraints)
            reply = {
                "id": "KnowledgeBase",
                "text": f"Found {count} items in {api_name}. Example: {json.dumps(items)}.",
                "example_item": items,
                "api_name": api_name,
                "num_items": count,
            }
        except Exception as e:
            print_and_log(45, f"Could not interpret your query: {e}", False)
            reply = {
                "id": "KnowledgeBase",
                "text": "Nothing found.",
                "example_item": None,
                "api_name": api_name,
                "num_items": 0,
            }

        self._messages.append(reply)

        return reply


class WOZDummyAgent(NonMTurkAgent):
    """Agent returns a random response."""

    @staticmethod
    def add_cmdline_args(parser) -> None:
        """Add command line arguments for this agent."""
        parser = parser.add_argument_group('DummyAgent arguments')
        parser.add_argument(
            "--dummy-responses",
            type=str,
            default=None,
            help="File of candidate responses to choose from",
        )
        parser.add_argument(
            "--dummy-user", action="store_true", help="Use a dummy user",
        )

    def __init__(self, opt: Union[Opt, dict], role: Text) -> None:
        """Initialize this agent."""
        super().__init__(opt)
        self.id = "User"
        self.role = role
        self.id = role
        self._num_messages_sent = 0
        self._messages = []
        if opt.get("dummy_responses"):
            try:
                with open(opt.get("dummy_responses"), "r", encoding="utf-8") as file:
                    self.response_candidates = file.read().split("\n")
            except FileNotFoundError:
                self.response_candidates = [
                    f"I am a dummy agent that didn't find "
                    f"replies in '{os.path.abspath(opt.get('dummy_responses'))}'."
                ]
        else:
            self.response_candidates = None

    def act(self) -> Dict[Text, Any]:
        """Generates a response to the last observation.

        Returns:
            Message with reply
        """
        if not self.response_candidates:
            return {
                "id": self.getID(),
                "text": "DUMMY: No response candidates.",
                "role": self.role,
            }

        self._num_messages_sent += 1
        index = self._num_messages_sent % len(self.response_candidates)
        reply = {
            "id": self.getID(),
            "text": self.response_candidates[index],
            "role": self.role,
        }

        self._messages.append(reply)

        return reply


class WOZInstructorAgent(NonMTurkAgent):
    @staticmethod
    def add_cmdline_args(parser) -> None:
        """Adds command line arguments for this agent."""
        pass

    def __init__(self, options: Opt, rules: List[Dict[Text, Any]]) -> None:
        """Initialize this agent."""
        super().__init__(options)
        self.id = "Tutor"
        self.demo_role = None
        self._num_messages_sent = 0
        self._messages = []

        self._rules = rules  # Conditions on dialogue history + responses that should be uttered if those conditions are satisfied
        self._event_history = None  # Entire dialogue history (to be observed)

    def observe(self, history: List[Dict[Text, Any]]) -> None:
        self._event_history = history

    def act(self) -> Tuple[Dict[Text, Any], Dict[Text, Any]]:
        # print(f"acting on: {self._event_history}")
        if not self._event_history:
            return {}, {}
        for rule in self._rules:
            if rule.get("triggers_left", 1) > 0 and rule.get(
                "condition", self.constant_condition(False)
            )(self._event_history):
                # print(rule["message"])
                if rule.get("probability", 1.0) < 1.0 and random.uniform(
                    0.0, 1.0
                ) > rule.get("probability", 1.0):
                    continue
                last_agent = self._event_history[-1].get("Agent")
                if rule["target"] == last_agent:
                    continue
                rule["triggers_left"] -= 1
                if rule["target"] == "User":
                    return rule["message"], {}
                else:
                    return {}, rule["message"]

        return {}, {}

    def add_rule(
        self,
        condition: Callable,
        text: Text,
        target: Text,
        max_times_triggered: int = 10000,
        probability: float = 1.0,
    ) -> None:
        assert target == "User" or target == "Wizard"
        self._rules.append(
            {
                "condition": condition,
                "message": {"text": text, "id": "MTurk System"},
                "triggers_left": max_times_triggered,
                "probability": probability,
                "target": target,
            }
        )

    @staticmethod
    def num_turns_condition(
        min_num_turns: Optional[int], max_num_turns: Optional[int] = None
    ) -> Callable:
        _min_num_turns = min_num_turns or 0
        if max_num_turns is not None:
            return lambda history: (
                _min_num_turns <= num_turns(history) <= max_num_turns
            )
        else:
            return lambda history: (_min_num_turns <= num_turns(history))

    @staticmethod
    def random_turn_condition(
        min_num_turns: Optional[int], max_num_turns: int, count: int = 1
    ) -> Callable:
        assert max_num_turns > (min_num_turns or 0)
        n = random.sample(range(min_num_turns or 0, max_num_turns), count)
        print(f"Will trigger on turns {n}")
        return lambda history: num_turns(history) in n

    @staticmethod
    def kb_changed_condition(
        previous_api_name: Optional[Text] = None, new_api_name: Optional[Text] = None
    ) -> Callable:
        def wizard_changed_kb(history):
            if not history:
                return False
            api_name_stack = []
            for event in history[:-1]:
                if event.get("Action") == QueryCommand.command_name:
                    api_name_stack.append(event.get("API"))
                if event.get("Agent") == "User":
                    if api_name_stack:
                        api_name_stack = [api_name_stack[-1]]
            if len(api_name_stack) <= 1:
                return False
            elif previous_api_name and new_api_name:
                return (api_name_stack[-2] == previous_api_name) and (
                    api_name_stack[-1] == new_api_name
                )
            elif previous_api_name:
                return (api_name_stack[-2] == previous_api_name) and (
                    api_name_stack[-1] != previous_api_name
                )
            elif new_api_name:
                return (api_name_stack[-2] != new_api_name) and (
                    api_name_stack[-1] == new_api_name
                )
            else:
                return api_name_stack[-2] != api_name_stack[-1]

        return wizard_changed_kb

    @staticmethod
    def constant_condition(const: bool) -> Callable:
        return lambda _: const


class WOZWizardIntroAgent(NonMTurkAgent):
    @staticmethod
    def add_cmdline_args(parser) -> None:
        """Add command line arguments for this agent."""
        parser = parser.add_argument_group('DummyAgent arguments')
        parser.add_argument(
            "--wizard-intro",
            type=str,
            default=None,
            help="File with wizard intro tutorial",
        )

    def __init__(self, opt: Opt, role: Text) -> None:
        """Initialize this agent."""
        super().__init__(opt)
        self.id = "User"  # or "MTurk System" - changes on act()
        self.role = role
        self.demo_role = role
        self._num_messages_sent = 0
        self._step_index = 0
        self._correction_index = 0
        self._messages = []
        self.worker_succeeded = False
        if opt.get("wizard_intro"):
            with open(opt.get("wizard_intro"), "r") as file:
                self.guidelines = json.load(file)
            self.steps = self.guidelines.get("Steps", [])
        else:
            self.guidelines = None
            self.steps = []

        self.user = WOZDummyAgent(opt={}, role="User")

    def observe(self, event: Dict[Text, Any]) -> None:
        self.observation = event

    def act(self) -> Optional[Dict[Text, Any]]:
        """Generates a response to the last observation.

        Returns:
            Message with reply
        """
        if not self.guidelines:
            return GuideCommand("Dummy guide command.").message

        self._num_messages_sent += 1

        reply = None
        while reply is None:
            if self._step_index >= len(self.steps):
                self.worker_succeeded = True
                return DialogueCompletedCommand(sender=self.user).message
            current_step = self.steps[self._step_index]
            if "Guide" in current_step:
                self.id = "MTurk System"
                self._step_index += 1
                self._correction_index = 0
                self.observation = None
                reply = GuideCommand(text=current_step["Guide"]).message
            elif "Wizard" in current_step:
                if not self.observation:
                    reply = SilentCommand(sender=self.user).message
                elif step_condition_satisfied(
                    current_step["Wizard"], self.observation or {}
                ):
                    self._step_index += 1
                    self.observation = None
                else:
                    corrections = current_step.get("Corrections", [])
                    if self._correction_index >= len(corrections):
                        reply = DialogueCompletedCommand(sender=self.user).message
                    else:
                        reply = GuideCommand(
                            text=corrections[self._correction_index]
                        ).message
                        self._correction_index += 1
                    self.observation = None
            elif "User" in current_step:
                self.id = "User"
                self._step_index += 1
                self._correction_index = 0
                self.observation = None
                reply = UtterCommand(
                    text=current_step["User"], sender=self.user
                ).message
        return reply


def step_condition_satisfied(
    step: Union[str, Dict[Text, Any]], observation: Dict[Text, Any]
) -> bool:
    if isinstance(step, str):
        return similar(observation.get("Text", ""), step)
    elif isinstance(step, dict):

        if "TextRegex" in step:
            if (
                re.fullmatch(
                    step["TextRegex"], observation.get("Text", ""), flags=re.IGNORECASE
                )
                is None
            ):
                return False
            del step["TextRegex"]

        if "Constraints" in step:
            if "Constraints" not in observation:
                return False
            observed_constraints = observation["Constraints"]
            for expected_constraint in step["Constraints"]:
                try:
                    observed_constraint = select_first(
                        observed_constraints,
                        lambda c: constraint_name(c)
                        == constraint_name(expected_constraint),
                    )
                except (StopIteration, ValueError):
                    return False

                if not similar(
                    constraint_value(expected_constraint),
                    constraint_value(observed_constraint),
                ):
                    return False
            del step["Constraints"]

        if "PrimaryItem" in step:
            if not observation.get("PrimaryItem"):
                return False
            observed_item = observation.get("PrimaryItem")
            for key, value in step.get("PrimaryItem", {}).items():
                if key not in observed_item:
                    return False
                if not similar(value, observed_item.get(key, "")):
                    return False
            del step["PrimaryItem"]

        if "SecondaryItem" in step:
            if not observation.get("SecondaryItem"):
                return False
            observed_item = observation.get("SecondaryItem")
            for key, value in step.get("SecondaryItem", {}).items():
                if key not in observed_item:
                    return False
                if not similar(key, observed_item.get(key, "")):
                    return False
            del step["SecondaryItem"]

        return all([similar(step[k], observation[k]) for k in step if k in observation])


def similar(a: Any, b: Any):
    if isinstance(a, str) and isinstance(b, str):
        return a.lower().strip() == b.lower().strip()
    else:
        return a == b


def select_first(iterable, condition=lambda x: True):
    """
    Returns the first item in the `iterable` that
    satisfies the `condition`.

    If the condition is not given, returns the first item of
    the iterable.

    Raises `StopIteration` if no item satysfing the condition is found.

    >>> select_first( (1,2,3), condition=lambda x: x % 2 == 0)
    2
    >>> select_first(range(3, 100))
    3
    >>> select_first( () )
    Traceback (most recent call last):
    ...
    StopIteration
    """

    return next(x for x in iterable if condition(x))


def constraint_name(constraint: Dict[Text, Any]):
    if len(constraint) != 1:
        raise ValueError(f"Constraint {constraint} does not have single item.")
    return list(constraint.keys())[0]


def constraint_value(constraint: Dict[Text, Any]):
    if len(constraint) != 1:
        raise ValueError(f"Constraint {constraint} does not have single item.")
    return list(constraint.values())[0]


def num_turns(history: List[Dict[Text, Any]]) -> int:
    result = 0
    for event in history:
        if event.get("Agent") == "User":
            result += 1
    return result
