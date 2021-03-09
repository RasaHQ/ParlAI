#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

STAGE4 = True

if STAGE4:

    TUTORIAL_URL = "https://youtu.be/dd0s2Sqox6g"

    task_config = {}
    version = "v4"

    """A short and descriptive title about the kind of task the HIT contains.
    On the Amazon Mechanical Turk web site, the HIT title appears in search results,
    and everywhere the HIT is mentioned.
    """
    task_config['hit_title'] = f"AI Dialogues - Stage IV (Multi Task Dialogues) [{version}]"

    """A description includes detailed information about the kind of task the HIT contains.
    On the Amazon Mechanical Turk web site, the HIT description appears in the expanded
    view of search results, and in the HIT and assignment screens.
    """

    """One or more words or phrases that describe the HIT, separated by commas.
    On MTurk website, these words are used in searches to find HITs.
    """
    task_config['hit_keywords'] = 'chat, dialogue'

    """A detailed task description that will be shown on the HIT task preview page
    and on the left side of the chat page. Supports HTML formatting.
    """
    # with open("front_end.html", "r", encoding="utf-8") as file:
    #     task_config['task_description'] = file.read()
    task_config['frontend_version'] = 1

    intro_test = f"""To enter this task, you need a qualification from the 'AI Dialogues - Stage III' task.

    In this task you will take one of two roles: You could be a 'user' who wants to achieve some goal, 
    or, alternatively, you could take the role of an 'AI assistant' that helps the user achieve his/her goal.

    In case you want to re-watch the video tutorial: {TUTORIAL_URL}"""

    task_config['task_description'] = intro_test
    task_config['hit_description'] = intro_test
    task_config['chat_title'] = "AI Dialogues"

    # Allow four hours, because onboarding can take forever
    task_config["assignment_duration_in_seconds"] = 240 * 60


else:

    TUTORIAL_URL = "https://youtu.be/L7QpscLPTFM"

    task_config = {}
    version = "v5.1"

    """A short and descriptive title about the kind of task the HIT contains.
    On the Amazon Mechanical Turk web site, the HIT title appears in search results,
    and everywhere the HIT is mentioned.
    """
    task_config['hit_title'] = f"AI Dialogues - Stage II (Single Task Dialogues) [{version}]"


    """A description includes detailed information about the kind of task the HIT contains.
    On the Amazon Mechanical Turk web site, the HIT description appears in the expanded
    view of search results, and in the HIT and assignment screens.
    """


    """One or more words or phrases that describe the HIT, separated by commas.
    On MTurk website, these words are used in searches to find HITs.
    """
    task_config['hit_keywords'] = 'chat, dialogue'


    """A detailed task description that will be shown on the HIT task preview page
    and on the left side of the chat page. Supports HTML formatting.
    """
    # with open("front_end.html", "r", encoding="utf-8") as file:
    #     task_config['task_description'] = file.read()
    task_config['frontend_version'] = 1

    intro_test = f"""To enter this task, you need a qualification from the 'AI Dialogues - Stage I' task.
    
    In this task you will take one of two roles: You could be a 'user' who wants to achieve some goal, 
    or, alternatively, you could take the role of an 'AI assistant' that helps the user achieve his/her goal.
    
    In case you want to re-watch the video tutorial: {TUTORIAL_URL}"""

    task_config['task_description'] = intro_test
    task_config['hit_description'] = intro_test
    task_config['chat_title'] = "AI Dialogues"

    # Allow one hour, because onboarding can take forever
    task_config["assignment_duration_in_seconds"] = 120 * 60
