import json
import os
from typing import Text, Dict, Any, List, Optional, Union, Tuple
import time

from parlai import PROJECT_PATH
from parlai.core.agents import Agent
# DO NOT REMOVE THIS IMPORT (needed for eval):
from parlai.mturk.core.agents import MTurkAgent, MTURK_DISCONNECT_MESSAGE, RETURN_MESSAGE, TIMEOUT_MESSAGE
from parlai.mturk.core.shared_utils import print_and_log
from parlai.mturk.tasks.woz.knowledgebase import api

__all_constants = None

DEFAULT_SCHEMA_URLS = {
    "followup_doctor_appointment": "https://i.imgur.com/OdjFGll.jpg",
    "weather": "https://i.imgur.com/yVozOzY.jpg",
    "party_rsvp": "https://i.imgur.com/4Pz33hK.jpg",
    "spaceship_life_support": "https://i.imgur.com/Ts0fkey.jpg",
    "spaceship_access_codes": "https://i.imgur.com/FmuNL4M.jpg",
    "book_doctor_appointment": "https://i.imgur.com/J5zxJmO.jpg",
    "restaurant_search": "https://i.imgur.com/wnmwuOT.jpg",
    "ride_change": "https://i.imgur.com/eFNOMNJ.jpg",
    "trivia": "https://i.imgur.com/T0c2Cxw.jpg",
    "restaurant_reserve": "https://i.imgur.com/1YDWRLf.png",
    "book_apartment_viewing": "https://i.imgur.com/rjpZovV.jpg",
    "ride_status": "https://i.imgur.com/yjjqvuM.jpg",
    "bank_fraud_report": "https://i.imgur.com/CRJFvkk.jpg",
    "hotel_service_request": "https://i.imgur.com/bOxmgLz.jpg",
    "party_plan": "https://i.imgur.com/HMsuGxR.jpg",
    "schedule_meeting": "https://i.imgur.com/6pIfKIz.jpg",
    "hotel_search": "https://i.imgur.com/BkUBBg7.jpg",
    "plane_reserve": "https://i.imgur.com/QlpRuAX.jpg",
    "hotel_reserve": "https://i.imgur.com/tgOz4pz.jpg",
    "plane_search": "https://i.imgur.com/F9p6MBi.jpg",
    "trip_directions": "https://i.imgur.com/V4O0yaw.jpg",
    "book_ride": "https://drive.google.com/uc?id=1zYWS2H0XMuJEoy6QRWKr51weyVztMZai",
    "apartment_search": "https://i.imgur.com/yICteJ1.jpg",
    "bank_balance": "https://i.imgur.com/71cZyxI.jpg"
}

DEFAULT_USER_INSTRUCTION = (
    "Follow the instructions and comments of the MTurk System bot (darker yellow boxes in the dialogue). "
    "Do not end the dialogue before the MTurk System bot (not the assistant) has told you to do so. "
)

DEFAULT_WIZARD_INSTRUCTION = "Follow the flow chart(s) and help the user."

DEFAULT_USER_COMPLETION_QUESTIONS = [
    "Did the assistant stay calm and helpful throughout the dialogue?"
]

DEFAULT_WIZARD_COMPLETION_QUESTIONS = [
    "Did the user change his/her mind about what he/she wants at any time?",
    "Did the user become aggressive or annoyed during the dialogue? (Note: some users may be instructed to be annoying.)",
    "Where you unsure about what to do at any time? (Feel free to send us an email with details.)",
]


def is_disconnected(act):
    return 'text' in act and act['text'] in [
        MTURK_DISCONNECT_MESSAGE,
        RETURN_MESSAGE,
        TIMEOUT_MESSAGE,
    ]


def all_constants():
    global __all_constants
    if not __all_constants:
        with open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "constants.json"),
            "r",
        ) as file:
            __all_constants = json.load(file)
    return __all_constants


