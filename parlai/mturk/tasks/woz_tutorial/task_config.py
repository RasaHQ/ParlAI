#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from typing import Dict, Any

TUTORIAL_URL = "https://youtu.be/L7QpscLPTFM"

task_config: Dict[str, Any] = {}


task_config['frontend_version'] = 1

"""A short and descriptive title about the kind of task the HIT contains.
On the Amazon Mechanical Turk web site, the HIT title appears in search results,
and everywhere the HIT is mentioned.
"""
task_config['hit_title'] = 'AI Dialogues - Stage I'


"""A description includes detailed information about the kind of task the HIT contains.
On the Amazon Mechanical Turk web site, the HIT description appears in the expanded
view of search results, and in the HIT and assignment screens.
"""
task_config['hit_description'] = 'Go through the onboarding process of the AI Dialogue Tasks. In the latter, you have a chat with a partner and play either a user or an AI assistant.'


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
This task is Stage 1 of the AI Dialogue tasks and should prepare you for the remaining 3 stages.
Higher stages offer greater payments, but you cannot enter the other stages without giving the correct answers in this test.
The test is about the contents of this video: {TUTORIAL_URL}.
You fail the test if you need more than 5 hints.
Your submission will be REJECTED if you need more than 8 hints.

Note: The number of HITs for the various stages is limited and not all the stages will be available at all times. 
'''
