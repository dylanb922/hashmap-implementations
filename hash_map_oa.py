# Name: Dylan Bishop
# OSU Email: bishopdy@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: HashMap (Portfolio Assignment)
# Due Date: 3/12/26
# Description: An implementation of a Hash Map using open addressing for collisions.

from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Places a new key/value pair into the HashMap, probing for a spot if needed

        :param: key: the key of the object
        :param: value: the value of the object
        """
        # resize if load factor is too high
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # find first open index or index of a matching key if it exists
        index = self._probe_for_index(key, True)
        item = self._buckets[index]

        # an open index (None or tombstone) was found
        if item is None or item.is_tombstone:
            self._buckets[index] = HashEntry(key, value)
            self._size += 1
        else:
            # a matching key value was found - update value
            item.value = value


    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the HashMap to the next prime number from the given capacity

        :param: new_capacity: the new capacity of the HashMap
        """
        if new_capacity < self._size:
            return

        # ensure capacity is prime if it isn't already
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # preserve old HashMap for copying over values
        old_map = self._buckets
        self._capacity = new_capacity
        self._size = 0

        # basically redo __init__
        self._buckets = DynamicArray()
        for i in range(self._capacity):
            self._buckets.append(None)

        # rehash all the elements from the old HashMap
        for i in range(old_map.length()):
            item = old_map[i]

            # skips over tombstones
            if item is not None and item.is_tombstone is False:
                self.put(item.key, item.value)

    def table_load(self) -> float:
        """
        Finds the load factor of the HashMap

        :return: the load factor as a float value
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Finds how many empty buckets there are in the HashMap

        :return: the number of empty buckets
        """
        # includes tombstone values as "empty" buckets
        return self._capacity - self._size

    def get(self, key: str) -> object:
        """
        Finds the value associated with a given key

        :param: key: the key to search for

        :return: the value of the key if found, None if not
        """
        index = self._probe_for_index(key, False)
        item = self._buckets[index]

        # matching key was found
        if item is not None:
            return item.value

        # key wasn't found
        return None

    def contains_key(self, key: str) -> bool:
        """
        Determines if a key exists within the HashMap

        :param: key: the key to search for

        :return: True if the key exists, False if not
        """
        if self._size == 0:
            return False

        value = self.get(key)

        # matching key has an associated value (it exists)
        if value is not None:
            return True
        # key wasn't found
        return False

    def remove(self, key: str) -> None:
        """
        Removes a determined value from the HashMap by making it a tombstone

        :param: key: the key of the object to remove
        """
        index = self._probe_for_index(key, False)
        item = self._buckets[index]

        # matching key was found (not a tombstone)
        if item is not None:
            item.is_tombstone = True
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Finds each key/value pair in the HashMap

        :return: DynamicArray containing tuples with each key/value pair
        """
        keys_and_values = DynamicArray()

        # scan through the HashMap
        for i in range(self._capacity):
            item = self._buckets[i]

            # item is not empty nor a tombstone
            if item is not None and item.is_tombstone is False:
                keys_and_values.append((item.key, item.value))

        return keys_and_values

    def clear(self) -> None:
        """
        Clears the contents of the HashMap without changing capacity
        """
        # replaces each bucket with an empty spot
        for i in range(self._capacity):
            self._buckets[i] = None
        self._size = 0

    def __iter__(self):
        """
        Create iterator for loop
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        """
        while self._index < self._capacity:
            item = self._buckets[self._index]

            # advance the iteration forward
            self._index += 1

            # returns item if it's not empty nor a tombstone
            if item is not None and item.is_tombstone is False:
                return item

        # exit loop if nothing was returned
        raise StopIteration

    def _probe_for_index(self, key: str, need_tombstones: bool) -> int:
        """
        Helper that searches through the DA for a matching key or open index

        :param: key: the key to search for/use as starting point
        :param: need_tombstones: tells the method to ignore or look for tombstones

        :return: the first open index, index of the matching key, or tombstone index
        """
        initial_index = self._hash_function(key) % self._capacity
        index = initial_index
        first_tombstone = None
        probe_value = 1

        # probe until existing key or first open spot is found
        while self._buckets[index] is not None:
            item = self._buckets[index]

            # saves index of the first tombstone if we need it
            if item.is_tombstone:
                if first_tombstone is None:
                    first_tombstone = index

            # key already exists in the map
            elif item.key == key:
                return index

            # continue probing through the HashMap
            index = (initial_index + probe_value ** 2) % self._capacity
            probe_value += 1

        # if a tombstone was found and we're using tombstones
        if need_tombstones is True and first_tombstone is not None:
            return first_tombstone

        # first open (None) value
        return index

# ------------------- BASIC TESTING ---------------------------------------- #


if __name__ == "__main__":

    print('\nPDF - put example 1')
    print('-------------------')
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print('\nPDF - put example 2')
    print('-------------------')
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print('\nPDF - resize example 1')
    print('----------------------')
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print('\nPDF - resize example 2')
    print('----------------------')
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f'Check that the load factor is acceptable after the call to resize_table().\n'
                  f'Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5')

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print('\nPDF - table_load example 1')
    print('--------------------------')
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print('\nPDF - table_load example 2')
    print('--------------------------')
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print('\nPDF - empty_buckets example 1')
    print('-----------------------------')
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print('\nPDF - empty_buckets example 2')
    print('-----------------------------')
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print('\nPDF - get example 1')
    print('-------------------')
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print('\nPDF - get example 2')
    print('-------------------')
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print('\nPDF - contains_key example 1')
    print('----------------------------')
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print('\nPDF - contains_key example 2')
    print('----------------------------')
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print('\nPDF - remove example 1')
    print('----------------------')
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print('\nPDF - get_keys_and_values example 1')
    print('------------------------')
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print('\nPDF - clear example 1')
    print('---------------------')
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print('\nPDF - clear example 2')
    print('---------------------')
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print('\nPDF - __iter__(), __next__() example 1')
    print('---------------------')
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print('\nPDF - __iter__(), __next__() example 2')
    print('---------------------')
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