DOMAINS_OF_TASKS = {
    "apartment_search": "apartment",
    "bank_balance": "bank",
    "bank_fraud_report": "bank",
    "book_apartment_viewing": "apartment",
    "book_doctor_appointment": "doctor",
    "book_ride": "ride",
    "followup_doctor_appointment": "doctor",
    "hotel_reserve": "hotel",
    "hotel_search": "hotel",
    "hotel_service_request": "hotel",
    "movie_search": "movie",
    "party_plan": "party",
    "party_rsvp": "party",
    "plane_reserve": "plane",
    "plane_search": "plane",
    "restaurant_reserve": "restaurant",
    "restaurant_search": "restaurant",
    "ride_change": "ride",
    "ride_status": "ride",
    "schedule_meeting": "meeting",
    "shopping_order_item": "shopping",
    "shopping_order_status": "shopping",
    "shopping_search": "shopping",
    "spaceship_access_codes": "spaceship",
    "spaceship_life_support": "spaceship",
    "trip_directions": "trip",
    "trip_traffic": "trip",
    "trivia": "trivia",
    "weather": "weather",
}


class Command:
    def __init__(self, sender: Optional[Agent] = None) -> None:
        self._command_name = None
        self._sender = sender

    @property
    def sender(self):
        return self._sender

    @property
    def message(self) -> Dict[Text, Any]:
        raise NotImplementedError()

    @staticmethod
    def from_message(
        sender: Agent,
        text: Optional[Text] = None,
        extracted_from_text: Optional[Text] = None,
        suggestions: Optional[List[Text]] = None,
        task_description: Optional[Text] = None,
        completion_requirements: Optional[List[Text]] = None,
        completion_questions: Optional[List[Text]] = None,
        form_description: Optional[Dict[Text, Any]] = None,
        role: Optional[Text] = None,
    ) -> Optional["Command"]:
        raise NotImplementedError()

    @property
    def event(self) -> Optional[Dict[Text, Any]]:
        raise NotImplementedError()


class AgentCommand(Command):
    def __init__(self, sender: Optional[Agent] = None):
        super(AgentCommand, self).__init__(sender)

    @property
    def message(self) -> Dict[Text, Any]:
        raise NotImplementedError()

    @staticmethod
    def from_message(sender: Agent, **kwargs) -> Optional["Command"]:
        raise NotImplementedError()

    @property
    def event(self) -> Optional[Dict[Text, Any]]:
        raise NotImplementedError()


class WorkerCommand(AgentCommand):
    def __init__(self, sender: Optional[Agent] = None):
        super(WorkerCommand, self).__init__(sender)

    @property
    def message(self) -> Dict[Text, Any]:
        raise NotImplementedError()

    @staticmethod
    def from_message(sender: Agent, **kwargs,) -> Optional["Command"]:
        raise NotImplementedError()

    @property
    def event(self) -> Optional[Dict[Text, Any]]:
        raise NotImplementedError()


class WizardCommand(WorkerCommand):
    def __init__(self, sender: Optional[Agent] = None):
        super(WizardCommand, self).__init__(sender)

    @property
    def message(self) -> Dict[Text, Any]:
        raise NotImplementedError()

    @staticmethod
    def from_message(
        sender: Agent,
        text: Optional[Text] = None,
        extracted_from_text: Optional[Text] = None,
    ) -> Optional["Command"]:
        raise NotImplementedError()

    @property
    def event(self) -> Optional[Dict[Text, Any]]:
        return {
            "Agent": self._sender.id,
            "Action": self._command_name,
            "UnixTime": int(time.time()),
        }


class BackendCommand(Command):
    def __init__(self):
        super(BackendCommand, self).__init__(sender=None)

    @property
    def message(self) -> Dict[Text, Any]:
        raise NotImplementedError()

    @staticmethod
    def from_message(sender: Agent, **kwargs) -> Optional["Command"]:
        raise NotImplementedError()

    @property
    def event(self) -> Optional[Dict[Text, Any]]:
        return None


class UtterCommand(WorkerCommand):
    def __init__(self, text: Text, sender: Agent):
        super(UtterCommand, self).__init__(sender)
        self._command_name = "utter"

        self._text = text

    @property
    def message(self) -> Dict[Text, Any]:
        return {
            "id": self._sender.id,
            "text": self._text,
        }

    @staticmethod
    def from_message(
        sender: Agent, text: Optional[Text] = None, **kwargs
    ) -> Optional["Command"]:
        if text is None:
            raise ValueError("No text given")
        return UtterCommand(text=text, sender=sender)

    @property
    def event(self) -> Optional[Dict[Text, Any]]:
        return {
            "Agent": self._sender.id,
            "Action": self._command_name,
            "Text": self._text,
            "UnixTime": int(time.time()),
        }


