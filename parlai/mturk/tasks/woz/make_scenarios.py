import re
from collections import defaultdict

import copy
import json
import os
import random
import string
from typing import Optional, Text

from parlai.mturk.tasks.woz.backend.commands import DEFAULT_USER_INSTRUCTION
from parlai.mturk.tasks.woz.task_config import TUTORIAL_URL

template_dir = 'templates/'
scenario_dir = 'scenarios/'
scenario_file = 'scenarios/all_scenarios.txt'
db_dir = 'templates/dbs/'
scenarios_per = 5


def sample(parameter):
    if parameter.get("Type") == "Integer":
        _min = int(parameter.get("Min", 0))
        _max = int(parameter.get("Max", 100))
        return random.randint(_min, _max)
    elif parameter.get("Type") == "Categorical":
        return random.choice(parameter.get("Categories"))
    elif parameter.get("Type") == "Boolean":
        return random.choice([False, True])


def populate(desc: Optional[Text], db_path: Text) -> Optional[Text]:
    if not desc:
        return None
    db = json.load(open(db_path))
    db_params = {e['Name']: e for e in db}

    # Detect all slots
    slots = [
        s[:-1] if s[-1] in string.punctuation else s
        for s in re.split(r"[ '(]", desc)
        if s.startswith('@')
    ]
    slots = list(set(slots))

    # Sample slots
    slot_values = {}
    param_selected = defaultdict(list)
    for slot in slots:
        param = slot.split('-')[0][1:]
        value = sample(db_params.get(param))

        # Resample if already selected
        while value in param_selected[param]:
            value = sample(db_params.get(param))

        param_selected[param].append(value)
        slot_values[slot] = value

    # Replace description
    for slot, value in slot_values.items():
        desc = desc.replace(slot, str(value))

    return desc


def get_value_from_db(slot: Text, filename: Text) -> Text:
    with open(filename, "r", encoding="utf-8") as file:
        db = json.load(file)
        db_params = {e['Name']: e for e in db}

    if re.match(slot, ".*-\d*"):
        slot, v = slot.split("-")
        variation = int(v)
    else:
        variation = None

    return sample(db_params.get(slot))


class DatabaseCollection:
    def __init__(self):
        self.databases = {}
        self.filled_slots = defaultdict(list)

    def _load_db_if_necessary(self, db_name: Text) -> None:
        if db_name not in self.databases:
            filename = os.path.join(db_dir, db_name + ".json")
            with open(filename, "r", encoding="utf-8") as file:
                self.databases[db_name] = json.load(file)

    def _new_sample(self, db_name: Text, slot_name: Text, variation: int) -> Text:
        self._load_db_if_necessary(db_name)
        db_params = {param["Name"]: param for param in self.databases[db_name]}
        candidate_sample = None
        while len(self.filled_slots[db_name + slot_name]) < variation + 1:
            while (
                not candidate_sample
                or candidate_sample in self.filled_slots[db_name + slot_name]
            ):
                candidate_sample = sample(db_params.get(slot_name))
            self.filled_slots[db_name + slot_name].append(candidate_sample)
        assert candidate_sample
        return candidate_sample

    def _existing_sample(
        self, db_name: Text, slot_name: Text, variation: int
    ) -> Optional[Text]:
        if db_name not in self.databases:
            return None
        elif db_name + slot_name not in self.filled_slots:
            return None
        elif len(self.filled_slots[db_name + slot_name]) < variation + 1:
            return None
        else:
            return self.filled_slots[db_name + slot_name][variation]

    def get_value(self, slot: Text, db_name: Text) -> Text:
        if re.match(r".+\-\d+", slot):
            name, v = slot.split("-")
            variation = int(v) - 1
        else:
            name = slot
            variation = 0

        result = self._existing_sample(db_name, name, variation)
        if not result:
            result = self._new_sample(db_name, name, variation)

        return result

    def populate(self, desc: Optional[Text]) -> Optional[Text]:
        if not desc:
            return None
        slots = re.findall(r"\`([\w\-]+)@([\w]+)\`", desc)
        for slot, db_name in slots:
            original = f"`{slot}@{db_name}`"
            desc = desc.replace(original, str(self.get_value(slot, db_name)))
        return desc


easy = [
    'happy_followup_doctor_appointment.json',
    'happy_weather.json',
    'happy_spaceship_access_codes.json',
    'happy_ride_change.json',
    'happy_ride_status.json',
]
medium = [
    'happy_party_rsvp.json',
    'happy_restaurant_search.json',
    'happy_restaurant_reserve.json',
    'happy_apartment_search.json',
    'happy_hotel_service_request.json',
    'happy_book_apartment_viewing.json',
    'happy_party_plan.json',
    'happy_hotel_search.json',
    'happy_hotel_reserve.json',
    'happy_plane_search.json',
    'happy_plane_reserve.json',
    'happy_book_ride.json',
    'happy_book_doctor_appointment.json',
]
hard = [
    'happy_trivia.json',
    'happy_bank_fraud_report.json',
    'happy_schedule_meeting.json',
    'happy_bank_balance.json',
    'happy_trip_directions.json',
]

