"""
Consolidated FSTrent Core Utilities

This module contains ONLY the functions actually used in the cbtrade project.
Replaces the bloated 40-file fstrent_common library with essential functions only.

🔴 GILFOYLE'S CLEANUP: 95% reduction in code bloat (40 files → 1 file)
"""

import csv
import copy
import datetime
import decimal
import functools
import json
import os
import re
import sys
import time
import traceback
import uuid

from datetime import datetime as dt
from datetime import timezone
from decimal import Decimal
from typing import Any, Callable, Dict, List, Optional, Type, Union
from typing import get_args, get_origin

#<=====>#

spacer = ' ' * 4

#<=====>#

class AttrDict(dict):
    """
    A dictionary that allows attribute-style access (dict.key) in addition to item-style access (dict['key']).
    """
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        for k, v in self.items():
            if isinstance(v, dict):
                self[k] = AttrDict(v)

    #<=====>#
 
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    #<=====>#
 
    def __setattr__(self, name, value):
        if isinstance(value, dict) and not isinstance(value, AttrDict):
            value = AttrDict(value)
        self[name] = value

    #<=====>#
 
    def __delattr__(self, name):

            del self[name]

#<=====>#
 
class AttrDictEnh(dict):
    """
    Enhanced AttrDict with schema validation, type conversion, mutable factory system, and serialization.
    
    Features:
    - Schema-based type validation and conversion
    - Automatic factory system for mutable types (prevents shared object issues)
    - Support for complex types (Optional, List, Dict, Decimal, custom classes)
    - Required field validation and custom validation functions
    - Multiple serialization formats (JSON, CSV)
    - Dynamic field addition and runtime schema modification
    - Backward compatibility with AttrDict
    
    Example:
        class TradeData(AttrDictEnh):
            _schema = {
                'symbol': str,
                'price': float,
                'indicators': list,  # Auto-factory: each instance gets fresh list
                'config': dict,      # Auto-factory: each instance gets fresh dict
            }
        
        trade = TradeData({'symbol': 'BTC-USD', 'price': '50000'})  # price auto-converted
        trade.indicators.append('RSI')  # Safe - no shared objects
    """
    
    _schema = {}  # Default empty schema
    _MUTABLE_TYPES = {list, dict, set, bytearray}  # Built-in mutable types for auto-factory
    _REGISTERED_MUTABLE_TYPES = set()  # Custom registered mutable types

    #<=====>#
 
    def __init__(self, data=None, schema=None):
        """
        Initialize AttrDictEnh with optional data and schema override.
        
        Args:
            data: Initial data (dict-like or None)
            schema: Schema override (dict or None to use class _schema)
        """
        super().__init__()
        
        # Use provided schema or class schema
        self._instance_schema = schema if schema is not None else self._schema.copy()
        self._processed_schema = self._process_schema(self._instance_schema)
        
        # Apply schema defaults with factories first
        self._apply_schema_defaults()
        
        # Then update with provided data (with validation)
        if data:
            if isinstance(data, dict):
                for key, value in data.items():
                    self[key] = value
            else:
                raise TypeError(f"AttrDictEnh data must be dict-like, got {type(data)}")

    #<=====>#
 
    def __getattr__(self, name):
        """Enable dot notation access."""
        # For internal attributes (starting with underscore), raise AttributeError if not found
        # This prevents infinite recursion when checking for internal attributes like _defaults
        if name.startswith('_'):
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    #<=====>#
 
    def __setattr__(self, name, value):
        """Handle attribute assignment with schema validation."""
        # Allow internal attributes
        if name.startswith('_'):
            super().__setattr__(name, value)
            return
        
        # Use __setitem__ for schema validation
        self[name] = value

    #<=====>#
 
    def __setitem__(self, key, value):
        """Handle item assignment with schema validation and type conversion."""
        # Check if field is in schema
        if key in self._processed_schema:
            field_info = self._processed_schema[key]
            
            # Type validation and conversion
            if field_info['type'] is not None:
                value = self._validate_and_convert_type(key, value, field_info['type'])
            
            # Custom validation
            if field_info['validator'] is not None:

                    if not field_info['validator'](value):
                        raise ValueError(f"Custom validation failed for field '{key}' with value: {value}")
        
        # Convert nested dicts to AttrDictEnh for consistency
        if isinstance(value, dict) and not isinstance(value, AttrDictEnh):
            value = AttrDictEnh(value)
        
        super().__setitem__(key, value)

    #<=====>#
 
    def __delattr__(self, name):
        """Handle attribute deletion."""

        del self[name]

    #<=====>#
 
    def _process_schema(self, schema):
        """
        Process schema to extract type, factory, required status, and validation functions.
        
        Returns processed schema dict with standardized format:
        {field_name: {'type': type, 'factory': callable, 'required': bool, 'validator': callable}}
        """
        processed = {}
        
        for field_name, field_spec in schema.items():
            entry = {
                'type': None,
                'factory': None,
                'required': False,
                'validator': None
            }

            if isinstance(field_spec, type):
                # Simple type: 'field': str
                entry['type'] = field_spec
                entry['factory'] = self._get_auto_factory(field_spec)
                
            elif isinstance(field_spec, tuple):
                if len(field_spec) == 2:
                    # Could be (type, factory), (type, validator), or (type, required)
                    type_spec, second = field_spec
                    entry['type'] = type_spec
                    
                    if callable(second) and not isinstance(second, type):
                        # (type, validator_function)
                        entry['validator'] = second
                        entry['factory'] = self._get_auto_factory(type_spec)
                    elif second is True or (hasattr(second, '__name__') and second.__name__ == 'required'):
                        # (type, required=True)
                        entry['required'] = True
                        entry['factory'] = self._get_auto_factory(type_spec)
                    else:
                        # (type, factory)
                        entry['factory'] = second
                        
                elif len(field_spec) == 3:
                    # (type, factory, required) or (type, factory, validator)
                    type_spec, factory, third = field_spec
                    entry['type'] = type_spec
                    entry['factory'] = factory
                    
                    if callable(third):
                        entry['validator'] = third
                    else:
                        entry['required'] = bool(third)
                        
                else:
                    raise ValueError(f"Invalid schema specification for field '{field_name}': {field_spec}")
            else:
                # Handle complex types from typing module
                entry['type'] = field_spec
                entry['factory'] = self._get_auto_factory(field_spec)
            
            processed[field_name] = entry
            
        return processed

    #<=====>#
 
    def _get_auto_factory(self, type_spec):
        """
        Get automatic factory for mutable types.
        
        Args:
            type_spec: Type specification
            
        Returns:
            Factory callable or None
        """
        # Handle basic mutable types
        if type_spec in self._MUTABLE_TYPES or type_spec in self._REGISTERED_MUTABLE_TYPES:
            return type_spec
        
        # Handle typing module types
        origin = get_origin(type_spec)
        if origin is not None:
            if origin in self._MUTABLE_TYPES:
                return origin
            if origin is Union:
                # Handle Optional[T] (which is Union[T, None])
                args = get_args(type_spec)
                if len(args) == 2 and type(None) in args:
                    # This is Optional[T], no factory needed (defaults to None)
                    return None
        
        return None

    #<=====>#
 
    def _apply_schema_defaults(self):
        """Apply default values using factories for mutable types and _defaults for scalar types."""
        
        # First apply factory-based defaults for mutable types
        for field_name, field_info in self._processed_schema.items():
            if field_info['factory'] is not None:
                # Only apply factory defaults if field is not already set
                if field_name not in self:
                    if callable(field_info['factory']):
                        default_value = field_info['factory']()
                    else:
                        default_value = field_info['factory']
                    
                    # Set directly in dict to avoid validation during initialization
                    super().__setitem__(field_name, default_value)
        
        # Then apply scalar defaults from _defaults attribute if it exists
        if hasattr(self, '_defaults') and self._defaults:
            for field_name, default_value in self._defaults.items():
                # Only set if field is in schema and not already set by factory
                if field_name in self._processed_schema and field_name not in self:
                    # Set directly in dict to avoid validation during initialization
                    super().__setitem__(field_name, default_value)

    #<=====>#
 
 
    def _save_to_csv(self, filepath):
        """Save to CSV file (flattened structure)."""
        dir_val(filepath)
        
        flattened = self._flatten_for_csv()
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            if flattened:
                writer = csv.DictWriter(f, fieldnames=flattened.keys())
                writer.writeheader()
                writer.writerow(flattened)

    #<=====>#
 


    #<=====>#
 
    @classmethod
    def _load_from_csv(cls, filepath, schema=None):
        """Load from CSV file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            row = next(reader, {})
            
        # Unflatten the data
        data = cls._unflatten_from_csv(row)
        return cls(data, schema=schema)

    #<=====>#
 
    def _flatten_for_csv(self, prefix=''):
        """Flatten nested structure for CSV compatibility."""
        flattened = {}
        
        for key, value in self.items():
            full_key = f"{prefix}{key}" if prefix else key
            
            if isinstance(value, dict):
                # Recursively flatten nested dicts
                nested = AttrDictEnh(value)._flatten_for_csv(f"{full_key}.")
                flattened.update(nested)
            elif isinstance(value, list):
                # Store lists as JSON strings
                flattened[full_key] = json.dumps(value)
            else:
                flattened[full_key] = str(value)
        
        return flattened

    #<=====>#
 
    @classmethod
    def _unflatten_from_csv(cls, flattened_data):
        """Unflatten CSV data back to nested structure."""
        data = {}
        
        for key, value in flattened_data.items():
            if '.' in key:
                # Handle nested keys
                keys = key.split('.')
                current = data
                
                for k in keys[:-1]:
                    if k not in current:
                        current[k] = {}
                    current = current[k]

                    current[keys[-1]] = json.loads(value)
            else:

                    data[key] = json.loads(value)
        
        return data

    #<=====>#
 
    def _validate_and_convert_type(self, field_name, value, expected_type):
        """
        Validate and convert value to expected type.
        
        Args:
            field_name: Name of the field
            value: Value to validate/convert
            expected_type: Expected type specification
            
        Returns:
            Converted value
            
        Raises:
            ValueError: If validation/conversion fails
        """
        from decimal import Decimal
        import datetime
        from typing import Union, Optional, List, Dict, get_origin, get_args
        
        if value is None:
            # First check if we have a default value (even for Optional fields)
            if hasattr(self.__class__, '_defaults') and field_name in getattr(self.__class__, '_defaults', {}):
                default_value = getattr(self.__class__, '_defaults', {})[field_name]
                # CRITICAL: Prevent recursion if default is same as current value
                if default_value == value:
                    return None  # Break recursion cycle
                # Recursively validate the default value to ensure it's the right type
                return self._validate_and_convert_type(field_name, default_value, expected_type)
            
            # Handle Optional types (only after checking for defaults)
            origin = get_origin(expected_type)
            if origin is Union:
                args = get_args(expected_type)
                if type(None) in args:
                    return None
            
            # For non-optional fields with None value and no default
            if expected_type != type(None):
                raise ValueError(f"Field '{field_name}' cannot be None and no default value is available")
            return None
        
        # Handle typing module types first
        origin = get_origin(expected_type)
        if origin is not None:
            if origin is Union:
                # Handle Optional[T]
                args = get_args(expected_type)
                if len(args) == 2 and type(None) in args:
                    non_none_type = args[0] if args[1] is type(None) else args[1]
                    # Special handling for string "None" in Optional types
                    if isinstance(value, str) and value == "None":
                        return None  # Convert string "None" to actual None for Optional fields
                    return self._validate_and_convert_type(field_name, value, non_none_type)
            elif origin in (list, List):
                if not isinstance(value, list):
                    raise ValueError(f"Field '{field_name}' expects list, got {type(value).__name__}: {value}")
                return value
            elif origin in (dict, Dict):
                if not isinstance(value, dict):
                    raise ValueError(f"Field '{field_name}' expects dict, got {type(value).__name__}: {value}")
                return value
        
        # Check if value is already the correct type
        if isinstance(value, expected_type):
            return value

        # Type conversion for basic types
        if expected_type == str:
            return str(value)
        elif expected_type == int:
            if isinstance(value, str):
                return int(float(value))  # Handle "123.0" -> 123
            return int(value)
        elif expected_type == float:
            return float(value)
        elif expected_type == bool:
            if isinstance(value, str):
                return value.lower() in ('true', '1', 'yes', 'on')
            return bool(value)
        elif expected_type == Decimal:
            return Decimal(str(value))
        elif expected_type == datetime.datetime:
            if isinstance(value, str):
                # Handle string "None" as actual None value
                if value == "None":
                    return None
                # First try ISO format (backwards compatibility)
                return datetime.datetime.fromisoformat(value.replace('Z', '+00:00'))
            return value
        else:
            # Try direct type conversion for other types
            try:
                return expected_type(value)
            except (TypeError, ValueError) as e:
                raise ValueError(f"Cannot convert value '{value}' to type {expected_type.__name__} for field '{field_name}': {e}")

    #<=====>#
 
    def add_schema_field(self, name, field_type):
        """
        Add or modify a schema field at runtime.
        
        Args:
            name: Field name
            field_type: Field type specification (same format as _schema)
        """
        self._instance_schema[name] = field_type
        self._processed_schema = self._process_schema(self._instance_schema)
        
        # Apply default if field doesn't exist and has factory
        if name not in self and name in self._processed_schema:
            field_info = self._processed_schema[name]
            if field_info['factory'] is not None:

                    default_value = field_info['factory']()
                    super().__setitem__(name, default_value)

    #<=====>#
 
    @classmethod
    def register_mutable_type(cls, type_class):
        """
        Register a custom type as mutable for auto-factory treatment.
        
        Args:
            type_class: Type to register as mutable
        """
        cls._REGISTERED_MUTABLE_TYPES.add(type_class)

    #<=====>#
 
    def validate_all(self):
        """
        Validate all current fields against schema.
        
        Returns:
            Dict of validation results: {field_name: True/error_message}
        """
        results = {}
        
        # Check required fields
        for field_name, field_info in self._processed_schema.items():
            if field_info['required'] and field_name not in self:
                results[field_name] = f"Required field '{field_name}' is missing"
                continue
            
            if field_name in self:

                    # Validate type
                    if field_info['type'] is not None:
                        self._validate_and_convert_type(field_name, self[field_name], field_info['type'])
                    
                    # Validate custom validation
                    if field_info['validator'] is not None:
                        if not field_info['validator'](self[field_name]):
                            results[field_name] = f"Custom validation failed for field '{field_name}'"
                        else:
                            results[field_name] = True
                    else:
                        results[field_name] = True
        return results

    #<=====>#
 
    def get_schema_fields(self):
        """Return list of fields defined in schema."""
        return list(self._processed_schema.keys())

    #<=====>#
 
    def get_dynamic_fields(self):
        """Return list of fields not defined in schema."""
        return [key for key in self.keys() if key not in self._processed_schema]

    #<=====>#
 
    def copy(self):
        """Create a deep copy of the AttrDictEnh instance."""
        new_instance = self.__class__(schema=self._instance_schema.copy())
        for key, value in self.items():
            new_instance[key] = copy.deepcopy(value)
        return new_instance

    #<=====>#
 
    def to_dict(self):
        """Convert to plain dict (like dataclass asdict())."""
        result = {}
        for key, value in self.items():
            if isinstance(value, AttrDictEnh):
                result[key] = value.to_dict()
            elif isinstance(value, list):
                result[key] = [item.to_dict() if isinstance(item, AttrDictEnh) else item for item in value]
            elif isinstance(value, dict):
                result[key] = {k: (v.to_dict() if isinstance(v, AttrDictEnh) else v) for k, v in value.items()}
            else:
                result[key] = value
        return result

    #<=====>#
 
    def to_json(self):
        """Return JSON string representation."""
        def json_serializer(obj):
            if isinstance(obj, Decimal):
                return float(obj)
            elif isinstance(obj, datetime.datetime):
                return obj.isoformat()
            elif isinstance(obj, AttrDictEnh):
                return obj.to_dict()
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
        
        return json.dumps(self.to_dict(), default=json_serializer, indent=2)
    
    @classmethod
    def from_json(cls, json_str, schema=None):
        """Create instance from JSON string."""
        data = json.loads(json_str)
        return cls(data, schema=schema)
    

    #<=====>#
 
    def save_to_json(self, filepath):
        """Save to JSON file."""
        dir_val(filepath)  # Ensure directory exists
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_json())
    

    #<=====>#
 
    @classmethod
    def load_from_json(cls, filepath, schema=None):
        """Load from JSON file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            return cls.from_json(f.read(), schema=schema)
    

    #<=====>#
 
    def save_to_file(self, filepath, format='json'):
        """
        Save to file in specified format.
        
        Args:
            filepath: File path
            format: Format ('json', 'csv')
        """
        format = format.lower()
        
        if format == 'json':
            self.save_to_json(filepath)
        elif format == 'csv':
            self._save_to_csv(filepath)
        else:
            raise ValueError(f"Unsupported format: {format}")

    #<=====>#
 
    @classmethod
    def load_from_file(cls, filepath, format='auto', schema=None):
        """
        Load from file with format detection.
        
        Args:
            filepath: File path
            format: Format ('auto', 'json', 'csv')
            schema: Schema override
        """
        if format == 'auto':
            ext = os.path.splitext(filepath)[1].lower()
            if ext == '.json':
                format = 'json'
            elif ext == '.csv':
                format = 'csv'
            else:
                raise ValueError(f"Cannot auto-detect format for file: {filepath}")
        
        format = format.lower()
        
        if format == 'json':
            return cls.load_from_json(filepath, schema=schema)
        elif format == 'csv':
            return cls._load_from_csv(filepath, schema=schema)
        else:
            raise ValueError(f"Unsupported format: {format}")

