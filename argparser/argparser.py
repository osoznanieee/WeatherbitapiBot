import argparse
from typing import (
    Literal, Optional
)

from pydantic import BaseModel


class Action(BaseModel):
    create: Literal['create']
    drop: Optional[Literal['drop']]


class SQLDrop(BaseModel):
    drop: Literal['drop']


class ArgParser:
    def __call__(self, *args, **kwargs) -> Optional[Action | SQLDrop]:
        parser = argparse.ArgumentParser()

        parser.add_argument('-a', '--action', type=str)
        parser.add_argument('-d', '--drop', type=str)

        args = parser.parse_args()

        if action := args.action:

            create = action[:action.find('-')] if action.find('-') != -1 else action

            drop = action[action.find('-') + 1:] if action.find('-') != -1 else None

            return Action(create=create, drop=drop)

        elif action := args.drop:
            return SQLDrop(drop=action)

        return None
