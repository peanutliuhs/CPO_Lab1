import math
from functools import reduce
from typing import Any, List, Callable


class DynamicArray:
    """A dynamic array class akin to a simplified Python list."""

    def __init__(self) -> None:
        """Create an empty array."""
        self.n = 0          # count actual elements
        self.capacity = 1   # default array capacity
        self.A = self._make_array(self.capacity)   # low-level array

    def is_empty(self) -> bool:
        """ Return True if array is empty"""
        return self.n == 0

    def _len_(self) -> int:
        """Return numbers of elements stored in the array."""
        return self.n

    def _getitem_(self, i: int) -> Any:
        """Return element at index i."""
        if not 0 <= i < self.n:
            # Check it i index is in bounds of array
            raise ValueError('invalid index')
        return self.A[i]

    def append(self, obj: int) -> None:
        """Add object to end of the array."""
        if self.n == self.capacity:
            # Double capacity if not enough room
            self._resize(2 * self.capacity)
        self.A[self.n] = obj  # Set self.n index to obj
        self.n += 1

    def _resize(self, c: int) -> None:
        """Resize internal array to capacity c."""
        B = self._make_array(c)
        for k in range(self.n):
            B[k] = self.A[k]
        self.A = B
        self.capacity = c

    def _make_array(self, c: int) -> List[Any]:
        """Return new array with capacity c."""
        return c * [None]

    def _print(self) -> None:
        """Print the array."""
        for i in range(self.n):
            print(self.A[i], end=' ')
        print()

    # 1. add a new element
    def insert(self, k: int, value: int) -> List[Any]:
        """Insert value at position k."""
        if self.n == self.capacity:
            self._resize(2 * self.capacity)
        for j in range(self.n, k, -1):
            self.A[j] = self.A[j - 1]
        self.A[k] = value
        self.n += 1
        return self.A[:self.n]

    # 2. remove an element
    def deleteindex(self, index: int) -> List[int]:
        """Remove item at index (default first)."""
        if (self._len_() < index):
            raise ValueError('index is out of range')
        if index >= self.n or index < 0:
            raise ValueError('invalid index')
        for i in range(index, self.n - 1):
            self.A[i] = self.A[i + 1]
        self.A[self.n - 1] = None
        self.n -= 1
        return self.A[:self.n]

    def deletevalue(self, value: int) -> List[int]:
        """Remove the first occurrence of a value in the array."""
        for k in range(self.n):
            if self.A[k] == value:
                for j in range(k, self.n - 1):
                    self.A[j] = self.A[j + 1]
                self.A[self.n - 1] = None
                self.n -= 1
                return self.A[:self.n]
        raise ValueError('value not found')

    # 3. size
    def size(self) -> int:
        """Return the size of the array."""
        return (self._len_())

    # 4.ismember
    def ismember(self, value: int) -> bool:
        """Check if the value is a member of the array."""
        for k in range(self.n):
            if self.A[k] == value:
                return True
        return False

    # 5.reverse
    def reverse(self) -> List[int]:
        """Reverse the array."""
        for i in range(int(self.size() / 2)):
            num = self.A[i]
            self.A[i] = self.A[self.size() - i - 1]
            self.A[self.size() - i - 1] = num
        return self.A[:self.n]

    # 6. conversion from and to python lists
    def from_list(self, lst: List[int]) -> List[int]:
        """Conversion from list to DynamicArray."""
        self.mempty()
        for i in range(len(lst)):
            self.insert(i, lst[i])
        return self.A[:self.n]

    def to_list(self) -> List[int]:
        """Conversion from DynamicArray to list"""
        lst = []
        for i in range(self.size()):
            lst.append(self.A[i])
        return lst

    # 7. find element by specific predicate
    def find_value(self, key: int) -> Any:
        """Find value by the index."""
        if key >= self.n or key < 0:
            raise ValueError('invalid index')
        return self.A[key]

    def find_key(self, value: int) -> int:
        """Find index by the value."""
        for k in range(self.n):
            if self.A[k] == value:
                return k
        return -1

    # 8. filter data structure by specific predicate
    def value_is_odd(self, n: int) -> bool:
        """Check if n is odd."""
        return n % 2 == 1

    def value_is_even(self, n: int) -> bool:
        """Check if n is even."""
        return n % 2 == 0

    def is_sqr(self, n: int) -> bool:
        """Check if n is the square of some value."""
        return math.sqrt(n) % 1 == 0

    def filter_func(self, fun: Callable[[int], Any]) -> List[int]:
        """Filter elements by given function fun."""
        arr = self.to_list()
        newlist = list(filter(fun, arr))
        return newlist

    # 9. map structure by specific function
    def square(self, x: int) -> int:
        """Calculate the square of x."""
        return x ** 2

    def map_func(self, fun: Callable[[int], Any]) -> List[int]:
        """Map the elements in the array with the given function fun."""
        arr = self.to_list()
        newlist = map(fun, arr)
        j = 0
        for i in newlist:
            self.deleteindex(j)
            self.insert(j, i)
            j = j + 1
        return self.A[:self.n]

    # 10. reduce __ process structure elements to build a return value by
    # specific functions
    def add(self, x: int, y: int) -> int:
        """Calculate the sum of x and y."""
        return x + y

    def reduce_func(self, func: Callable[[int, int], int]) -> int:
        """Process the elements in the array by the given function fun."""
        arr = self.to_list()
        sum = reduce(func, arr)
        return sum

    # 11. iterator
    def iter(self) -> None:
        """Build an iterator over the DynamicArray."""
        self.num = -1

    def next(self) -> Any:
        """Return the next element of the DynamicArray."""
        if self.num >= self.size():
            raise StopIteration
        self.num = self.num + 1
        tmp = self.A[self.num]
        return tmp

    # 12. mempty and mconcat
    def mempty(self) -> List[int]:
        """Set the DynamicArray to empty."""
        self.n = 0
        return self.A[:self.n]

    def mconcat(self, Arr: List[int]) -> List[int]:
        """Concat the elements in two dynamic arrays."""
        j = self.size()
        for i in range(len(Arr)):
            self.insert(j, Arr[i])
            j = j + 1
        return self.A[:self.n]
