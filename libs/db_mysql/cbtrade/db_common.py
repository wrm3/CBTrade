#<=====>#
# Description
#<=====>#


#<=====>#
# Known To Do List
#<=====>#


#<=====>#
# Imports - Public
#<=====>#


#<=====>#
# Imports - Project
#<=====>#
from libs.common import narc
from typing import Any, Iterable, Optional, Tuple


#<=====>#
# Variables
#<=====>#
lib_name      = 'cbtrade.db_common'
log_name      = 'cbtrade.db_common'


# <=====>#
# Assignments Pre
# <=====>#
debug_tf = False


#<=====>#
# Classes
#<=====>#



#<=====>#
# Functions
#<=====>#

@narc(1)
def to_scalar_dict(obj):
    """
    Convert an object or mapping into a flat dict of scalar values only,
    skipping private keys and nested collections.
    """
    out = {}
    # Mapping-like (e.g., AttrDict, dict)
    try:
        items: Optional[Iterable[Tuple[Any, Any]]] = (
            obj.items() if hasattr(obj, 'items') and callable(getattr(obj, 'items', None)) else None
        )
        if items is not None:
            for k, v in items:
                if not str(k).startswith('_') and not isinstance(v, (dict, list, set, tuple)):
                    out[k] = v
            return out
    except Exception:
        pass
    # Attribute introspection fallback
    for k in dir(obj):
        if k.startswith('_'):
            continue
        try:
            v = getattr(obj, k)
        except Exception:
            continue
        if not callable(v) and not isinstance(v, (dict, list, set, tuple)):
            out[k] = v
    return out

#<=====>#
