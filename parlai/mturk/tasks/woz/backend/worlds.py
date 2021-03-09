#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import os
import time
from typing import Text, List, Dict, Any, Optional, Tuple

from parlai import PROJECT_PATH
from parlai.core.agents import Agent
from parlai.core.opt import Opt
from parlai.mturk.core import shared_utils, mturk_utils
from parlai.mturk.core.agents import (
    MTURK_DISCONNECT_MESSAGE,
    RETURN_MESSAGE,
    TIMEOUT_MESSAGE,
    MTurkAgent,
)
from parlai.mturk.core.shared_utils import print_and_log
from parlai.mturk.core.worlds import MTurkOnboardWorld, MTurkTaskWorld
import threading

import parlai.mturk.tasks.woz.echo as echo
from parlai.mturk.tasks.woz.backend.commands import (
    command_from_message,
    all_constants,
    UtterCommand,
    DialogueCompletedCommand,
    TaskDoneCommand,
    ReviewCommand,
    QueryCommand,
    SelectPrimaryCommand,
    SelectSecondaryCommand,
    RequestSuggestionsCommand,
    PickSuggestionCommand,
    SupplySuggestionsCommand,
    SetupCommand,
    GuideCommand,
    SilentCommand,
    SelectTopicCommand,
)
from parlai.mturk.tasks.woz.backend.suggestions import WizardSuggestion, CUSTOM_INTENT
from parlai.mturk.tasks.woz.backend.workers import (
    WorkerDatabase,
    TASK_LEVEL_SINGLE_HAPPY,
)
from parlai.mturk.tasks.woz.task_config import TUTORIAL_URL


TURN_TIME_LIMIT = (
    18 * 60
)  # Maximum allowed time in seconds for one turn (user or wizard)


def is_disconnected(act):
    return 'text' in act and act['text'] in [
        MTURK_DISCONNECT_MESSAGE,
        RETURN_MESSAGE,
        TIMEOUT_MESSAGE,
    ]


def send_mturk_message(text: Text, recipient: Agent) -> None:
    message = {"id": all_constants()["agent_ids"]["system_id"], "text": text}
    recipient.observe(message)


def send_setup_command(
    task_description: Text,
    completion_requirements: List[Text],
    form_description: Dict[Text, Any],
    completion_questions: List[Text],
    recipient: Agent,
):
    recipient.observe(
        {
            "id": recipient.id,
            "text": "",
            "command": all_constants()["back_to_front"]["command_setup"],
            "task_description": task_description,
            "completion_requirements": completion_requirements,
            "completion_questions": completion_questions,
            "form_description": form_description,
        }
    )


class WizardOnboardingWorld(MTurkOnboardWorld):
    """
    Example onboarding world.

    Sends a message from the world to the worker and then exits as complete after the
    worker uses the interface
    """

    def __init__(self, opt: Opt, mturk_agent: Agent, worker_id: Text) -> None:
        super(WizardOnboardingWorld, self).__init__(opt, mturk_agent=mturk_agent)
        self._scenario = opt.get("scenario")
        self.opt = opt
        assert self._scenario
        self._worker_id = worker_id

    def parley(self):
        self.mturk_agent.observe(
            GuideCommand(
                f"Hello {self._worker_id}. Every time you do this task you will be randomly assigned one of two roles: "
                f"an AI assistant, or a user. This time, you'll play the AI assistant. When you type 'ready' and "
                f"send a message, we will pair you up with another worker who plays the AI assistant. "
                f"Note that this might take a few minutes."
            ).message
        )
        self.mturk_agent.act()

        self.mturk_agent.passed_onboarding = True
        send_mturk_message(
            "Please wait for the user and join the conversation...", self.mturk_agent,
        )
        self.episodeDone = True

    def get_model_agent(self):
        return self.mturk_agent

    def get_task_agent(self):
        return self.mturk_agent


