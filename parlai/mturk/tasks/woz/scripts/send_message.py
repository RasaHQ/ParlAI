#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import argparse
import parlai.mturk.core.mturk_utils as mturk_utils


def main():

    mturk_utils.setup_aws_credentials()
    client = mturk_utils.get_mturk_client(False)

    # client.notify_workers(
    #     Subject="AI Dialogues - Stage II [v2]",
    #     MessageText="Hi! \n\nThanks for going though Stage I of the AI Dialogues tasks! We just want to let you know that the Stage II task is currently running, and you can find it under the name 'AI Dialogues - Stage II (Single Task Dialogues) [v2]'. If it doesn't have a '[v2]' in the end, then its an older version where the server broke down, so that HIT won't work. Thus, look out for the '[v2]' :) \n\nBest wishes\nJohannes",
    #     WorkerIds  # ~~ Redacted ~~
    # )

    # workers = [  # ~~ Redacted ~~
    # workers = [  # ~~ Redacted ~~
    workers = []

    while workers:
        worker_batch = workers[:80]
        workers = workers[80:]
        print(f"Sending message to {worker_batch}")
        client.notify_workers(
            Subject="AI Dialogues - Stage IV Feedback",
            MessageText="Hello! "
                        ""
                        "Thank you for participating in the first Stage IV batch of our AI Dialogues. "
                        "We are still working out some details, but are already quite happy with the dialogues that we've seen. "
                        "However, we also noticed that nobody has done the long instruction sets (where we pay overtime bonus). "
                        "I am writing to you to get some feedback on why that might be. "
                        ""
                        "Is the risk of partner-disconnect to high? Or are long tasks generally not interesting? What can we do to improve? "
                        ""
                        "I am looking forward to hear your thoughts on this."
                        ""
                        "\n\nBest wishes\nJohannes",
            WorkerIds=worker_batch
        )


if __name__ == '__main__':
    main()