#<=====>#

class EmptyObject:
    """An empty object that can be used to dynamically add attributes."""
    pass

#<=====>#

def AttrDictConv(d, max_depth=20, current_depth=0, dec2float_yn='Y'):
    """Recursively converts a dictionary and its nested dictionaries to AttrDict.
    
    Args:
        d: Data to convert
        max_depth: Maximum recursion depth to prevent memory bloat
        current_depth: Current recursion level (internal use)
    """
    # Prevent infinite recursion and memory bloat
    if current_depth >= max_depth:
        print(f"🔴 GILFOYLE WARNING: AttrDictConv recursion limit reached at depth {max_depth}")
        if dec2float_yn == 'Y': d = dec_2_float(d)
        return d  # Return unconverted to prevent memory exhaustion

    if isinstance(d, dict):
        # For large dictionaries, limit processing to prevent memory issues
        if len(d) > 1000:
            print(f"🔴 GILFOYLE WARNING: Large dictionary ({len(d)} items) - using shallow conversion")
            # Just convert top level to prevent memory explosion
            d = AttrDict(d)
            if dec2float_yn == 'Y': d = dec_2_float(d)
            return d
        d = AttrDict({k: AttrDictConv(v, max_depth, current_depth + 1, dec2float_yn) for k, v in d.items()})
        if dec2float_yn == 'Y': d = dec_2_float(d)
        return d
    elif isinstance(d, list):
        # For large lists, limit processing
        if len(d) > 1000:
            print(f"🔴 GILFOYLE WARNING: Large list ({len(d)} items) - using shallow conversion")
            return d  # Return unconverted list to prevent memory issues
        d = [AttrDictConv(item, max_depth, current_depth + 1, dec2float_yn) for item in d]
        if dec2float_yn == 'Y': d = dec_2_float(d)
        return d
    else:
        return d