class SilentCommand(WorkerCommand):

    _command_name = "silent"

    @property
    def message(self) -> Dict[Text, Any]:
        return {
            "id": self._sender.id,
            "text": "<silent>",
        }

    @staticmethod
    def from_message(
        sender: Agent, text: Optional[Text] = None, **kwargs
    ) -> Optional["Command"]:
        return SilentCommand(sender=sender)

    @property
    def event(self) -> Optional[Dict[Text, Any]]:
        return {
            "Agent": self._sender.id,
            "Action": self._command_name,
            "UnixTime": int(time.time()),
        }


class SetupCommand(BackendCommand):
    def __init__(self, scenario: Text, role: Text,) -> None:
        super(SetupCommand, self).__init__()
        self._command_name = all_constants()["back_to_front"]["command_setup"]

        scenario_file_name = os.path.join(
            PROJECT_PATH,
            "parlai",
            "mturk",
            "tasks",
            "woz",
            "scenarios",
            scenario + ".json",
        )
        if not os.path.exists(scenario_file_name):
            raise FileNotFoundError(f"Could not find '{scenario_file_name}'.")
        with open(scenario_file_name, "r",) as file:
            scenario = json.load(file)

        self._command_name = all_constants()["back_to_front"]["command_setup"]
        image_not_found_url = "https://stockpictures.io/wp-content/uploads/2020/01/image-not-found-big.png"

        self._is_happy = os.path.basename(scenario_file_name).startswith("happy")
        self._wizard_capabilities = []

        try:
            form_description = {}
            for api_name in scenario["api_names"]:
                api_file_name = os.path.join(
                    PROJECT_PATH,
                    "parlai",
                    "mturk",
                    "tasks",
                    "woz",
                    "knowledgebase",
                    "apis",
                    api_name + ".json",
                )
                with open(api_file_name, "r") as file:
                    api_description = json.load(file)
                form_description[api_name] = api_description
                schema_url = scenario.get("schema_urls", {}).get(api_name)
                if not schema_url:
                    schema_url = DEFAULT_SCHEMA_URLS.get(api_name, image_not_found_url)
                form_description[api_name]["schema_url"] = schema_url

                self._wizard_capabilities.append(
                    {
                        "Task": api_name,
                        "Domain": DOMAINS_OF_TASKS.get(api_name, "UNDEFINED"),
                        "SchemaURL": schema_url,
                        # "FormDescription": api_description,
                    }
                )

            if role == "User":
                self._task_description = scenario["instructions"]["User"].get(
                    "task_description", DEFAULT_USER_INSTRUCTION
                )
                self._completion_questions = scenario["instructions"]["User"].get(
                    "completion_questions", DEFAULT_USER_COMPLETION_QUESTIONS
                )
            else:
                self._task_description = scenario["instructions"][role].get(
                    "task_description", DEFAULT_WIZARD_INSTRUCTION
                )
                self._completion_questions = scenario["instructions"][role].get(
                    "completion_questions", DEFAULT_WIZARD_COMPLETION_QUESTIONS
                )
            self._form_description = form_description

            self._role = role
            self._user_linear_guide = scenario["instructions"]["User"].get(
                "linear_guide"
            )
        except KeyError as error:
            raise ImportError(f"Invalid scenario file '{scenario_file_name}': {error}.")

    @property
    def capabilities(self) -> List[Dict[Text, Any]]:
        return self._wizard_capabilities

    @property
    def completion_questions(self) -> List[Text]:
        return self._completion_questions

    @property
    def task_description(self) -> Text:
        return self._task_description

    @property
    def user_linear_guide(self) -> Optional[List[Optional[Text]]]:
        return self._user_linear_guide

    @property
    def api_names(self) -> List[Text]:
        return list(self._form_description.keys())

    @property
    def is_happy(self):
        return self._is_happy

    @property
    def message(self) -> Dict[Text, Any]:
        return {
            "id": self._role,
            "text": "",
            "command": self._command_name,
            "task_description": self._task_description,
            "completion_requirements": [],  # No longer used
            "completion_questions": self._completion_questions,
            "form_description": self._form_description,
            "min_user_turns": len(self._user_linear_guide)
            if self._user_linear_guide
            else 0,
        }

    @staticmethod
    def from_message(**kwargs,) -> Optional["Command"]:
        raise RuntimeError("SetupCommand cannot be created from message.")


