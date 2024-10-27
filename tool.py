from typing import Any, Callable, Dict
import json


class Tool:
    def __init__(self, schema: Dict[str, Any], function: Callable):
        self.schema = { "type": "function", "function": schema }
        self.function = function

    def __call__(self, *args, **kwargs) -> Any:
        return self.function(*args, **kwargs)
