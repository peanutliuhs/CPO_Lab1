import unittest
from dynamicArray import DynamicArray
from hypothesis import given
import hypothesis.strategies as st


class Testfunction(unittest.TestCase):

    def test_add(self):
        dyArr = DynamicArray()
        self.assertEqual(dyArr.insert(0, 1), [1])
        self.assertEqual(dyArr.insert(1, 4), [1, 4])
        self.assertEqual(dyArr.insert(2, 5), [1, 4, 5])
        self.assertEqual(dyArr.insert(3, 3), [1, 4, 5, 3])

    def test_delete(self):
        dyArr = DynamicArray()
        lst = [1, 4, 5, 3]
        dyArr.from_list(lst)
        self.assertEqual(dyArr.deleteindex(2), [1, 4, 3])
        self.assertEqual(dyArr.deletevalue(4), [1, 3])

    def test_size(self):
        dyArr = DynamicArray()
        lst = [1, 4, 5, 3]
        dyArr.from_list(lst)
        self.assertEqual(dyArr.size(), 4)

    def test_reverse(self):
        dyArr = DynamicArray()
        lst = [1, 4, 5, 3]
        dyArr.from_list(lst)
        self.assertEqual(dyArr.reverse(), [3, 5, 4, 1])

    def test_from_list(self):
        lst = [1, 4, 5, 3]
        dyArr = DynamicArray()
        dyArr.from_list(lst)
        self.assertEqual(dyArr.to_list(), lst)

    def test_to_list(self):
        dyArr = DynamicArray()
        self.assertEqual(dyArr.to_list(), [])
        lst = [1, 4, 5, 3]
        dyArr.from_list(lst)
        ls = dyArr.to_list()
        ls1 = []
        for i in range(dyArr.size()):
            ls1.append(dyArr.A[i])
        self.assertEqual(ls1, ls)

    def test_find(self):
        dyArr = DynamicArray()
        lst = [1, 4, 5, 3]
        dyArr.from_list(lst)
        self.assertEqual(dyArr.find_value(2), 5)
        self.assertEqual(dyArr.find_key(5), 2)

    def test_filter_func(self):
        dyArr = DynamicArray()
        lst = [1, 4, 5, 3]
        dyArr.from_list(lst)
        self.assertEqual(dyArr.filter_func(dyArr.value_is_odd), [1, 5, 3])
        self.assertEqual(dyArr.filter_func(dyArr.value_is_even), [4])
        self.assertEqual(dyArr.filter_func(dyArr.is_sqr), [1, 4])

    def test_map_func(self):
        dyArr = DynamicArray()
        lst = [1, 4, 5, 3]
        dyArr.from_list(lst)
        self.assertEqual(dyArr.map_func(dyArr.square), [1, 16, 25, 9])

    def test_reduce_func(self):
        dyArr = DynamicArray()
        lst = [1, 4, 5, 3]
        dyArr.from_list(lst)
        self.assertEqual(dyArr.reduce_func(dyArr.add), 13)

    def test_iter(self):
        dyArr1 = DynamicArray()
        dyArr2 = DynamicArray()
        lst = [1, 4, 5, 3]
        dyArr1.from_list(lst)
        dyArr2.from_list(lst)
        dyArr1.iter()
        dyArr2.iter()
        self.assertEqual(dyArr1.next(), 1)
        self.assertEqual(dyArr1.next(), 4)
        self.assertEqual(dyArr2.next(), 1)
        self.assertEqual(dyArr2.next(), 4)
        self.assertEqual(dyArr1.next(), dyArr2.next())

    def test_mempty(self):
        dyArr = DynamicArray()
        lst = [1, 4, 5, 3]
        dyArr.from_list(lst)
        self.assertEqual(dyArr.mempty(), [])

    def test_mconcat(self):
        dyArr1 = DynamicArray()
        dyArr2 = DynamicArray()
        dyArr1.from_list([])
        self.assertEqual(dyArr1.mconcat([]), [])
        self.assertEqual(dyArr1.mconcat([1, 4]), [1, 4])
        arr2 = dyArr2.from_list([5, 3])
        self.assertEqual(dyArr1.mconcat(arr2), [1, 4, 5, 3])

    @given(st.lists(st.integers()))
    def test_from_list_to_list(self, lst):
        dyArr = DynamicArray()
        arr = dyArr.from_list(lst)
        self.assertEqual(lst, arr)

    @given(st.lists(st.integers()))
    def test_len_size(self, lst):
        dyArr = DynamicArray()
        dyArr.from_list(lst)
        self.assertEqual(dyArr.size(), len(lst))

    @given(st.lists(st.integers()))
    def test_monoid_identity(self, lst):
        dyArr1 = DynamicArray()
        dyArr2 = DynamicArray()
        arr = dyArr1.from_list(lst)
        arr2 = dyArr2.from_list([])
        self.assertEqual(dyArr1.mconcat(arr2), dyArr1.to_list())
        self.assertEqual(dyArr2.mconcat(arr), dyArr1.to_list())
        arr2 = dyArr2.from_list([])
        self.assertEqual(dyArr1.mconcat(arr2),
                         dyArr2.mconcat(arr))

    @given(st.lists(st.integers()),
           st.lists(st.integers()), st.lists(st.integers()))
    def test_monoid_associativity(self, lst1, lst2, lst3):
        dyArr1 = DynamicArray()
        dyArr2 = DynamicArray()
        dyArr3 = DynamicArray()
        dyArr1.from_list(lst1)
        b = dyArr2.from_list(lst2)
        c = dyArr3.from_list(lst3)
        dyArr1.mconcat(b)
        arr1 = dyArr1.mconcat(c)
        dyArr1.from_list(lst1)
        arr2 = dyArr1.mconcat(dyArr2.mconcat(c))
        self.assertEqual(arr1, arr2)