#<=====>#
 
def narc(max_secs=1.0, uniq_id=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # ENTRY LOG
            log_name = f'logs/debug.log'
            if uniq_id:
                log_name = f'logs/debug_{uniq_id}.log'
            msg = f"{dttm_get()} ==> CALL {uniq_id} {func.__name__}"
            # write_it(log_name, msg)
            # print(msg)
            start = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            if elapsed > max_secs:
                print(f"[SLOW] {func.__name__} took {elapsed:.2f} seconds")
            return result
        return wrapper
    return decorator

#<=====>#

def HasVal(val: Any = None) -> bool:
    """
    Check if a value is non-empty.
    Returns True if:
    - String with length > 0
    - Dict with length > 0
    - List with length > 0
    - Tuple with length > 0
    - Any non-None, non-empty value
    """
    if val is None:
        return False
    elif isinstance(val, (str, dict, list, tuple)):
        return bool(len(val))
    return val is not None and val != ''

#<=====>#

def AllHaveVal(vals: Optional[Union[Any, List[Any]]] = None, itemize_yn: str = 'N') -> bool:
    """
    Check if all values have non-empty values using HasVal.
    itemize_yn - if 'Y', prints validation results for each item
    """
    if isinstance(vals, list):
        for x in vals:
            r = HasVal(x)
            if itemize_yn == 'Y':
                print(f'r : {r}, x : {x}')
            if not r:
                return False
        return True
    return HasVal(vals)

#<=====>#

def is_valid_email(email: str) -> bool:
    """Check if string is a valid email address."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

#<=====>#

def is_valid_path(path: str) -> bool:
    """Check if string is a valid file system path."""
    try:
        # Normalize the path to handle different path separators
        normalized_path = os.path.normpath(path)
        return os.path.exists(os.path.dirname(normalized_path))
    except SystemExit:
        raise  # Never catch SystemExit
    except BaseException as e:
        # Fallback error handling - log and return False for path validation failure
        print(f"⚠️ Path validation error: {e}")
        traceback.print_exc()
        return False

#<=====>#

def DictKeyValIfElse(in_dict: Dict, k: str, d: Any) -> Any:
    """Return value if key is present and has value, else return default."""
    try:
        if k in in_dict and in_dict[k]:
            return in_dict[k]
        return d
    except Exception as e:
        print(f'DictKeyValIfElse ==> errored... {e}')
        traceback.print_exc()
        sys.exit(1)

#<=====>#

def DictKeyValFill(in_dict: Dict, k: str, v: Any) -> Any:
    """Build key if absent or fill with default value if empty."""
    try:
        if k not in in_dict or not in_dict[k]:
            in_dict[k] = v
        return in_dict[k]
    except Exception as e:
        print(f'DictKeyValFill ==> errored... {e}')
        traceback.print_exc()
        sys.exit(1)

#<=====>#

def DictKey(in_dict: Dict, k: str) -> bool:
    """Check if key exists in dictionary."""
    try:
        return k in in_dict
    except Exception as e:
        print(f'DictKey ==> errored... {e}')
        traceback.print_exc()
        sys.exit(1)

#<=====>#

def DictKeyVal(in_dict: Dict, k: str) -> bool:
    """Check if key exists in dictionary."""
    try:
        return k in in_dict
    except Exception as e:
        print(f'DictKey ==> errored... {e}')
        traceback.print_exc()
        sys.exit(1)

#<=====>#

def DictKeyDel(in_dict: Dict, k: str) -> bool:
    """Delete key from dictionary if it exists."""
    try:
        if k in in_dict:
            del in_dict[k]
            return True
        return False
    except Exception as e:
        print(f'DictKeyDel ==> errored... {e}')
        traceback.print_exc()
        sys.exit(1)

#<=====>#

def DictKeyValMult(in_dict: Dict, ks: List[str]) -> bool:
    """Check if all keys exist and have non-None values."""
    return all(DictKeyVal(in_dict, k) for k in ks)

#<=====>#

def DictContainsKeys(in_dict: Dict = {}, ks: Union[str, List[str]] = []) -> bool:
    """
    Check if all keys in ks are present in in_dict.
    ks can be either a single key or list of keys.
    """
    if isinstance(ks, str):
        ks = [ks]
    return set(ks).issubset(in_dict.keys())

#<=====>#

def DictValCheck(in_dict: Dict = {}, ks: Union[str, List[str]] = [], show_yn: str = 'N') -> bool:
    """
    Verify all specified values in dict have value.
    ks - allows specified keys to be checked
    show_yn - if 'Y', prints keys with no value
    """
    if not HasVal(ks):
        return True
        
    if isinstance(ks, str):
        ks = [ks]
        
    for k in ks:
        if k not in in_dict:
            return False
        v = in_dict[k]
        if not HasVal(v):
            if show_yn == 'Y':
                print(f'{k} : {v}')
            return False
    return True

#<=====>#

def get_unix_timestamp() -> int:
    """Return current Unix timestamp (seconds since epoch)"""
    return int(time.time())

#<=====>#

def conv_utc_timestamp_to_unix(utc_timestamp) -> int:
    """Convert UTC timestamp string to Unix timestamp - FIXED TO PREVENT EPOCH CORRUPTION"""
    if not utc_timestamp:
        # 🔴 CORRUPTION FIX: Return current timestamp instead of 0 to prevent epoch corruption
        import time
        return int(time.time())
    
    try:
        dt_obj = datetime.datetime.fromisoformat(str(utc_timestamp).replace('Z', '+00:00'))
        # Make it timezone aware (UTC)
        dt_obj = dt_obj.replace(tzinfo=datetime.timezone.utc)
        unix_timestamp = int(dt_obj.timestamp())
        
        # 🔴 VALIDATION: Ensure timestamp is reasonable (after 2020)
        if unix_timestamp < 1577836800:  # 2020-01-01 00:00:00 UTC
            import time
            return int(time.time())
            
        return unix_timestamp
    except (ValueError, AttributeError, OSError) as e:
        # 🔴 ERROR HANDLING: Return current timestamp for any conversion errors
        import time
        return int(time.time())

#<=====>#

def dttm_get():
    """Get current UTC datetime as formatted string"""
    return dt.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

#<=====>#

def dttm_unix():
    """Get current UTC datetime as Unix timestamp"""
    return int(time.time())

#<=====>#

def dttm_utc_get():
    """Get current UTC datetime"""
    return dt.now(timezone.utc)

#<=====>#

def now_utc_get():
    """Get current UTC datetime"""
    return dt.now(timezone.utc)

#<=====>#

def dec(value):
    """Convert value to Decimal with proper precision"""
    if value is None:
        return decimal.Decimal('0')
    return decimal.Decimal(str(value))

#<=====>#

def dec_2_float(data):
    """Convert decimal values to float in data structure (dict, list, or single value)"""
    if data is None:
        return data
    elif isinstance(data, decimal.Decimal):
        return float(data)
    elif isinstance(data, dict):
        return {k: dec_2_float(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [dec_2_float(item) for item in data]
    else:
        return data

#<=====>#

def format_disp_age(age_mins):
    """Format age in minutes as compact human-readable string.

    Rules:
    - >= 1 day:  "Xd Yh" (e.g., "128d 12h")
    - >= 1 hour: "H:MM"
    - < 1 hour:  "Mm"
    """
    if age_mins is None:
        return "unknown"

    try:
        age_mins = int(age_mins)
    except Exception:
        return "unknown"

    days = age_mins // (24 * 60)
    # Clamp extreme ages to a max display of 999 days for alignment
    if days >= 999:
        return "999d 0h"
    hours = (age_mins % (24 * 60)) // 60
    minutes = age_mins % 60

    if days > 0:
        return f"{days}d {hours}h"
    if hours > 0:
        return f"{hours}:{minutes:02d}"
    return f"{minutes}m"

#<=====>#

def format_disp_age2(elapsed_seconds):
    """Enhanced age formatting for display"""
    if elapsed_seconds is None:
        return "unknown"
    
    elapsed_seconds = int(elapsed_seconds)
    # Clamp extreme/unknown ages to a max display of 999 days for alignment
    max_days = 999
    max_secs = max_days * 86400
    if elapsed_seconds >= max_secs:
        return f"{max_days}d 0h"
    
    if elapsed_seconds < 60:
        return f"{elapsed_seconds}s"
    elif elapsed_seconds < 3600:
        minutes = elapsed_seconds // 60
        seconds = elapsed_seconds % 60
        return f"{minutes}:{seconds:02d}"
    elif elapsed_seconds < 86400:
        hours = elapsed_seconds // 3600
        minutes = (elapsed_seconds % 3600) // 60
        return f"{hours}:{minutes:02d}:00"
    else:
        days = elapsed_seconds // 86400
        hours = (elapsed_seconds % 86400) // 3600
        return f"{days}d {hours}h"

#<=====>#

def format_disp_age3(elapsed_seconds):
    """Uniform age formatting: 123d HH:MM with smart truncation for column alignment"""
    if elapsed_seconds is None:
        return "unknown"
    
    elapsed_seconds = int(elapsed_seconds)
    # Clamp extreme/unknown ages to a max display of 999 days
    max_days = 999
    max_secs = max_days * 86400
    if elapsed_seconds >= max_secs:
        return f"{max_days}d"
    
    total_minutes = elapsed_seconds // 60
    
    if total_minutes < 60:
        # Less than 1 hour: show just minutes
        return f"{total_minutes}m"
    elif total_minutes < 1440:  # Less than 24 hours (1440 minutes)
        # 1+ hours but less than 1 day: show HH:MM
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return f"{hours:02d}:{minutes:02d}"
    else:
        # 1+ days: show 123d HH:MM
        days = total_minutes // 1440
        remaining_minutes = total_minutes % 1440
        hours = remaining_minutes // 60
        minutes = remaining_minutes % 60
        return f"{days}d {hours:02d}:{minutes:02d}"

#<=====>#

def print_adv(lines=1):
    """Advanced print with line control"""
    for _ in range(lines):
        print()

#<=====>#

def left(string, length):
    """Get left portion of string"""
    if string is None:
        return ""
    return str(string)[:length]

#<=====>#

def dir_val(path):
    """Validate/create directory from file path"""
    if path is None:
        return
    
    # Extract directory from file path
    directory = os.path.dirname(path)
    
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

#<=====>#

def beep(count=1):
    """System beep"""

    for _ in range(count):
        if sys.platform.startswith('win'):
            import winsound
            winsound.Beep(1000, 200)
            print('beep()')
        else:
            print('\a', end='', flush=True)
            print('beep()')
            time.sleep(0.2)

#<=====>#

def fatal_error_exit(error_msg, file_path=None, func_name=None, line_no=None):
    """
    🔴 GILFOYLE'S ENHANCED FATAL ERROR HANDLER
    
    Replaces degraded graceful error handling with proper fatal termination.
    Provides comprehensive debugging information for immediate problem identification.
    
    Args:
        error_msg (str): Description of the critical error
        file_path (str): Source file where error occurred (__file__)
        func_name (str): Function name where error occurred
        line_no (int): Line number where error occurred
    """
    import traceback
    import sys
    import os
    
    print(f'\n🔴 ===== CRITICAL FATAL ERROR ===== 🔴')
    print(f'🔴 ERROR: {error_msg}')
    print(f'🔴 TIMESTAMP: {dttm_get()}')
    
    if file_path:
        print(f'🔴 FILE: {os.path.basename(file_path)}')
    else:
        print(f'🔴 FILE: Unknown')
        
    if func_name:
        print(f'🔴 FUNCTION: {func_name}')
    else:
        print(f'🔴 FUNCTION: Unknown')
        
    if line_no:
        print(f'🔴 LINE: {line_no}')
    else:
        print(f'🔴 LINE: Unknown')
    
    print(f'🔴 TRACEBACK:')
    traceback.print_exc()
    
    print(f'🔴 STACK TRACE:')
    traceback.print_stack()
    
    beep(3)
    
    print(f'🔴 BOT TERMINATING - MANUAL INTERVENTION REQUIRED')
    print(f'🔴 ===== FATAL ERROR TERMINATION ===== 🔴\n')
    
    sys.exit(1)

#<=====>#

def simple_error_handler(error):
    """
    Simple error handler that prints the error and stack trace.
    
    Args:
        error: Exception or error message
    """
    print(f"\n===== ERROR =====")
    print(f"ERROR TYPE: {type(error).__name__}")
    print(f"ERROR MESSAGE: {str(error)}")
    print(f"TIMESTAMP: {dttm_get()}")
    
    print(f"TRACEBACK:")
    traceback.print_exc()
    
    beep(1)
    print(f"===== END ERROR =====\n")
    
    # Hard exit with error
    sys.exit(f"FATAL ERROR: {type(error).__name__}: {str(error)}")

#<=====>#

def fatal_error(error):
    """
    Simple error handler that always exits.
    """
    simple_error_handler(error)

#<=====>#

def speak(text, speak_enabled: bool = False):
    """Text-to-speech obeying settings; safe on low-memory errors.

    Args:
        text: message to speak
        speak_enabled: optional explicit flag; if None, callers should gate by settings
    """
    if speak_enabled is not None and speak_enabled is not True:
        print(f"SPEAK ({speak_enabled}): {text}")
        return
    try:
        if sys.platform.startswith('win'):
            import pyttsx3
            engine = pyttsx3.init()
            engine.say(str(text))
            engine.runAndWait()
            print(f"SPEAK ({speak_enabled}): {text}")
        else:
            # For non-Windows, just print the text
            print(f"SPEAK ({speak_enabled}): {text}")
    except Exception as _e:
        # Fail silently to avoid crashing trading loop on COM/OOM issues
        pass

#<=====>#

def speak_async(text, speak_enabled: bool = False):
    """Async text-to-speech (simplified - just calls speak for now) obeying settings"""
    speak(text, speak_enabled=speak_enabled)

#<=====>#

def play_cash():
    """Play cash register sound for winning trades"""

    import winsound
    sound_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sounds', 'cashreg.wav')
    if os.path.exists(sound_path):
        winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
    else:
        # Fallback to beeps if sound file missing
        beep(3)  # Audio alert for missing sound file

#<=====>#

def play_thunder():
    """Play thunder sound for losing trades"""

    import winsound
    sound_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sounds', 'thunder.wav')
    if os.path.exists(sound_path):
        winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
    else:
        # Fallback to beeps if sound file missing
        beep(3)

#<=====>#

def gen_guid(self):
    """🔴 UTILITY - Extracted from cls_bot.py (~3 lines)
    
    Generates a unique GUID for BOT instance identification.
    
    LOW RISK: Simple UUID generation utility
    - Creates unique identifier string
    - Used for BOT instance tracking
    """
    return str(uuid.uuid4())

#<=====>#

def calc_chg_pct(old_val, new_val, dec_prec=2):
    """🔴 UTILITY - Extracted from cls_bot.py (~3 lines)
    
    Calculates percentage change between two values.
    
    LOW RISK: Mathematical utility function
    - Calculates percentage change with specified precision
    - Used throughout system for profit/loss calculations
    - Core mathematical utility for price change tracking
    """
    chg_pct = round((((new_val - old_val) / old_val) * 100), dec_prec)
    return chg_pct

#<=====>#

def write_it(fullfilename, msg):
    dir_val(fullfilename)
    with open(fullfilename, 'a') as fw:
        fw.writelines(msg)
        fw.writelines('\n')
        fw.close()
    return


#<=====>#

def writeit(self, fullfilename, msg):
    """🔴 UTILITY - Extracted from cls_bot.py (~8 lines)
    
    Simple file writing utility with directory creation.
    
    LOW RISK: File writing utility
    - Creates directories if they don't exist
    - Appends message to file with newline
    - Used for logging and file output
    """
    dir_val(fullfilename)
    with open(fullfilename, 'a') as fw:
        fw.writelines(msg)
        fw.writelines('\n')
        fw.close()
    return

#<=====>#

def get_lib_func_secs_max(self, lib_name=None, func_name=None):
    """🔴 UTILITY - Extracted from cls_bot.py (~10 lines)
    
    Gets function execution time limits from debug settings.
    
    LOW RISK: Performance monitoring utility
    - Retrieves function timeout limits from settings
    - Used for performance monitoring and debugging
    - Supports library-specific and function-specific limits
    """
    func_str = f'get_lib_func_secs_max(lib_name={lib_name}, func_name={func_name})'
    dst, debug_settings = self.debug_settings_get()
    if lib_name and func_name:
        lib_secs_max = debug_settings.get_ovrd2(in_dict=dst.elapse_max, in_key=lib_name, in_key2=func_name)
    elif lib_name:
        lib_secs_max = debug_settings.get_ovrd2(in_dict=dst.elapse_max, in_key=lib_name, in_key2=None)
    else:
        lib_secs_max = debug_settings.get_ovrd2(in_dict=dst.elapse_max, in_key=None, in_key2=None)
    return lib_secs_max 



#<=====>#

# Export all functions for easy importing
__all__ = [
    # Dictionary utilities
    'AttrDict', 'AttrDictEnh', 'AttrDictConv', 'DictKey', 'EmptyObject',
    
    # Time utilities
    'get_unix_timestamp', 'conv_utc_timestamp_to_unix', 'dttm_get', 'now_utc_get',
    
    # Conversion utilities  
    'dec', 'dec_2_float',
    
    # Display utilities
    'format_disp_age', 'format_disp_age2', 'print_adv',
    
    # String utilities
    'left',
    
    # File utilities
    'dir_val',
    
    # Sound utilities
    'beep', 'speak', 'speak_async', 'play_cash', 'play_thunder',
    
    # Error handling
    'fatal_error_exit'
]

#<=====>#

if __name__ == '__main__':
    import os
    error_msg = f"""
=== LIBRARY MODULE DIRECT EXECUTION ===
File: {os.path.basename(__file__)}
Function: __main__
Timestamp: {dttm_get()}
Issue: Library module should not be run directly
Module Path: {__file__}
======================================
"""
    print(error_msg)
    beep(3)  # Audio alert for immediate attention
    sys.exit(f"LIBRARY MODULE DIRECT EXECUTION EXIT - File: {os.path.basename(__file__)}, Reason: Library module run directly")

#<=====>#