class GuideCommand(BackendCommand):

    _command_name = "guide"

    def __init__(self, text: Text) -> None:
        super(GuideCommand, self).__init__()
        self._text = text

    @property
    def message(self) -> Dict[Text, Any]:
        return {"id": all_constants()["agent_ids"]["system_id"], "text": self._text}

    @staticmethod
    def from_message(
        sender: Agent, extracted_from_text: Optional[Text] = None, **kwargs
    ) -> Optional["Command"]:
        if extracted_from_text is None:
            raise ValueError("No text for GuideCommand.")
        return GuideCommand(text=extracted_from_text)


class ReviewCommand(BackendCommand):
    def __init__(self, recipient: Agent) -> None:
        super(ReviewCommand, self).__init__()
        self._command_name = all_constants()["back_to_front"]["command_review"]
        self._recipient = recipient

    @property
    def message(self) -> Dict[Text, Any]:
        return {
            # "id": self._recipient.id,
            "text": "",
            "command": self._command_name,
        }

    @staticmethod
    def from_message(sender: Agent, **kwargs,) -> Optional["Command"]:
        return ReviewCommand(recipient=sender)


def safe_eval(expression: Text, default: Any = None) -> Any:
    # noinspection PyBroadException
    try:
        result = eval(expression)
    except:
        print_and_log(100, f"Problem with parsing expression: {expression}")
        return default
    return result


class QueryCommand(WizardCommand):

    command_name = "query"

    def __init__(self, query: Text, sender: Agent) -> None:
        super(QueryCommand, self).__init__(sender)
        self._command_name = self.command_name
        self._constraints = None
        self._constraints_raw = None
        self._api_name = None

        self._query = query
        self._parse(self._query)

    @property
    def message(self) -> Dict[Text, Any]:
        return {"id": self._sender.id, "text": "", "query": self._query}

    @staticmethod
    def from_message(
        sender: Agent, extracted_from_text: Optional[Text] = None, **kwargs
    ) -> Optional["Command"]:
        if extracted_from_text is None:
            raise ValueError("Nothing extracted from text for knowledge base")
        return QueryCommand(query=extracted_from_text, sender=sender)

    @property
    def constraints(self) -> List[Dict[Text, Any]]:
        return self._constraints

    @property
    def api_name(self) -> Text:
        return self._api_name

    def _parse(self, text: Text) -> None:
        data = safe_eval(text, dict())
        assert isinstance(data, dict)
        assert "constraints" in data
        assert "db" in data

        self._constraints = [
            {name: safe_eval(expr)}
            for constraint in data["constraints"]
            for name, expr in constraint.items() if len(expr) > 0
        ]

        self._constraints_raw = [
            {name: expr}
            for constraint in data["constraints"]
            for name, expr in constraint.items()
        ]

        self._api_name = data["db"]

    @property
    def event(self) -> Optional[Dict[Text, Any]]:
        return {
            "Agent": self._sender.id,
            "Action": self._command_name,
            "Constraints": self._constraints_raw,
            "API": self._api_name,
            "UnixTime": int(time.time()),
        }


class DialogueCompletedCommand(WorkerCommand):
    def __init__(self, sender: Agent) -> None:
        super(DialogueCompletedCommand, self).__init__(sender)
        self._command_name = "complete"

    @property
    def message(self) -> Dict[Text, Any]:
        return {
            "id": self._sender.id,
            "text": all_constants()["front_to_back"]["complete_prefix"],
        }

    @staticmethod
    def from_message(sender: Agent, **kwargs) -> Optional["Command"]:
        return DialogueCompletedCommand(sender=sender)

    @property
    def event(self) -> Optional[Dict[Text, Any]]:
        return {
            "Agent": self._sender.id,
            "Action": self._command_name,
            "UnixTime": int(time.time()),
        }


