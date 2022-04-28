import ctypes
import math
import numpy as np
from functools import reduce
from typing import Iterator, Callable


class DynamicArray:
    """A dynamic array class akin to a simplified Python list."""

    def __init__(self):
        """Create an empty array."""
        self.n = 0       # count actual elements
        self.capacity = 1   # default array capacity
        self.A = self._make_array(self.capacity)   # low-level array

    def is_empty(self):
        """ Return True if array is empty"""
        return self.n == 0

    def _len_(self):
        """Return numbers of elements stored in the array."""
        return self.n

    def _getitem_(self, i):
        """Return element at index i."""
        if not 0 <= i < self.n:
            # Check it i index is in bounds of array
            raise ValueError('invalid index')
        return self.A[i]

    def append(self, obj):
        """Add object to end of the array."""
        if self.n == self.capacity:
            # Double capacity if not enough room
            self._resize(2 * self.capacity)
        self.A[self.n] = obj  # Set self.n index to obj
        self.n += 1

    def _resize(self, c):
        """Resize internal array to capacity c."""
        B = self._make_array(c)   # New bigger array
        for k in range(self.n):  # Reference all existing values
            B[k] = self.A[k]
        self.A = B     # Call A the new bigger array
        self.capacity = c  # Reset the capacity

    def _make_array(self, c):
        """Return new array with capacity c."""
        return (c * ctypes.py_object)()

    def _print(self):
        """Print the array."""
        for i in range(self.n):
            print(self.A[i], end=' ')
        print()

    # 1. add a new element

    def insert(self, k, value):
        """Insert value at position k."""
        if self.n == self.capacity:
            self._resize(2 * self.capacity)
        for j in range(self.n, k, -1):
            self.A[j] = self.A[j - 1]
        self.A[k] = value
        self.n += 1
        return self

    # 2. remove an element
    def deleteindex(self, index):
        """Remove item at index (default first)."""
        if (self._len_() < index):
            print("index is out of range")
            return
        if index >= self.n or index < 0:
            raise ValueError('invalid index')
        for i in range(index, self.n - 1):
            self.A[i] = self.A[i + 1]
        self.A[self.n - 1] = None
        self.n -= 1
        return self

    def deletevalue(self, value):
        """Remove the first occurrence of a value in the array."""
        for k in range(self.n):
            if self.A[k] == value:
                for j in range(k, self.n - 1):
                    self.A[j] = self.A[j + 1]
                self.A[self.n - 1] = None
                self.n -= 1
                return self
        raise ValueError('value not found')

    # 3. size
    def size(self):
        return (self._len_())

    # 4.ismember
    def ismember(self, value):
        for k in range(self.n):
            if self.A[k] == value:
                return True
        return False

    # 5.reverse
    def reverse(self):
        for i in range(int(self.size() / 2)):
            num = self.A[i]
            self.A[i] = self.A[self.size() - i - 1]
            self.A[self.size() - i - 1] = num
        return self

    # 6. conversion from and to python lists
    def from_list(self, lst):
        dyArr = DynamicArray()
        for i in range(len(lst)):
            dyArr.insert(i, lst[i])
        return dyArr

    def to_list(self):
        lst = []
        for i in range(self.size()):
            lst.append(self.A[i])
        return lst

    # 7. find element by specific predicate
    def find_value(self, key):
        if key >= self.n or key < 0:
            raise ValueError('invalid index')
        return self.A[key]

    def find_key(self, value):
        for k in range(self.n):
            if self.A[k] == value:
                return k
        return False

    # 8. filter data structure by specific predicate
    def value_is_odd(self, n):
        return n % 2 == 1

    def value_is_even(self, n):
        return n % 2 == 0

    def is_sqr(self, x):
        return math.sqrt(x) % 1 == 0

    def filter_func(self, fun):
        arr = self.to_list()
        newlist = list(filter(fun, arr))
        return newlist

    # 9. map structure by specific function
    def square(self, x):
        return x ** 2

    def map_func(self, fun):
        arr = self.to_list()
        newlist = map(fun, arr)
        dyArr = DynamicArray()
        j = 0
        for i in newlist:
            dyArr.insert(j, i)
            j = j + 1
        return dyArr

    # 10. reduce – process structure elements to build a return value by
    # specific functions
    def add(self, x, y):
        return x + y

    def reduce_func(self, func):
        arr = self.to_list()
        sum = reduce(func, arr)
        return sum

    # 11. iterator
    def __iter__(self) -> Iterator:
        self.num = 0
        return self

    def __next__(self) -> Callable:
        if self.num >= self.size():
            raise StopIteration
        tmp = self.A[self.num]
        self.num = self.num + 1
        return tmp

    # 12. mempty and mconcat
    def mempty(self):
        dyArr = DynamicArray()
        self = dyArr.from_list([])
        return self

    def mconcat(self, a):
        dyArr = DynamicArray()
        if isinstance(a, list):
            a = dyArr.from_list(a)
        j = self.size()
        for i in range(a.size()):
            self.insert(j, a.A[i])
            j = j + 1
        return self
