import copy
from enum import Enum


class SerializationError(Exception):
    pass


class TaggedClass:
    pass


class TaggedCustomString(str):
    pass


def serialize(x):
    if isinstance(x, list):
        return {"type": "OcamlList", "value": [serialize(result) for result in x]}
    elif isinstance(x, tuple) and len(x) == 2:
        return {"type": "ScmPair", "value": {"car": serialize(x[0]), "cdr": serialize(x[1])}}
    elif isinstance(x, Enum):
        return {"type": x.__class__.__name__, "value": x.name}
    elif isinstance(x, TaggedCustomString):
        return {"type": x.__class__.__name__, "value": str(x)}
    elif isinstance(x, TaggedClass):
        res = {}
        for key in x.__dict__:
            attribute = getattr(x, key)
            res[key] = serialize(attribute)

        if res == {}:
            return {"type": x.__class__.__name__}
        else:
            return {"type": x.__class__.__name__, "value": res}

    elif isinstance(x, str) or isinstance(x, int) or isinstance(x, float):
        return x

    else:
        raise SerializationError(f"Unseriazable type: f{type(x)}")
