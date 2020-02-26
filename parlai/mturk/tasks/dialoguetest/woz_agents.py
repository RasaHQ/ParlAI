from typing import Dict, Text, Any, Optional, List, Union

from parlai.core.agents import Agent
from parlai.core.opt import Opt
from parlai.core.params import ParlaiParser
from parlai.mturk.core.shared_utils import AssignState
import parlai.mturk.tasks.dialoguetest.api as api
import os
import json

from parlai.mturk.tasks.dialoguetest import echo


class WOZKnowledgeBaseAgent(Agent):
    """
    Agent that represents a knowledge base.
    """

    @staticmethod
    def add_cmdline_args(parser: ParlaiParser) -> None:
        """Add command line arguments for this agent."""
        pass

    def __init__(self, opt: Opt, shared: Optional[bool] = None):
        """Initialize this agent."""
        super().__init__(opt)
        self.role = "KnowledgeBase"
        self.demo_role = "KnowledgeBase"
        self._messages = []

    def act(self) -> Dict[Text, Any]:
        """Generates a response to the last observation.

        Returns:
            Message with reply
        """
        observation = self.observation

        if observation is None:
            return {"text": "Knowledge base invoked without observation."}

        query = observation.get("query")
        echo.log_write(f"KBQuery: {query}")

        if not query:
            return {"text": "Knowledge base invoked with empty query."}

        try:
            constraints = self._parse(query)
            apartment, count = api.call_api("apartment_search", constraints=constraints)
            reply = {
                "id": "KnowledgeBase",
                "text": f"Found {count} apartments. Example: {json.dumps(apartment)}.",
            }
        except Exception as e:
            print("Error: ", e)
            import traceback
            traceback.print_exc()

            reply = {
                "id": "KnowledgeBase",
                "text": f"Could not interpret your query: {e}",
            }

        self._messages.append(reply)

        return reply

    def _parse_old(self, text: Text) -> Dict[Text, Any]:
        return eval(text)

    def _parse_new(self, text: Text) -> Dict[Text, Any]:
        constraints = eval(text)
        result = [
            {name: eval(expr)}
            for constraint in constraints
            for name, expr in constraint.items()
        ]
        return result[0]

    def _parse_json(self, constraints: List[Dict[Text, Text]]) -> Dict[Text, Any]:
        result = [
            {name: eval(expr)}
            for constraint in constraints
            for name, expr in constraint.items()
        ]
        return result[0]

    def _parse(self, text: Union[Text, List]) -> Dict[Text, Any]:
        if isinstance(text, list):
            return self._parse_json(text)
        else:
            if text.startswith("["):
                return self._parse_new(text)
            else:
                return self._parse_old(text)

    def get_messages(self) -> List[Dict[Text, Any]]:
        # Note: Messages must contain a 'text' field
        return self._messages

    def clear_messages(self) -> None:
        pass  # ToDo: Implement

    def is_final(self):
        return AssignState.STATUS_DONE

    def get_status(self):
        return AssignState.STATUS_DONE

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


class WOZDummyAgent(Agent):
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
            "--dummy-user",
            action="store_true",
            help="Use a dummy user",
        )

    def __init__(self, opt: Opt, role: Text) -> None:
        """Initialize this agent."""
        super().__init__(opt)
        self.id = "DummyAgent"
        self.role = role
        self.demo_role = role
        self._num_messages_sent = 0
        self._messages = []
        if opt.get("dummy_responses"):
            try:
                with open(opt.get("dummy_responses"), "r", encoding="utf-8") as file:
                    self.response_candidates = file.read().split("\n")
            except FileNotFoundError:
                self.response_candidates = [f"I am a dummy agent that didn't find "
                                            f"replies in '{os.path.abspath(opt.get('dummy_responses'))}'."]
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

    def get_messages(self) -> List[Dict[Text, Any]]:
        # Note: Messages must contain a 'text' field
        return self._messages

    def clear_messages(self) -> None:
        pass  # ToDo: Implement

    def is_final(self):
        return AssignState.STATUS_DONE

    def get_status(self):
        return AssignState.STATUS_DONE

    def set_status(self, *args, **kwargs):
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