class TaskDoneCommand(WorkerCommand):
    def __init__(self, sender: Agent, answers: List[bool]) -> None:
        super(TaskDoneCommand, self).__init__(sender)
        self._command_name = "done"
        self.answers = answers

    @property
    def message(self) -> Dict[Text, Any]:
        return {"id": self._sender.id, "text": ""}

    @staticmethod
    def from_message(
        sender: Agent, extracted_from_text: Optional[Text] = None, **kwargs
    ) -> Optional["Command"]:
        answers = [
            value
            for _, value in sorted(
                json.loads(extracted_from_text).items(), key=(lambda item: item[0])
            )
        ]
        return TaskDoneCommand(sender=sender, answers=answers)


class SelectPrimaryCommand(WizardCommand):
    def __init__(self, sender: Agent, item: Dict[Text, Any]) -> None:
        super(SelectPrimaryCommand, self).__init__(sender)
        self._command_name = "select_primary"
        self._item = item
        print(f"Creating SelectPrimaryCommand: {item}")

    @property
    def item(self):
        return self._item

    @property
    def message(self) -> Dict[Text, Any]:
        print("Constructing message from SelectPrimaryCommand")
        return {
            "id": self._sender.id,
            "text": all_constants()["front_to_back"]["select_kb_entry_prefix"]
            + str(self._item),
        }

    @staticmethod
    def from_message(
        sender: Agent, extracted_from_text: Optional[Text] = None, **kwargs
    ) -> Optional["Command"]:
        _, item_text = extracted_from_text.strip().split("|", 1)
        item = json.loads(item_text)
        return SelectPrimaryCommand(sender=sender, item=item)

    @property
    def event(self) -> Optional[Dict[Text, Any]]:
        return {
            "Agent": self._sender.id,
            "Action": self._command_name,
            "UnixTime": int(time.time()),
        }


class SelectSecondaryCommand(WizardCommand):
    def __init__(self, sender: Agent, item: Dict[Text, Any]) -> None:
        super(SelectSecondaryCommand, self).__init__(sender)
        self._command_name = "select_secondary"
        self._item = item

    @property
    def item(self):
        return self._item

    @property
    def message(self) -> Dict[Text, Any]:
        print("Constructing message from SelectSecondaryCommand")
        return {
            "id": self._sender.id,
            "text": all_constants()["front_to_back"]["select_reference_kb_entry_prefix"]
            + str(self._item),
        }

    @staticmethod
    def from_message(
        sender: Agent, extracted_from_text: Optional[Text] = None, **kwargs
    ) -> Optional["Command"]:
        print(f"Constructing SelectSecondaryCommand from message {extracted_from_text}")
        _, item_text = extracted_from_text.strip().split("|", 1)
        item = json.loads(item_text)
        return SelectSecondaryCommand(sender=sender, item=item)

    @property
    def event(self) -> Optional[Dict[Text, Any]]:
        return {
            "Agent": self._sender.id,
            "Action": self._command_name,
            "UnixTime": int(time.time()),
        }


class SelectTopicCommand(WizardCommand):
    def __init__(self, sender: Agent, topic: Text) -> None:
        super(SelectTopicCommand, self).__init__(sender)
        self._command_name = "select_topic"
        self._topic = topic
        print(f"selecting: {topic}")

    @property
    def topic(self):
        return self._topic

    @property
    def message(self) -> Dict[Text, Any]:
        return {
            "id": self._sender.id,
            "text": all_constants()["front_to_back"]["select_topic_prefix"]
            + str(self._topic),
        }

    @staticmethod
    def from_message(
        sender: Agent, extracted_from_text: Optional[Text] = None, **kwargs
    ) -> Optional["Command"]:
        topic = extracted_from_text.strip()
        return SelectTopicCommand(sender=sender, topic=topic)

    @property
    def event(self) -> Optional[Dict[Text, Any]]:
        return {
            "Agent": self._sender.id,
            "Action": self._command_name,
            "Topic": self.topic,
            "UnixTime": int(time.time()),
        }


