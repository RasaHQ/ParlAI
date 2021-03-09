#!/usr/bin/env python3
from typing import Set

import parlai.mturk.core.mturk_utils as mturk_utils

first_class_workers = [
    # Most experience
    # ~~ Redacted ~~
    # Longest average user utterances (but at least 10 dialogues)
    # ~~ Redacted ~~
    # Workers who asked good questions or submitted good dialogues
    # ~~ Redacted ~~
]

all_workers_with_at_least_10_wizard_HITs = [
    # ~~ Redacted ~~
]


def grant_stage3_qualification(workers: Set, is_sandbox: bool = True) -> None:

    mturk_utils.setup_aws_credentials()
    client = mturk_utils.get_mturk_client(False)

    qualification = mturk_utils.find_or_create_qualification(
        "ReadyForAIDialoguesTutorial2",
        "If owned, the worker can enter Stage III of the AI Dialogues tasks.",
        is_sandbox,
    )

    for worker in workers:
        print(f"Qualifying {worker}")

        client.associate_qualification_with_worker(
            QualificationTypeId=qualification,
            WorkerId=worker,
            IntegerValue=1,
            SendNotification=True,
        )


if __name__ == '__main__':
    print(f"{len(first_class_workers)} -- {len(set(first_class_workers))}")

    # grant_stage3_qualification(set(first_class_workers), is_sandbox=False)
    grant_stage3_qualification(set(all_workers_with_at_least_10_wizard_HITs), is_sandbox=False)
