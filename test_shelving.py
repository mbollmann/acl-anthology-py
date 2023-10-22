# Copyright 2023 Marcel Bollmann <marcel@bollmann.me>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import attrs
import shelve
from acl_anthology import Anthology
from acl_anthology.people import Name, Person, PersonIndex
from pathlib import Path
from rich import print
from timer import Timer


filename = Path("test_shelf")
if filename.is_file():
    filename.unlink()


def access_index(idx):
    print(idx)
    people = idx.get_by_name(Name("Pranav", "Anand"))
    print(people)
    person = idx.get("pranav-anand")
    print(person)
    print(idx.similar.subset(person.id))


anthology = Anthology.from_repo()

with Timer().watch_and_report(msg="build PeopleIndex"):
    anthology.people.load()

access_index(anthology.people)

with Timer().watch_and_report(msg="shelve PeopleIndex"):
    with shelve.open(filename) as db:
        db["similar"] = anthology.people.similar
        db["name_to_ids"] = anthology.people.name_to_ids
        db["data"] = {
            person_id: attrs.asdict(
                person, recurse=False, filter=lambda k, v: k.name not in ("id", "parent")
            )
            for person_id, person in anthology.people.items()
        }

del anthology.people
index = PersonIndex(anthology)
index.is_data_loaded = True

with Timer().watch_and_report(msg="restore PeopleIndex"):
    with shelve.open(filename) as db:
        index.similar = db["similar"]
        index.name_to_ids = db["name_to_ids"]
        for person_id, person_dict in db["data"].items():
            index[person_id] = Person(person_id, anthology, **person_dict)

anthology.people = index
access_index(anthology.people)

# PersonIndex depends on:
# - xml/*
# - yaml/name_variants.yaml
#
# SIGIndex depends on:
# - yaml/sigs/*
#
# VenueIndex depends on:
# - xml/*
# - yaml/venues/*