class UserOnboardingWorld(MTurkOnboardWorld):
    """
    Example onboarding world.

    Sends a message from the world to the worker and then exits as complete after the
    worker uses the interface
    """

    def __init__(self, opt: Opt, mturk_agent: Agent, worker_id: Text) -> None:
        super(UserOnboardingWorld, self).__init__(opt, mturk_agent=mturk_agent)
        self._scenario = opt.get("scenario")
        self._worker_id = worker_id
        assert self._scenario

    def parley(self) -> None:
        setup = SetupCommand(scenario="intro", role="User")
        self.mturk_agent.observe(setup.message)
        self.mturk_agent.observe(
            GuideCommand(
                f"Hello {self._worker_id}. Every time you do this task you will be randomly assigned one of two roles: "
                f"an AI assistant, or a user. This time, you'll play the user. When you type 'ready' and "
                f"send a message, we will pair you up with another worker who plays the AI assistant. "
                f"Note that this might take a few minutes."
            ).message
        )
        self.mturk_agent.act()
        self.mturk_agent.passed_onboarding = True
        self.mturk_agent.observe(
            GuideCommand(
                "Please wait for the virtual assistant to join the conversation..."
            ).message
        ),
        self.episodeDone = True

    def get_model_agent(self):
        return self.mturk_agent

    def get_task_agent(self):
        return self.mturk_agent


class RoleOnboardWorld(MTurkOnboardWorld):
    """
    A world that provides the appropriate instructions during onboarding.
    """

    def __init__(self, opt, mturk_agent, role):
        self.task_type = 'sandbox' if opt['is_sandbox'] else 'live'
        self.max_onboard_time = opt['max_onboard_time']
        self.role = role
        super().__init__(opt, mturk_agent)

    def parley(self):
        onboard_msg = {
            "id": "MTurk System",
            "text": f"Hello {self.mturk_agent.worker_id}. If you want to refresh your memory about this task, here is the tutorial video: {TUTORIAL_URL} . "
                    f"Please send any message to get paired with a co-worker (this might take some time).",
        }
        self.mturk_agent.observe(onboard_msg)
        act = self.mturk_agent.act(timeout=self.max_onboard_time)
        # timeout
        if act['episode_done'] or ('text' in act and act['text'] == TIMEOUT_MESSAGE):
            self.episodeDone = True
            return

        if 'text' not in act:
            control_msg = {'id': 'SYSTEM', 'text': "something is wrong"}
            self.mturk_agent.observe(control_msg)
            self.episodeDone = True


SETUP_STAGE = 0
DIALOGUE_STAGE = 1
EVALUATION_STAGE = 2
END_STAGE = 3


