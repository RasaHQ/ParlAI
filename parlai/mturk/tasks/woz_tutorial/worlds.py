#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
from typing import Optional, Text, List

from parlai.mturk.core import mturk_utils
from parlai.mturk.core.agents import MTURK_DISCONNECT_MESSAGE, RETURN_MESSAGE, TIMEOUT_MESSAGE
from parlai.mturk.core.worlds import MTurkTaskWorld
from parlai.mturk.tasks.woz_tutorial.task_config import TUTORIAL_URL


class TutorialFailedError(ValueError):
    pass


class GuideCommand:

    def __init__(self, text):
        self._text = text

    @property
    def message(self):
        return {"id": "MTurk System", "text": self._text}


def is_disconnected(act):
    return 'text' in act and act['text'] in [
        MTURK_DISCONNECT_MESSAGE,
        RETURN_MESSAGE,
        TIMEOUT_MESSAGE,
    ]


class TutorialWorld1(MTurkTaskWorld):
    """
    Tutorial I
    """

    def __init__(self, opt, mturk_agent, qualification_id) -> None:
        super(TutorialWorld1, self).__init__(opt, mturk_agent=mturk_agent)
        self.opt = opt
        self.qualification_id = qualification_id
        self.hints_needed = 0
        self._worker_id = mturk_agent.worker_id
        self._assignment_id = mturk_agent.assignment_id

    def parley(self) -> None:
        self.mturk_agent.observe(
            GuideCommand(
                f"Hello {self.mturk_agent.worker_id}. In this task you have to answer a multiple-choice "
                f"test about a video tutorial. If you successfully answer the questions, you "
                f"earn a qualification to participate in the dialogue tasks that are described "
                f"in the video. Send any text to continue."
            ).message
        )
        self.hints_needed = 0
        try:
            while not self.check_response():
                pass
            self.mturk_agent.observe(
                GuideCommand(
                    f"If you are not interested in earning the qualification for the AI Dialogue "
                    f"tasks, please return the HIT immediately. Otherwise, please watch the following "
                    f"video tutorial carefully and be prepared to answer questions: {TUTORIAL_URL} . "
                    f"Send any text when you're ready to answer questions. "
                ).message
            )
            while not self.check_response():
                pass
            self.mturk_agent.observe(
                GuideCommand(
                    f"Ok, let's start the quiz. Please answer by sending the number of the answer "
                    f"that you think is most correct. "
                ).message
            )
            self.hints_needed += self.ask(
                question="As the user, when can you end the task?",
                choices=[
                    "I cannot. Only the assistant can do this.",
                    "As soon as the 'Click here when you've accomplished your task(s)' button is enabled.",
                    "When I have followed all the instructions, including those on the left panel and those that are given by the MTurk System Bot.",
                ],
                answer=3,
                hints=[
                    "No... To answer you should send either '1', '2', or '3' (without the quotes).",
                    "No... Think about the name of that button in the second answer. Try again...",
                    "Not quite. One more try...",
                ],
            )
            self.hints_needed += self.ask(
                question="As the user, if you forget to follow an instruction from the MTurk System bot, what should you do?",
                choices=[
                    "Forget about the instruction since it is outdated.",
                    "Follow the instruction once I realise that I've overlooked it.",
                    "Tell the AI Assistant that I've missed an instruction.",
                ],
                answer=2,
                hints=[
                    "No... Remember that we want the user to push for a complex dialogue.",
                    "Still not right. Try again.",
                    "Not quite. One more try...",
                ],
            )
            self.hints_needed += self.ask(
                question="As the user, what should you do if you need some information that was not given in the task instructions?",
                choices=[
                    "I can just make something up.",
                    "Give up.",
                    "I must avoid answering any questions about the missing information.",
                ],
                answer=1,
                hints=[
                    "No... Remember that we want the user to push for a complex dialogue.",
                    "Still not right. Try again.",
                    "Not quite. One more try...",
                ],
            )
            self.hints_needed += self.ask(
                question="As the assistant, what should you do if the user begins a dialogue, but doesn't say what he/she wants?",
                choices=[
                    "I tell the user what task I can help her with",
                    "I should just greet the user",
                    "I should say that I cannot understand what he/she's saying",
                ],
                answer=2,
                hints=[
                    "Not quite. Try again :)",
                    "Not quite. Try again...",
                    "No. One more try...",
                ],
            )
            self.hints_needed += self.ask(
                question="For the assistant, what of these things is the MOST important?",
                choices=[
                    "Being helpful to the user",
                    "Following the flow chart of the current task whenever possible",
                    "Making the conversation as short as possible",
                    "Making the conversation as long as possible",
                ],
                answer=2,
                hints=[
                    "No. The length of the conversation is not as important to us as its quality. Try again.",
                    "No. The correct answer starts with 'Following the flow chart...'. Try one last time...",
                ],
            )
            self.hints_needed += self.ask(
                question="What does the request-optional box mean in the flow chart?",
                choices=[
                    "It represents information that I can use, but that is not absolutely required.",
                    "I can ignore this box if it doesn't make sense here",
                ],
                answer=1,
                hints=[
                    "No. Try again.",
                    "No. Try again.",
                ],
            )
            self.hints_needed += self.ask(
                question="As an assistant, when should you use one of the suggested responses?",
                choices=[
                    "Whenever possible - I only use custom responses if the situation is not accounted for in the flow chart",
                    "Only if they fit exactly what I want to say",
                ],
                answer=1,
                hints=[
                    "No. Try again.",
                    "No. Try again.",
                ],
            )
            self.hints_needed += self.ask(
                question="What does the \"request type\" form field mean?",
                choices=[
                    "It is there to distinguish between checking if a booking is available or actually performing the booking",
                    "It's about the type of person I am dealing with",
                    "The request type describes the topic that the user is referring to.",
                ],
                answer=1,
                hints=[
                    "No. Remember that there are Query (Check) and Query (Book) boxes in the flow chart.",
                    "No. Try again.",
                    "No. One more try...",
                ],
            )
            self.hints_needed += self.ask(
                question="How does the ideal user behave?",
                choices=[
                    "As a user, I should behave in a structured and consistent manner. Always friendly and concise.",
                    "As a user, I should make the dialogue more interesting and complicated (but follow instructions).",
                    "Just follow the instructions.",
                ],
                answer=2,
                hints=[
                    "No. Remember the end of the tutorial video.",
                    "No. Try again.",
                ],
            )
            self.hints_needed += self.ask(
                question="How does the ideal AI Assistant behave?",
                choices=[
                    "Just follow the instructions.",
                    "As an AI Assistant, I should make the dialogue more complex and be very creative - but follow the instructions.",
                    "As an AI Assistant, I should behave in a structured and consistent manner. Always friendly and concise.",
                ],
                answer=3,
                hints=[
                    "No. Remember the end of the tutorial video.",
                    "No. Try again.",
                ],
            )
            if self.hints_needed == 0:
                self.mturk_agent.observe(
                    GuideCommand(
                        f"Perfect Score! Well done! You got your qualification for the task "
                        f"'AI Dialogues - Stage II (Single Task Dialogues)' and a BONUS of $0.50."
                    ).message
                )
                self.mturk_agent.pay_bonus(0.50, reason="You didn't need any hints!")
                mturk_utils.give_worker_qualification(
                    self.mturk_agent.worker_id,
                    self.qualification_id,
                    value=self.hints_needed,
                    is_sandbox=self.opt['is_sandbox'],
                )
                self.mturk_agent.approve_work()
            elif self.hints_needed < 4:
                self.mturk_agent.observe(
                    GuideCommand(
                        f"Nicely done! You got your qualification for the task "
                        f"'AI Dialogues - Stage II (Single Task Dialogues)' and a BONUS of $0.25."
                    ).message
                )
                self.mturk_agent.pay_bonus(0.25, reason="You needed fewer than 4 hints.")
                mturk_utils.give_worker_qualification(
                    self.mturk_agent.worker_id,
                    self.qualification_id,
                    value=self.hints_needed,
                    is_sandbox=self.opt['is_sandbox'],
                )
                self.mturk_agent.approve_work()
            elif self.hints_needed < 6:
                self.mturk_agent.observe(
                    GuideCommand(
                        f"Done! You got your qualification for the task "
                        f"'AI Dialogues - Stage II (Single Task Dialogues)'."
                    ).message
                )
                mturk_utils.give_worker_qualification(
                    self.mturk_agent.worker_id,
                    self.qualification_id,
                    value=self.hints_needed,
                    is_sandbox=self.opt['is_sandbox'],
                )
                self.mturk_agent.approve_work()
            elif self.hints_needed < 9:
                self.mturk_agent.observe(
                    GuideCommand(
                        f"Sorry, but it took you too many hints to answer all the questions "
                        f"right, so we can't give you the qualification. Thanks for trying, though!"
                    ).message
                )
                self.mturk_agent.approve_work()
            else:
                self.mturk_agent.observe(
                    GuideCommand(
                        f"Sorry, but you've used too many hints. "
                    ).message
                )
                self.mturk_agent.reject_work(reason="You needed 9 or more hints to answer the questions.")
        except ConnectionError:
            self.episodeDone = True
            return
        except TutorialFailedError as e:
            self.mturk_agent.observe(
                GuideCommand(
                    f"Sorry, but the correct answer was choice {e}. Thank you for trying, though!"
                ).message
            )
            self.episodeDone = True
            return
        self.mturk_agent.observe(GuideCommand(f"All done!").message)

        self.episodeDone = True

    def check_response(self, expected_choice: Optional[int] = None) -> bool:
        message = self.mturk_agent.act()
        if is_disconnected(message):
            raise ConnectionError()
        else:
            if message.get("text", "1").isnumeric():
                choice = int(message.get("text", "1"))
            else:
                choice = 0
            return (
                expected_choice is None
                or choice == expected_choice
            )

    def ask(
        self,
        question: Text,
        choices: List[Text],
        answer: int,
        hints: Optional[List[Text]] = None,
    ) -> int:
        question_and_choices: Text = question + "\n"
        for i, choice in enumerate(choices):
            question_and_choices += f" {i+1}: {choice}\n"
        self.mturk_agent.observe(GuideCommand(question_and_choices).message)
        hints = hints or []
        hints_given = 0
        while not self.check_response(answer) and hints_given <= len(hints):
            if hints_given == len(hints):
                raise TutorialFailedError(answer)
            self.mturk_agent.observe(GuideCommand(hints[hints_given]).message)
            hints_given += 1
        return hints_given

    def review_work(self):
        # Can review the work here to accept or reject it
        pass

    def get_custom_task_data(self):
        return {
            "WorkerID": self._worker_id,
            "AssignmentID": self._assignment_id,
            "UsedHints": self.hints_needed
        }

    def get_model_agent(self):
        return self.mturk_agent

    def get_task_agent(self):
        return self.mturk_agent

    def episode_done(self):
        return self.episodeDone
