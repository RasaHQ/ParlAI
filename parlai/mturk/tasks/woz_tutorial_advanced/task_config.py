#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from typing import Dict, Any

TUTORIAL_URL = "https://youtu.be/dd0s2Sqox6g"

task_config: Dict[str, Any] = {}


task_config['frontend_version'] = 1

"""A short and descriptive title about the kind of task the HIT contains.
On the Amazon Mechanical Turk web site, the HIT title appears in search results,
and everywhere the HIT is mentioned.
"""
task_config['hit_title'] = 'AI Dialogues - Stage III'


"""A description includes detailed information about the kind of task the HIT contains.
On the Amazon Mechanical Turk web site, the HIT description appears in the expanded
view of search results, and in the HIT and assignment screens.
"""
task_config['hit_description'] = 'This is the advanced tutorial (with questionnaire) preparing you for Stage 4 (multi-task dialogues).'


"""One or more words or phrases that describe the HIT, separated by commas.
On MTurk website, these words are used in searches to find HITs.
"""
task_config['hit_keywords'] = 'chat, dialogue, onboarding'


"""A detailed task description that will be shown on the HIT task preview page
and on the left side of the chat page. Supports HTML formatting.
"""
task_config[
    'task_description'
] = f'''
This task is Stage III of the AI Dialogue tasks and should prepare you for Stage IV (multi-task dialogues).
Stage IV cannot be entered without giving the correct answers in this test.
The test is about the contents of this video: {TUTORIAL_URL}.
You fail the test if you need more than 5 hints.
Your submission will be REJECTED if you need more than 8 hints.

Note: The number of HITs for the various stages is limited and not all the stages will be available at all times. 
'''

task_config["assignment_duration_in_seconds"] = 240 * 60
