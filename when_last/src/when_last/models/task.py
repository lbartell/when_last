import dataclasses
import datetime
from uuid import UUID, uuid1


@dataclasses.dataclass
class Task:
    name: str
    created: datetime.datetime = None
    uuid: UUID = None

    def __post_init__(self):
        self.created = datetime.datetime.now()
        self.uuid = uuid1()
