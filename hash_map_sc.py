# Name: Dylan Bishop
# OSU Email: bishopdy@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: HashMap (Portfolio Assignment)
# Due Date: 3/12/26
# Description: An implementation of a Hash Map using chaining for collisions.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        Places a new key/value pair into the hash map. Overwrites value if key exists

        :param: key: the key of the SLNode to insert
        :param: value: the value of the SLNode to insert
        """
        # resize if load factor is too high
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)

        index = self._hash_function(key) % self._capacity
        target_bucket = self._buckets[index]

        # will be none if the key doesn't already exist
        node = target_bucket.contains(key)

        # key already exists, overwrite value
        if node is not None:
            node.value = value
        else:
            # key doesn't exist, insert new node
            target_bucket.insert(key, value)
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the HashMap to the next prime number from the given capacity

        :param: new_capacity: the new capacity of the HashMap
        """
        if new_capacity < 1:
            return

        # find the next prime if not already prime
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # preserve the old HashMap so we can read it for copying
        old_map = self._buckets
        self._capacity = new_capacity
        self._size = 0

        # essentially redo __init__ to establish a new HashMap
        self._buckets = DynamicArray()
        for i in range(self._capacity):
            self._buckets.append(LinkedList())

        # rehash all the elements from the old HashMap
        for i in range(old_map.length()):
            current_bucket = old_map[i]
            for node in current_bucket:
                self.put(node.key, node.value)

    def table_load(self) -> float:
        """
        Finds the load factor of the HashMap

        :return: the load factor as a float value
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Finds the amount of empty buckets in the HashMap

        :return: the # of empty buckets
        """
        count = 0
        # iterates through the buckets and increments counter for each empty bucket
        for i in range(self._capacity):
            if self._buckets[i].length() == 0:
                count += 1
        return count

    def get(self, key: str) -> object:
        """
        Searches for the value associated with a given key

        :param: key: the key of the node to search for

        :return: the value of the key, None if the key doesn't exist
        """
        index = self._hash_function(key) % self._capacity

        # becomes node associated with key or None if it doesn't exist
        node = self._buckets[index].contains(key)

        # matching key has an associated value (it exists)
        if node is not None:
            return node.value
        # key wasn't found
        return None

    def contains_key(self, key: str) -> bool:
        """
        Determines if the key is already in the HashMap

        :param: key: the key to search for

        :return: True if it exists, False if not
        """
        if self._size == 0:
            return False

        node = self.get(key)

        if node is not None:
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes a key/value pair from the HashMap

        :param: key: the key to search for and remove
        """
        index = self._hash_function(key) % self._capacity

        # calls remove and decrements size if a remove was performed
        if self._buckets[index].remove(key) is True:
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Finds each key/value pair in the HashMap

        :return: DynamicArray containing tuples with each key/value pair
        """
        keys_and_values = DynamicArray()

        # iterate through buckets and append each key/value pair to the DynamicArray
        for i in range(self._capacity):
            for node in self._buckets[i]:
                keys_and_values.append((node.key, node.value))

        return keys_and_values

    def clear(self) -> None:
        """
        Clears the contents of the HashMap without changing capacity
        """
        # clears by replacing each bucket with a fresh, empty linked list
        for i in range(self._capacity):
            self._buckets[i] = LinkedList()
        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Finds the frequently occurring values in the DynamicArray

    :param: da: the DynamicArray to find the modes in

    :return: a tuple of a DynamicArray with the mode values
    and an integer of the number of times they appeared
    """
    map = HashMap()
    highest_frequency = 0

    # use HashMap to store the items and their frequencies
    for i in range(da.length()):
        current_item = da[i]
        # checks if the item is in the hash map, gets its value (count) if it is
        current_count = map.get(current_item)

        # .get will return None if the value doesn't exist in the map
        if current_count is None:
            current_count = 0

        # increments the number of appearances by 1 & places item/count in the map
        updated_count = current_count + 1
        map.put(current_item, updated_count)

        if updated_count > highest_frequency:
            highest_frequency = updated_count

    # initialize modes array and finds all items + their counts from HashMap
    modes = DynamicArray()
    items_and_counts = map.get_keys_and_values()

    # if an item's paired count is the highest_frequency number, append it to modes
    for i in range(items_and_counts.length()):
        item, count = items_and_counts[i]
        if count == highest_frequency:
            modes.append(item)

    return modes, highest_frequency

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
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
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

    print('\nPDF - find_mode example 1')
    print('-----------------------------')
    da = DynamicArray(['apple', 'apple', 'grape', 'melon', 'peach'])
    mode, frequency = find_mode(da)
    print(f'Input: {da}\nMode : {mode}, Frequency: {frequency}')

    print('\nPDF - find_mode example 2')
    print('-----------------------------')
    test_cases = (
        ['Arch', 'Manjaro', 'Manjaro', 'Mint', 'Mint', 'Mint', 'Ubuntu', 'Ubuntu', 'Ubuntu'],
        ['one', 'two', 'three', 'four', 'five'],
        ['2', '4', '2', '6', '8', '4', '1', '3', '4', '5', '7', '3', '3', '2']
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f'Input: {da}\nMode : {mode}, Frequency: {frequency}\n')