class WOZWorld(MTurkTaskWorld):
    """
    Wizard-of-Oz world.
    """

    def __init__(
        self,
        opt: Opt,
        scenario: Text,
        agents: List[MTurkAgent],
        observers: Optional[List[Agent]] = None,
    ) -> None:
        print_and_log(
            100,
            f"Creating new world for workers {[(w.id, w.worker_id) for w in agents]}",
            True,
        )
        super(WOZWorld, self).__init__(opt, mturk_agent=None)
        self._is_sandbox = opt["is_sandbox"] or False
        self.observers = observers or []
        self.knowledgebase = None
        self.user = None
        self.wizard = None

        for agent in agents:
            assert hasattr(agent, "id")
            if agent.id == "User":
                self.user = agent
            elif agent.id == "Wizard":
                self.wizard = agent
            elif agent.id == "KnowledgeBase":
                self.knowledgebase = agent

        # ToDo: Adjust as NLU module gets better
        self._scenario = scenario
        self._current_domain = (
            "ride" if self._scenario.startswith("book_ride") else None
        )
        print(f"Start domain/scenario: {self._current_domain} / {self._scenario}")

        assert self.user
        assert self.wizard
        assert self._scenario

        self._episode_done = False
        self._stage = SETUP_STAGE
        self._received_evaluations = 0
        self.events = []
        self._suggestion_module = None

        self.num_turns = 1

        self._primary_kb_item = None
        self._secondary_kb_item = None
        self._selected_api: Optional[Text] = None  # The api of the selected tab
        self._selected_kb_item_api: Optional[
            Text
        ] = None  # The api of the selected knowledge base item
        self._api_names: Optional[List[Text]] = None
        self._scenario_is_happy: bool = False

        self._user_task_description = None
        self._questions_to_user = None
        self._questions_to_wizard = None
        self._answers_by_user = None
        self._answers_by_wizard = None
        self._user_linear_guide = None

        self._wizard_task_description = None
        self._wizard_capabilities = None

        self._wizard_has_used_kb = False
        self._num_wizard_utterances = 0
        self._num_user_utterances = 0
        self._user_has_ended_dialogue = False
        self._wizard_has_ended_dialogue = False

    def parley(self):
        try:
            if self._stage == SETUP_STAGE:
                try:
                    wizard_setup_command = SetupCommand(scenario=self._scenario, role="Wizard")
                except FileNotFoundError as e:
                    print_and_log(100, f"ERROR: Missing scenario file: {e}", True)
                    self._scenario = "happy_trivia_v0"
                    wizard_setup_command = SetupCommand(scenario=self._scenario, role="Wizard")
                self._wizard_task_description = wizard_setup_command.task_description
                self._wizard_capabilities = wizard_setup_command.capabilities
                assert self._wizard_capabilities
                self._questions_to_wizard = wizard_setup_command.completion_questions
                self._api_names = wizard_setup_command.api_names
                self._selected_api = self._api_names[0]
                self._scenario_is_happy = wizard_setup_command.is_happy

                base_dir = os.path.join(PROJECT_PATH, "resources")
                self._suggestion_module = WizardSuggestion(
                    scenario_list=self._api_names, resources_dir=base_dir
                )

                self.wizard.observe(wizard_setup_command.message)

                user_setup_command = SetupCommand(scenario=self._scenario, role="User")
                self._questions_to_user = user_setup_command.completion_questions
                self._user_task_description = user_setup_command.task_description
                self._user_linear_guide = user_setup_command.user_linear_guide
                self.user.observe(user_setup_command.message)

                if self.overtime_bonus(preview=True) > 0.:
                    send_mturk_message(
                        f"This instruction set is particularly long, so if you complete it we'll pay a bonus of ${self.overtime_bonus(preview=True):.2f}. (For technical reasons, this automatic bonus will not work if you or your partner disconnects early.)",
                        self.user,
                    )
                    send_mturk_message(
                        f"This instruction set is particularly long, so if you complete it we'll pay a bonus of {self.overtime_bonus(preview=True):.2f}. (For technical reasons, this automatic bonus will not work if you or your partner disconnects early.)",
                        self.wizard,
                    )

                send_mturk_message(
                    f"Your task: {wizard_setup_command.message.get('task_description')} "
                    f"\n\nNote: It may happen that the auto-responses don't work and the only suggestion is your search query. In this case, please write a full sentence as a custom response.",
                    self.wizard,
                )

                self.tell_workers_to_start()
                self.num_turns = 0
                self._stage = DIALOGUE_STAGE
            elif self._stage == DIALOGUE_STAGE:
                self._parley_observers()
                if self.num_turns % 2 == 0:
                    self.num_turns += self._parley_dialogue_user()
                else:
                    self.num_turns += self._parley_dialogue_wizard_and_knowledgebase()
            elif self._stage == EVALUATION_STAGE:
                self._parley_evaluation(self.user)
                self._parley_evaluation(self.wizard)
                self._stage = END_STAGE
            elif self._stage == END_STAGE:
                if self._received_evaluations >= 2:
                    self._episode_done = True
        except RuntimeError as e:
            # Somebody disconnected
            print_and_log(100, f"Unexpected DISCONNECT: {e}", True)
            self._episode_done = True

    def _parley_observers(self) -> None:
        for observer in self.observers:
            observer.observe(self.events)
            message_to_user, message_to_wizard = observer.act()
            if message_to_user:
                self.user.observe(message_to_user)
            if message_to_wizard:
                self.wizard.observe(message_to_wizard)

    def _parley_dialogue_user(self) -> int:
        user_command = command_from_message(
            self.user.act(timeout=TURN_TIME_LIMIT), self.user
        )
        self.events.append(user_command.event)
        if isinstance(user_command, UtterCommand):
            self.wizard.observe(user_command.message)
            self._num_user_utterances += 1
            self.send_linear_user_guide_instruction()
            return 1
        elif isinstance(user_command, SilentCommand):
            return 1
        elif isinstance(user_command, DialogueCompletedCommand):
            self.wizard.observe(ReviewCommand(self.wizard).message)
            self.user.observe(ReviewCommand(self.user).message)
            self.user.observe(
                GuideCommand(
                    "Thank you for chatting. Now please review your conversation."
                ).message
            )
            self.wizard.observe(
                GuideCommand(
                    "The user thinks that the task is complete. Please review your conversation, click on 'confirm', and wait for the user."
                ).message
            )
            self._user_has_ended_dialogue = True
            self._stage = EVALUATION_STAGE
            return 1
        else:
            print_and_log(
                100,
                f"Command {type(user_command)} not allowed for User in dialogue stage: {user_command.message}",
                True,
            )

    def _parley_dialogue_wizard_and_knowledgebase(self) -> int:
        wizard_command = command_from_message(
            self.wizard.act(timeout=TURN_TIME_LIMIT), self.wizard
        )
        self.store_wizard_event(wizard_command)

        if isinstance(wizard_command, UtterCommand):
            self.user.observe(wizard_command.message)
            self._num_wizard_utterances += 1
            return 1
        elif isinstance(wizard_command, SilentCommand):
            return 1
        elif isinstance(wizard_command, QueryCommand):
            self._wizard_has_used_kb = True
            self.knowledgebase.observe(wizard_command)
            kb_message = self.knowledgebase.act()
            self._primary_kb_item = kb_message.get("example_item")
            self._selected_kb_item_api = (
                None
                if not self._primary_kb_item
                else self._primary_kb_item.get("api_name")
            )
            self._secondary_kb_item = None
            self.events.append(
                {
                    "Agent": "KnowledgeBase",
                    "Item": kb_message.get("example_item"),
                    "TotalItems": kb_message.get("num_items", 0),
                    "Topic": kb_message.get("api_name"),
                }
            )
            self.wizard.observe(kb_message)
            return 0
        elif isinstance(wizard_command, DialogueCompletedCommand):
            self._end_dialogue_by_wizard()
            return 1
        elif isinstance(wizard_command, SelectPrimaryCommand):
            self._primary_kb_item = wizard_command.item
            self._selected_kb_item_api = wizard_command.item.get("api_name")
            self._secondary_kb_item = None
            return 0
        elif isinstance(wizard_command, SelectSecondaryCommand):
            self._secondary_kb_item = wizard_command.item
            return 0
        elif isinstance(wizard_command, SelectTopicCommand):
            self._selected_api = self._api_names[int(wizard_command.topic)]
            return 0
        elif isinstance(wizard_command, RequestSuggestionsCommand):
            # Prevent wizards from copy/pasting entire KB item
            if "\t" in wizard_command.query:
                send_mturk_message(
                    "Please do not just copy/paste the knowledge base item.",
                    self.wizard,
                )
                return 0

            api_names = [self._selected_api]
            if self._selected_kb_item_api:
                api_names.append(self._selected_kb_item_api)
            else:
                api_names.append(self._selected_api)

            # Get suggestions from Rasa NLU server
            (
                suggestions,
                possibly_wrong_item_selected,
            ) = self._suggestion_module.get_suggestions(
                wizard_utterance=wizard_command.query,
                primary_kb_item=self._primary_kb_item,
                api_names=api_names,
            )
            # Warn if response template of top-ranked intent could not be filled by selected KB item
            if possibly_wrong_item_selected:
                send_mturk_message(
                    "Some suggestions won't show. Did you select the knowledge base item(s) that you are describing?",
                    self.wizard,
                )
            # Return suggested responses to front end
            self.wizard.observe(
                SupplySuggestionsCommand(self.wizard, suggestions).message
            )
            self._recent_suggestions = suggestions
            return 0
        elif isinstance(wizard_command, PickSuggestionCommand):
            self.wizard.observe(wizard_command.message)
            self.user.observe(wizard_command.message)
            self._num_wizard_utterances += 1
            # if "goodbye" in wizard_command.message.get("text", "").lower():
            #     self._end_dialogue_by_wizard()
            return 1
        else:
            print_and_log(
                100,
                f"Command {type(wizard_command)} not allowed for Wizard in dialogue stage: {wizard_command.message}",
                True,
            )

    def _parley_evaluation(self, agent) -> None:

        if not isinstance(agent, MTurkAgent):
            self._received_evaluations += 1
            return

        while True:
            command = command_from_message(
                agent.act(timeout=TURN_TIME_LIMIT, blocking=False), agent
            )

            if isinstance(command, UtterCommand):
                agent.observe(
                    GuideCommand(
                        "Thank you for your feedback! Please also complete the form on the left."
                    ).message
                )
            elif isinstance(command, TaskDoneCommand):
                if agent.id == "User":
                    self._answers_by_user = command.answers
                else:
                    self._answers_by_wizard = command.answers
                agent.observe(
                    GuideCommand(
                        "Thank you for evaluating! Goodbye. (You may have to wait for your partner to confirm.)"
                    ).message
                )
                self._received_evaluations += 1
                return
            elif command is None:
                # Happens when `agent.act()` returns `None` (can happen since `blocking=False`)
                time.sleep(shared_utils.THREAD_SHORT_SLEEP)
            else:
                print_and_log(
                    100,
                    f"Command {type(command)} not allowed for {agent.id} in evaluation stage: {command.message}",
                    True,
                )

    def _end_dialogue_by_wizard(self):
        self.wizard.observe(ReviewCommand(self.wizard).message)
        self.user.observe(ReviewCommand(self.user).message)
        self.wizard.observe(
            GuideCommand(
                "Thank you for chatting. Now please review your conversation."
            ).message
        )
        self.user.observe(
            GuideCommand(
                "The assistant thinks that the task is complete. Please review your conversation, click on 'confirm', and wait for the assistant."
            ).message
        )
        self._wizard_has_ended_dialogue = True
        self._stage = EVALUATION_STAGE

    def send_linear_user_guide_instruction(self) -> None:
        if not self._user_linear_guide or self._num_user_utterances >= len(
            self._user_linear_guide
        ):
            return

        instruction = self._user_linear_guide[self._num_user_utterances]
        if instruction:
            current_instruction_number = (
                len(
                    [
                        i
                        for i in self._user_linear_guide[: self._num_user_utterances]
                        if i is not None
                    ]
                )
                + 1
            )
            total_instruction_number = len(
                [i for i in self._user_linear_guide if i is not None]
            )
            instruction += f" [instruction {current_instruction_number} of {total_instruction_number}]"
            self.events.append(
                {
                    "Agent": "UserGuide",
                    "Action": "instruct",
                    "Text": instruction,
                    "UnixTime": int(time.time()),
                }
            )
            self.user.observe(GuideCommand(instruction).message)

    def store_wizard_event(self, command):
        _event = command.event

        # Add intent (hack)
        if isinstance(command, PickSuggestionCommand) and self._recent_suggestions:
            _event["Intent"] = CUSTOM_INTENT
            _event["IntentOptions"] = [
                intent for intent, text in self._recent_suggestions
            ]
            for intent, text in self._recent_suggestions:
                if command.text_matches(text):
                    _event["Intent"] = intent

        _event["PrimaryItem"] = self._primary_kb_item
        _event["SecondaryItem"] = self._secondary_kb_item

        self.events.append(_event)

    @echo.echo_in(
        output=echo.log_write, prolog={"command": None, "recipient": (lambda a: a.id)}
    )
    def send_command(self, command: Text, recipient: Agent) -> None:
        self.events.append(
            {"type": "WorldCommand", "command": command, "recipient": recipient.id,}
        )
        message = {
            "id": recipient.id,
            "text": "",
            "command": command,
        }
        recipient.observe(message)

    def tell_workers_to_start(self):
        if self._user_linear_guide:
            self.send_linear_user_guide_instruction()
        else:
            self.user.observe(
                GuideCommand("The assistant is ready. Go ahead, say hello!").message
            )
        self.wizard.observe(
            GuideCommand(
                "A user has joined the chat. Please wait for him/her to start the conversation."
            ).message
        )

    def episode_done(self):
        return self._episode_done

    def shutdown(self):
        # Parallel shutdown of agents
        def shutdown_agent(agent):
            try:
                agent.shutdown(timeout=None)
            except Exception:
                agent.shutdown()  # not MTurkAgent

        threads = []
        agents = [self.user, self.wizard, self.knowledgebase]
        mturk_agents = [agent for agent in agents if isinstance(agent, MTurkAgent)]
        for agent in mturk_agents:
            t = threading.Thread(target=shutdown_agent, args=(agent,))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()

    def review_work(self):
        # Can review the work here to accept or reject it
        if self.review_user():
            print(
                f"User {self.user.worker_id}'s work was approved (HIT {self.user.hit_id})"
            )
        else:
            print(
                f"User {self.user.worker_id}'s work remains unrated (HIT {self.user.hit_id})"
            )

        if self.review_wizard():
            print(
                f"Wizard {self.wizard.worker_id}'s work was approved (HIT {self.wizard.hit_id})"
            )
        else:
            print(
                f"Wizard {self.wizard.worker_id}'s work remains unrated (HIT {self.wizard.hit_id})"
            )

    def overtime_bonus(self, preview: bool = False) -> float:
        if self._user_linear_guide and len(self._user_linear_guide) > 10 and (self._num_user_utterances >= len(self._user_linear_guide) or preview):
            minutes_per_turn = 0.6
            hourly_salary = 10.00
            bonus = (len(self._user_linear_guide) - 10) * minutes_per_turn * hourly_salary / 60.
            return round(bonus, ndigits=2)
        else:
            return 0.00

    def review_user(self) -> bool:
        if not self._answers_by_user:
            return False

        bonus = self.overtime_bonus()
        if bonus > 0:
            print_and_log(100, f"Paying overtime bonus of ${bonus} to {self.user.worker_id}.", True)
            self.user.pay_bonus(bonus, reason="This instruction set was particularly long, so we pay you overtime.")

        self.user.approve_work()
        return True

    def review_wizard(self) -> bool:
        if not self._answers_by_wizard:
            return False

        if not self._wizard_has_used_kb:
            return False

        bonus = self.overtime_bonus()
        if bonus > 0:
            print_and_log(100, f"Paying overtime bonus of ${bonus} to {self.wizard.worker_id}.", True)
            self.wizard.pay_bonus(bonus, reason="This instruction set was particularly long, so we pay you overtime.")

        self.wizard.approve_work()
        return True

    def get_custom_task_data(self):
        # brings important data together for the task, to later be used for
        # creating the data set. If data requires pickling, put it in a field
        # called 'needs-pickle'.
        user_questionaire_data = [
            {"Question": self._questions_to_user[i], "Answer": self._answers_by_user[i]}
            for i in range(
                min(len(self._questions_to_user), len(self._answers_by_user))
            )
        ] if self._questions_to_user and self._answers_by_user else []
        wizard_questionaire_data = [
            {
                "Question": self._questions_to_wizard[i],
                "Answer": self._answers_by_wizard[i],
            }
            for i in range(
                min(len(self._questions_to_wizard), len(self._answers_by_wizard))
            )
        ] if self._questions_to_wizard and self._answers_by_wizard else []
        return {
            "FORMAT-VERSION": 5,
            "Scenario": {
                "Domains": sorted(
                    list({c.get("Domain") for c in self._wizard_capabilities})
                ),
                "UserTask": self._user_task_description,
                "WizardTask": self._wizard_task_description,
                "WizardCapabilities": self._wizard_capabilities,
                "Happy": self._scenario_is_happy
            },
            "Events": self.events,
            "WizardWorkerID": (
                self.wizard.worker_id if hasattr(self.wizard, "worker_id") else None
            ),
            "WizardHITID": (
                self.wizard.hit_id if hasattr(self.wizard, "hit_id") else None
            ),
            "WizardAssignmentID": (
                self.wizard.assignment_id
                if hasattr(self.wizard, "assignment_id")
                else None
            ),
            "UserWorkerID": (
                self.user.worker_id if hasattr(self.user, "worker_id") else None
            ),
            "UserHITID": (self.user.hit_id if hasattr(self.user, "hit_id") else None),
            "UserAssignmentID": (
                self.user.assignment_id if hasattr(self.user, "assignment_id") else None
            ),
            "UserQuestionaire": user_questionaire_data,
            "WizardQuestionaire": wizard_questionaire_data,
        }

    def get_model_agent(self):
        return self.wizard  # ToDo: Don't know if this is correct

    def get_task_agent(self):
        return self.user

    def send_suggestions(self, suggestions: List[Text], wizard_agent):
        self.send_command(
            all_constants()["back_to_front"]["command_supply_suggestions"]
            + str(suggestions),
            wizard_agent,
        )

    @staticmethod
    def add_cmdline_args(parser):
        parser = parser.add_argument_group('WOZWorld arguments')
        parser.add_argument(
            "--scenario", type=str, default="book_ride_tutorial", help="Scenario name",
        )
        parser.add_argument(
            "--scenario_list", type=str, default="all_scenarios", help="Scenario list",
        )


