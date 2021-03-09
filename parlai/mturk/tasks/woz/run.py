import os
import random

from parlai import PROJECT_PATH
from parlai.core.params import ParlaiParser
from parlai.mturk.core import mturk_utils
from parlai.mturk.core.mturk_manager import MTurkManager
from parlai.mturk.core.shared_utils import print_and_log
from parlai.mturk.tasks.woz.backend.agents import WOZKnowledgeBaseAgent
from parlai.mturk.tasks.woz.backend.worlds import WOZWorld, RoleOnboardWorld
from parlai.mturk.tasks.woz.qualify import MTurkQualificationManager
from parlai.mturk.tasks.woz.task_config import task_config


def main():
    arg_parser = ParlaiParser(False, False)
    arg_parser.add_parlai_data_path()
    arg_parser.add_mturk_args()
    arg_parser.add_argument(
        '--max-onboard-time',
        type=int,
        default=300,
        help='Time limit for workers in onboarding',
    )
    WOZKnowledgeBaseAgent.add_cmdline_args(arg_parser)
    WOZWorld.add_cmdline_args(arg_parser)

    opt = arg_parser.parse_args()

    # Set the task name to be the folder name
    opt["task"] = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
    opt.update(task_config)

    # On disconnect, use STATUS_PARTNER_DISCONNECT_EARLY if fewer messages than this
    opt["min_messages"] = 20

    mturk_agent_ids = ["Wizard", "User"]
    mturk_manager = MTurkManager(opt=opt, mturk_agent_ids=mturk_agent_ids, use_db=True)

    task_directory = os.path.dirname(os.path.abspath(__file__))
    mturk_manager.setup_server(task_directory_path=task_directory)

    has_passed_tutorial_1 = mturk_utils.find_or_create_qualification(
        "PassedAIDialoguesTutorial1",
        "If owned, the worker has passed the AI Dialogues Tutorial 1. The value corresponds to the number of hints that the worker used.",
        opt['is_sandbox'],
    )
    has_passed_tutorial_2 = mturk_utils.find_or_create_qualification(
        "PassedAIDialoguesTutorial2",
        "If owned, the worker has passed the AI Dialogues Tutorial 2. The value corresponds to the number of hints that the worker used.",
        opt['is_sandbox']
    )
    qualification_manager = MTurkQualificationManager()
    qualification_manager.require_existence(has_passed_tutorial_2)    # ToDo: Make this an arg switch
    print("Required qualifications:")
    for q in qualification_manager.qualifications:
        print(f" * {q}")

    worker_roles = {}
    connect_counter = 0

    try:
        mturk_manager.start_new_run()

        def run_onboard(worker):
            nonlocal connect_counter
            role = mturk_agent_ids[connect_counter % len(mturk_agent_ids)]
            connect_counter += 1
            print_and_log(100, f"run_onboard for {worker.worker_id} as {role}", True)
            worker_roles[worker.worker_id] = role
            world = RoleOnboardWorld(opt, worker, role)
            world.parley()
            world.shutdown()

        mturk_manager.set_onboard_function(onboard_function=run_onboard)
        mturk_manager.ready_to_accept_workers()
        mturk_manager.create_hits(qualifications=qualification_manager.qualifications)

        def check_workers_eligibility(workers):
            if opt['is_sandbox']:
                return workers
            valid_workers = {}
            for worker in workers:
                worker_id = worker.worker_id
                if worker_id not in worker_roles:
                    """
                    Something went wrong...
                    """
                    print_and_log(100, f"check_workers_eligibility failed", True)
                    continue
                role = worker_roles[worker_id]
                if role not in valid_workers:
                    valid_workers[role] = worker
                if len(valid_workers) == 2:
                    break
            return valid_workers.values() if len(valid_workers) == 2 else []

        eligibility_function = {'func': check_workers_eligibility, 'multiple': True}

        def assign_worker_roles(workers):
            if opt['is_sandbox']:
                for i, worker in enumerate(workers):
                    worker.id = mturk_agent_ids[i % len(mturk_agent_ids)]
                    print_and_log(
                        100, f"assigning {worker.id} role to {worker.worker_id}", True
                    )
            else:
                for worker in workers:
                    worker.id = worker_roles[worker.worker_id]
                    print_and_log(
                        100, f"assigning {worker.id} role to {worker.worker_id}", True
                    )

        # Load scenarios
        scenarios_list_fn = os.path.join(
            PROJECT_PATH,
            "parlai",
            "mturk",
            "tasks",
            "woz",
            "scenarios",
            opt.get("scenario_list") + ".txt",
        )
        scenarios_list = [e.strip() for e in open(scenarios_list_fn).readlines()]
        if not opt["is_sandbox"]:
            random.shuffle(scenarios_list)
        scenario_index: int = 0

        def run_conversation(mturk_manager, opt, workers):
            nonlocal scenario_index
            scenario = scenarios_list[scenario_index % len(scenarios_list)]
            scenario_index += 1

            if hasattr(mturk_manager, "conversation_index"):
                print_and_log(
                    100, f"run_conversation for t_{mturk_manager.conversation_index}", True
                )

            agents = workers[:]
            if not opt['is_sandbox']:
                for agent in agents:
                    worker_roles.pop(agent.worker_id)

            kb_agent = WOZKnowledgeBaseAgent(options=opt)
            workers += [kb_agent]

            world = WOZWorld(
                opt=opt,
                scenario=scenario,
                agents=workers,
                observers=[],  # [user_tutor_agent]
            )
            while not world.episode_done():
                world.parley()
            world.shutdown()
            world.review_work()

            # Return the contents for saving
            return world.prep_save_data(workers)

        mturk_manager.start_task(
            eligibility_function=eligibility_function,
            assign_role_function=assign_worker_roles,
            task_function=run_conversation,
        )

    except BaseException:
        raise
    finally:
        mturk_manager.expire_all_unassigned_hits()
        mturk_manager.shutdown()


if __name__ == '__main__':
    main()
