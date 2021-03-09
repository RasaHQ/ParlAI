import json
import os
import sys
import shutil
from typing import Any, Text, Optional, Tuple, List, Set


def get_tasks_domains_and_workers(t_dir: Text) -> Tuple[Set[Text], Set[Text], Set[Text]]:
    with open(os.path.join(t_dir, "custom", "data.json"), "r", encoding="utf-8") as file:
        data = json.load(file)
        _tasks = {c.get("Task") for c in data["Scenario"].get("WizardCapabilities")}
        _domains = set(data["Scenario"].get("Domains", []))
        _workers = {data.get("UserWorkerID"), data.get("WizardWorkerID")}
    return _tasks, _domains, _workers


if __name__ == '__main__':

    print(sys.argv)

    assert len(sys.argv) == 3
    store_directory = sys.argv.pop(1)
    run_directory = sys.argv.pop(1)

    run_name = os.path.basename(run_directory)

    destination = os.path.join(store_directory, run_name)
    os.makedirs(destination)

    tasks = set()
    domains = set()
    workers = set()

    for directory in os.listdir(run_directory):
        if directory.startswith("t_"):
            t, d, w = get_tasks_domains_and_workers(os.path.join(run_directory, directory))
            tasks.update(t)
            domains.update(d)
            workers.update(w)

            shutil.copytree(
                os.path.join(run_directory, directory),
                os.path.join(destination, directory)
            )

    print(f"Tasks:   {tasks}")
    print(f"Domains: {domains}")
    print(f"Workers: {workers}")

    # In case a domain was not defined
    domains = [d or "UNDEFINED" for d in domains]

    with open(os.path.join(destination, "README.md"), "w+", encoding="utf-8") as file:
        file.write(f"# {run_name}\n\n")
        file.write(f"## Metadata\n\n")
        file.write("\nDomains:\n")
        file.writelines([f"* {t}\n" for t in sorted(list(domains))])
        file.write("\nTasks:\n")
        file.writelines([f"* {t}\n" for t in sorted(list(tasks))])
        file.write("\nWorkers:\n")
        file.writelines([f"* {t}\n" for t in sorted(list(workers))])