# class WOZWizardTutorialWorld(MTurkTaskWorld):
#     def __init__(
#         self,
#         opt,
#         agents,
#         observers: Optional[List[Agent]] = None,
#         qualification_on_success: Optional[Text] = None,
#     ) -> None:
#         super(WOZWizardTutorialWorld, self).__init__(opt, mturk_agent=None)
#         self.opt = opt
#         self.observers = observers or []
#         self.knowledgebase = None
#         self.tutor = None
#         self.wizard = None
#         for agent in agents:
#             if agent.demo_role == "User":
#                 self.tutor = agent
#             elif agent.demo_role == "Wizard":
#                 self.wizard = agent
#             elif agent.demo_role == "KnowledgeBase":
#                 self.knowledgebase = agent
#
#         self._scenario = opt.get("scenario")
#         self._qualification_on_success = qualification_on_success
#
#         assert self.tutor
#         assert self.wizard
#         assert self._scenario
#
#         self._episode_done = False
#         self._stage = SETUP_STAGE
#         self._received_evaluations = 0
#         self.events = []
#
#         self.num_turns = 1
#
#         self._primary_kb_item = None
#         self._secondary_kb_item = None
#
#     def parley(self):
#         if self._stage == SETUP_STAGE:
#             self.wizard.observe(
#                 SetupCommand(scenario=self._scenario, role="Wizard").message
#             )
#             self.num_turns = 0
#             self._stage = DIALOGUE_STAGE
#         elif self._stage == DIALOGUE_STAGE:
#             if self.num_turns % 2 == 0:
#                 self.num_turns += self._parley_tutor()
#             else:
#                 self.num_turns += self._parley_wizard()
#         elif self._stage == EVALUATION_STAGE:
#             if not self.tutor.worker_succeeded:
#                 self.block_loop()
#             self._stage = END_STAGE
#         elif self._stage == END_STAGE:
#             self._episode_done = True
#
#     def _parley_tutor(self) -> int:
#         tutor_command = command_from_message(self.tutor.act(), self.tutor)
#         self.store_tutor_event(tutor_command.event)
#
#         if isinstance(tutor_command, DialogueCompletedCommand):
#             self._stage = EVALUATION_STAGE
#             return 1
#         elif isinstance(tutor_command, SilentCommand):
#             return 1
#         else:
#             self.wizard.observe(tutor_command.message)
#             return 0
#
#     def _parley_wizard(self) -> int:
#         wizard_command = command_from_message(self.wizard.act(), self.wizard)
#         self.store_wizard_event(wizard_command.event)
#
#         if isinstance(wizard_command, UtterCommand):
#             return 1
#         elif isinstance(wizard_command, SilentCommand):
#             return 1
#         elif isinstance(wizard_command, QueryCommand):
#             self.knowledgebase.observe(wizard_command)
#             kb_message = self.knowledgebase.act()
#             self._primary_kb_item = kb_message.get("example_item")
#             self._secondary_kb_item = None
#             self.events.append(
#                 {
#                     "Agent": "KnowledgeBase",
#                     "Item": kb_message.get("example_item"),
#                     "TotalItems": kb_message.get("num_items", 0),
#                     "Topic": kb_message.get("api_name"),
#                 }
#             )
#             self.wizard.observe(kb_message)
#             return 1
#         elif isinstance(wizard_command, DialogueCompletedCommand):
#             send_mturk_message(
#                 "You cannot use this functionality during the tutorial.", self.wizard
#             )
#             return 0
#         elif isinstance(wizard_command, SelectPrimaryCommand):
#             self._primary_kb_item = wizard_command.item
#             self._secondary_kb_item = None
#             return 0
#         elif isinstance(wizard_command, SelectSecondaryCommand):
#             self._secondary_kb_item = wizard_command.item
#             return 0
#         elif isinstance(wizard_command, RequestSuggestionsCommand):
#             suggestions = ["message 1", "message 2"]
#             self.wizard.observe(
#                 SupplySuggestionsCommand(self.wizard, suggestions).message
#             )
#             return 0
#         elif isinstance(wizard_command, PickSuggestionCommand):
#             return 1
#         else:
#             print_and_log(
#                 45,
#                 f"Command {type(wizard_command)} not allowed for Wizard in evaluation stage: {wizard_command.message}",
#                 True,
#             )
#
#     def block_loop(self) -> None:
#         print(f"Worker {self.wizard.worker_id} failed wizard's tutorial.")
#         send_mturk_message(
#             "Sorry, you've exceeded the maximum amount of tries to take the "
#             "correct actions, and thus we "
#             "don't believe you can complete the task correctly. Please return "
#             "the HIT.",
#             self.wizard,
#         )
#         self.wizard.mturk_manager.soft_block_worker(self.wizard.worker_id)
#         message = self.wizard.act()
#         while not is_disconnected(message):
#             send_mturk_message("Please return the HIT.", self.wizard)
#             message = self.wizard.act()
#
#     def store_wizard_event(self, event):
#         _event = event
#         _event["PrimaryItem"] = self._primary_kb_item
#         _event["SecondaryItem"] = self._secondary_kb_item
#         self.tutor.observe(_event)
#         self.events.append(_event)
#
#     def store_tutor_event(self, event):
#         self.events.append(event)
#
#     def episode_done(self):
#         return self._episode_done
#
#     def shutdown(self):
#         # Parallel shutdown of agents
#         def shutdown_agent(agent):
#             try:
#                 agent.shutdown(timeout=None)
#             except Exception:
#                 agent.shutdown()  # not MTurkAgent
#
#         threads = []
#         agents = [self.tutor, self.wizard, self.knowledgebase]
#         mturk_agents = [agent for agent in agents if isinstance(agent, MTurkAgent)]
#         for agent in mturk_agents:
#             t = threading.Thread(target=shutdown_agent, args=(agent,))
#             t.start()
#             threads.append(t)
#         for t in threads:
#             t.join()
#
#     def review_work(self):
#         # Can review the work here to accept or reject it
#         # self.mturk_agent.approve_work()
#         # self.mturk_agent.reject_work()
#         # self.mturk_agent.pay_bonus(1000) # Pay $1000 as bonus
#         # self.mturk_agent.block_worker() # Block this worker from future HITs
#         if self.tutor.worker_succeeded:
#             if self._qualification_on_success:
#                 mturk_utils.give_worker_qualification(
#                     self.wizard.worker_id,
#                     self._qualification_on_success,
#                     is_sandbox=self.opt["is_sandbox"],
#                 )
#             self.wizard.approve_work()
#         else:
#             self.wizard.block_worker(reason="Failed wizard tutorial of 2020-03-20")
#
#     def get_custom_task_data(self):
#         # brings important data together for the task, to later be used for
#         # creating the dataset. If data requires pickling, put it in a field
#         # called 'needs-pickle'.
#         return {"Events": self.events, "WizardWorkerID": self.wizard.worker_id}
#
#     def get_model_agent(self):
#         return self.wizard
#
#     def get_task_agent(self):
#         return self.tutor
#
#     @staticmethod
#     def add_cmdline_args(parser):
#         pass
