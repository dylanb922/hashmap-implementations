# HashMap Implementations

Two separate HashMap implementations using OOP in Python. Separate chaining is based on a Linked List structure, handling collisions by storing the value as a node in a linked list. Open Addressing uses a dynamic array to store values and handles collisions by probing for the next available spot.

## Project Details

* `a6_include.py` - Linked List and Dynamic Array data structures provided by CS 261
* `hash_map_oa.py` - HashMap implementation using Open Addressing 
* `hash_map_sc.py` - HashMap implementation using Separate Chaining

## Requirements

* Python 3.8+

## Usage

* Import the included file(s) to your project.
* Create an object of the HashMap class.
* Use any of the supplied methods to store/read data.

### Example

```python
from a6_include import DynamicArray, hash_function_1
from hash_map_sc import HashMap, find_mode

# Initialize HashMap
hm = HashMap(11, hash_function_1)
hm.put("apple", 10)
hm.put("banana", 20)
print(hm.get("apple"))        # Output: 10
print(hm.contains_key("fig")) # Output: False
```

## Acknowledgements

Skeleton code and project design provided by Oregon State University's Data Structures (CS 261) class.