easy_unhappy = [
    'unhappy_weather-1.json',
    'unhappy_book_ride-1.json',
    'unhappy_book_ride-2.json',
    'unhappy_book_ride-3.json',
    'unhappy_spaceship_life_support-1.json',
    'unhappy_spaceship_access_codes-1.json'
]
medium_unhappy = [
    'unhappy_followup_doctor_appointment-1.json',
    'unhappy_plane_reserve-1.json',
    'unhappy_party_plan-1.json',
    'unhappy_party_plan-2.json',
    'unhappy_book_apartment_viewing-1.json',
    'unhappy_book_doctor_appointment-1.json',
    'unhappy_trivia-1.json'
]
hard_unhappy = [
    'unhappy_fraud_report-1.json',
    'unhappy_fraud_report-2.json',
    'unhappy_trip_directions-1.json',
    'unhappy_hotel_reserve-1.json',
    'unhappy_hotel_search-1.json'
]

MIXED = True

if not MIXED:
    counts = {}
    for e in easy:
        counts[e] = 25
    for e in medium:
        counts[e] = 30
    for e in hard:
        counts[e] = 45
    for e in easy_unhappy:
        counts[e] = 40
    for e in medium_unhappy:
        counts[e] = 60
    for e in hard_unhappy:
        counts[e] = 80

    # counts = {
    #     "happy_ride_change.json": 10,
    #     "happy_ride_status.json": 10,
    #     "happy_apartment_search.json": 10,
    #     "happy_schedule_meeting.json": 10,
    #     "happy_restaurant_search.json": 10,
    #     "happy_followup_doctor_appointment.json": 10,
    #     "happy_restaurant_reserve.json": 1,
    #     "happy_plane_search.json": 1,
    #     "happy_bank_balance.json": 1,
    #     "happy_hotel_service_request.json": 1,
    #     "happy_spaceship_access_codes.json": 1,
    #     "happy_spaceship_life_support.json": 1,
    #     "happy_hotel_search.json": 1,
    # }
else:
    counts = {
        "mix_free-plane_search+reserve+weather.json": 20,
        "mix-trip_directions+trivia.json": 20,
        "mix_free-ride_change+status+party_rsvp.json": 10,
        "mix_free-hotel_search+reserve+weather.json": 20,
        "mix_party+restaurant+weather.json": 20,
        "mix_free-restaurant_reserve+bank_balance+fraud+weather-1.json": 20,
        "mix_free-restaurant_reserve+bank_balance+fraud+weather-2.json": 20,
        "mix_free-restaurant_reserve+bank_balance+weather.json": 20,
        "mix_free-apartment+book_ride+weather.json": 30,
        "mix_free-restaurant_search+followup_doctor+ride_change.json": 15,
        "mix_free-doctor_appointment+plane_reserve+restaurant_reserve+hotel_service.json": 20,
        "mix_free-plane_search+schedule_meeting+party_rsvp+restaurant_reserve+hotel_service_request.json": 20,
        "mix_free-ride_status+trip_directions+schedule_meeting+weather.json": 20
    }


if __name__ == '__main__':
    open(scenario_file, 'w+').write("")
    for fn in os.listdir(template_dir):
        if not fn.endswith('json'):
            continue

        template = json.load(open(template_dir + fn))
        if "task_descriptions" in template['instructions']['User']:
            task_descriptions = template['instructions']['User']['task_descriptions']
        else:
            task_descriptions = [DEFAULT_USER_INSTRUCTION]

        total = counts.get(fn, 0)
        for i in range(total):
            desc = random.choice(task_descriptions)
            dc = DatabaseCollection()
            new_scenario = copy.deepcopy(template)
            if "task_descriptions" in template['instructions']['User']:
                del new_scenario['instructions']['User']['task_descriptions']
            new_scenario['instructions']['User']['task_description'] = dc.populate(
                populate(desc, db_dir + template['db'])
            )
            new_scenario['instructions']['Wizard']['task_description'] = dc.populate(
                new_scenario['instructions']['Wizard']['task_description'].replace(
                    "@wizard-tutorial-url", TUTORIAL_URL
                )
            )
            if "linear_guide" in new_scenario['instructions']['User']:
                new_scenario['instructions']['User']["linear_guide"] = [
                    dc.populate(instruction)
                    for instruction in new_scenario['instructions']['User'][
                        "linear_guide"
                    ]
                ]
            new_fn = "{0}/{1}_v{2}.json".format(scenario_dir, fn.split('.')[0], i)
            new_name = "{0}_v{1}\n".format(fn.split('.')[0], i)
            json.dump(new_scenario, open(new_fn, 'w+'), indent=True)
            open(scenario_file, 'a+').write(new_name)
