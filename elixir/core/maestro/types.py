from typing import Callable, Type
from pydantic import BaseModel
import greenstalk

JobFunction = Callable[[greenstalk.Job, "Musician"], None]
JobParameters = Type[BaseModel]

JobIndex = dict[str, JobFunction]
JobList = dict[str, JobParameters]