class RequestSuggestionsCommand(WizardCommand):
    def __init__(self, sender: Agent, query_text: Text) -> None:
        super(RequestSuggestionsCommand, self).__init__(sender)
        self._command_name = "request_suggestions"
        self._query = query_text

    @property
    def message(self) -> Dict[Text, Any]:
        return {"id": self._sender.id, "text": self._query}

    @staticmethod
    def from_message(
        sender: Agent, extracted_from_text: Optional[Text] = None, **kwargs
    ) -> Optional["Command"]:
        return RequestSuggestionsCommand(
            sender=sender, query_text=(extracted_from_text or "")
        )

    @property
    def query(self) -> Text:
        return self._query

    @property
    def event(self) -> Optional[Dict[Text, Any]]:
        return {
            "Agent": self._sender.id,
            "Action": self._command_name,
            "Text": self._query,
            "UnixTime": int(time.time()),
        }


class SupplySuggestionsCommand(BackendCommand):
    def __init__(self, recipient: Agent, suggestions: List[Tuple[Text, Text]]) -> None:
        super(SupplySuggestionsCommand, self).__init__()
        self._command_name = all_constants()["back_to_front"][
            "command_supply_suggestions"
        ]
        self._recipient = recipient
        self._suggestions = suggestions

    @property
    def message(self) -> Dict[Text, Any]:
        return {
            "id": self._recipient.id,
            "text": "",
            "command": self._command_name + str([text for intent, text in self._suggestions]),
            "intents": [intent for intent, text in self._suggestions]
        }

    @staticmethod
    def from_message(
        sender: Agent, suggestions: Optional[List[Tuple[Text, Text]]] = None, **kwargs,
    ) -> Optional["Command"]:
        return SupplySuggestionsCommand(recipient=sender, suggestions=suggestions)


class PickSuggestionCommand(WizardCommand):
    def __init__(self, sender: Agent, chosen_text: Text) -> None:
        super(PickSuggestionCommand, self).__init__(sender)
        self._command_name = "pick_suggestion"
        self._text = chosen_text

    def text_matches(self, text: Text) -> bool:
        return text == self._text

    @property
    def message(self) -> Dict[Text, Any]:
        return {"id": self._sender.id, "text": self._text}

    @staticmethod
    def from_message(
        sender: Agent, extracted_from_text: Optional[Text] = None, **kwargs
    ) -> Optional["Command"]:
        if not extracted_from_text:
            raise ValueError(f"Chosen message is empty")
        return PickSuggestionCommand(sender=sender, chosen_text=extracted_from_text)

    @property
    def event(self) -> Optional[Dict[Text, Any]]:
        return {
            "Agent": self._sender.id,
            "Action": self._command_name,
            "Text": self._text,
            "UnixTime": int(time.time()),
        }


def command_from_message(
    message: Optional[Dict[Text, Any]], sender: Optional[Agent]
) -> Optional[Command]:
    if not message:
        return None

    if is_disconnected(message):
        # if isinstance(sender, MTurkAgent):
        #     sender.reject_work(reason="It looks like you disconnected without finishing the task.")
        raise RuntimeError("Disconnected")

    text = message.get("text", "")

    constants = all_constants()
    prefixes = {
        constants["front_to_back"]["query_prefix"]: QueryCommand,
        constants["front_to_back"]["complete_prefix"]: DialogueCompletedCommand,
        constants["front_to_back"]["done_prefix"]: TaskDoneCommand,
        constants["front_to_back"]["select_kb_entry_prefix"]: SelectPrimaryCommand,
        constants["front_to_back"][
            "select_reference_kb_entry_prefix"
        ]: SelectSecondaryCommand,
        constants["front_to_back"][
            "request_suggestions_prefix"
        ]: RequestSuggestionsCommand,
        constants["front_to_back"]["pick_suggestion_prefix"]: PickSuggestionCommand,
        constants["front_to_back"]["query_prefix"]: QueryCommand,
        "<guide>": GuideCommand,
        "<silent>": SilentCommand,
        constants["front_to_back"]["select_topic_prefix"]: SelectTopicCommand,
    }

    # Add information extracted from the `text` property (magic strings)
    command = UtterCommand
    _message = message
    for _prefix, _command in prefixes.items():
        if text.startswith(_prefix):
            command = _command
            _message["extracted_from_text"] = text[len(_prefix) :]
            break

    return command.from_message(sender, **_message)
