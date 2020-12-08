import re
from typing import Literal, Union

from pydantic import BaseModel, Field


class Acc(BaseModel):
    code: Literal["acc"]
    value: int = Field(..., alias="arg1")


class Nop(BaseModel):
    code: Literal["nop"]
    unused: int = Field(..., alias="arg1")


class Jmp(BaseModel):
    code: Literal["jmp"]
    offset: int = Field(..., alias="arg1")


Instruction = Union[
    Acc, Nop, Jmp
]


# Pretty pointless class that simply saves me the trouble
# of iterating over the Union type myself.
#
# Right now we could simply get the instruction type simply
# by looking at the code, but it's likely that in the future
# it may be a bit more complicated (e.g. `jmp +4` vs `jmp @4`,
# relative vs absolute jumps).
#
# Using a Union type instead of simply subclassing also means
# we can check for exhaustiveness.
class _InstructionBuilder(BaseModel):
    __root__: Instruction


_regex = "(?P<code>\\w{3}) (?P<arg1>(\\+|-)\\d+)"
_compiled = re.compile(_regex)


def instruction_parser(line: str) -> Instruction:
    if match := re.match(_compiled, line):
        return _InstructionBuilder.parse_obj(match.groupdict()).__root__
    else:
        raise ValueError(f"Unknown instruction {line}")

