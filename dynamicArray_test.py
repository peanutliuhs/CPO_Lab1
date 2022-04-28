import unittest
from dynamicArray import DynamicArray
from hypothesis import given
import hypothesis.strategies as st


class Testfunction(unittest.TestCase):

    def test_add(self):
        dyArr = DynamicArray()
        self.assertEqual(dyArr.insert(0, 1).to_list(), [1])
        self.assertEqual(dyArr.insert(1, 4).to_list(), [1, 4])
        self.assertEqual(dyArr.insert(2, 5).to_list(), [1, 4, 5])
        self.assertEqual(dyArr.insert(3, 3).to_list(), [1, 4, 5, 3])

    def test_delete(self):
        dyArr = DynamicArray()
        lst = [1, 4, 5, 3]
        arr = dyArr.from_list(lst)
        self.assertEqual(arr.deleteindex(2).to_list(), [1, 4, 3])
        self.assertEqual(arr.deletevalue(4).to_list(), [1, 3])

    def test_size(self):
        dyArr = DynamicArray()
        lst = [1, 4, 5, 3]
        arr = dyArr.from_list(lst)
        self.assertEqual(arr.size(), 4)

    def test_reverse(self):
        dyArr = DynamicArray()
        lst = [1, 4, 5, 3]
        arr = dyArr.from_list(lst)
        self.assertEqual(arr.reverse().to_list(), [3, 5, 4, 1])

    def test_from_list(self):
        lst = [1, 4, 5, 3]
        dyArr = DynamicArray()
        arr = dyArr.from_list(lst)
        self.assertEqual(arr.to_list(), lst)

    def test_to_list(self):
        dyArr = DynamicArray()
        self.assertEqual(dyArr.to_list(), [])
        lst = [1, 4, 5, 3]
        arr = dyArr.from_list(lst)
        ls = arr.to_list()
        ls1 = []
        for i in range(arr.size()):
            ls1.append(arr.A[i])
        self.assertEqual(ls1, ls)

    def test_find(self):
        dyArr = DynamicArray()
        lst = [1, 4, 5, 3]
        arr = dyArr.from_list(lst)
        self.assertEqual(arr.find_value(2), 5)
        self.assertEqual(arr.find_key(5), 2)

    def test_filter_func(self):
        dyArr = DynamicArray()
        lst = [1, 4, 5, 3]
        arr = dyArr.from_list(lst)
        self.assertEqual(arr.filter_func(arr.value_is_odd), [1, 5, 3])
        self.assertEqual(arr.filter_func(arr.value_is_even), [4])
        self.assertEqual(arr.filter_func(arr.is_sqr), [1, 4])

    def test_map_func(self):
        dyArr = DynamicArray()
        lst = [1, 4, 5, 3]
        arr = dyArr.from_list(lst)
        self.assertEqual(arr.map_func(arr.square).to_list(), [1, 16, 25, 9])

    def test_reduce_func(self):
        dyArr = DynamicArray()
        lst = [1, 4, 5, 3]
        arr = dyArr.from_list(lst)
        self.assertEqual(arr.reduce_func(arr.add), 13)

    def test_iter(self):
        dyArr = DynamicArray()
        i = iter(dyArr)
        self.assertRaises(StopIteration, lambda: next(i))

    def test_mempty(self):
        dyArr = DynamicArray()
        lst = [1, 4, 5, 3]
        arr = dyArr.from_list(lst)
        self.assertEqual(arr.mempty().to_list(), [])

    def test_mconcat(self):
        dyArr = DynamicArray()
        arr = dyArr.from_list([])
        self.assertEqual(arr.mconcat([]).to_list(), [])
        self.assertEqual(arr.mconcat([1, 4]).to_list(), [1, 4])
        arr2 = dyArr.from_list([5, 3])
        self.assertEqual(arr.mconcat(arr2).to_list(), [1, 4, 5, 3])

    @given(st.lists(st.integers()))
    def test_from_list_to_list(self, lst):
        dyArr = DynamicArray()
        arr = dyArr.from_list(lst)
        tmp_lst = arr.to_list()
        self.assertEqual(lst, tmp_lst)

    @given(st.lists(st.integers()))
    def test_len_size(self, lst):
        dyArr = DynamicArray()
        arr = dyArr.from_list(lst)
        self.assertEqual(arr.size(), len(lst))

    @given(st.lists(st.integers()))
    def test_monoid_identity(self, lst):
        dyArr = DynamicArray()
        arr = dyArr.from_list(lst)
        arr2 = dyArr.from_list([])
        self.assertEqual(arr.mconcat(arr2).to_list(), arr.to_list())
        self.assertEqual(arr2.mconcat(arr).to_list(), arr.to_list())
        arr2 = dyArr.from_list([])
        self.assertEqual(arr.mconcat(arr2).to_list(),
                         arr2.mconcat(arr).to_list())

    @given(st.lists(st.integers()),
           st.lists(st.integers()), st.lists(st.integers()))
    def test_monoid_associativity(self, lst1, lst2, lst3):
        dyArr = DynamicArray()
        a = dyArr.from_list(lst1)
        b = dyArr.from_list(lst2)
        c = dyArr.from_list(lst3)
        arr1 = a.mconcat(b).mconcat(c)
        a = dyArr.from_list(lst1)
        arr2 = a.mconcat(b.mconcat(c))
        self.assertEqual(arr1.to_list(), arr2.to_list())
