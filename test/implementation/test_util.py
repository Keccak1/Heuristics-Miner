import unittest
from implementation.util import unique_concatenate, unique_list

class UtilTest(unittest.TestCase):
    
    def unique_list_test(self):
        l = [1,1,2,3]
        unique_l = unique_list(l)
        self.assertEqual(unique_l, [1,2,3])
        
    def unique_concatenate_test(self):
        l1, l2  = [1,2,3], [1,2,4]
        unique_concatenate_l = unique_concatenate(l1, l2)
        self.assertEqual(unique_concatenate_l, [1,2,3,4])