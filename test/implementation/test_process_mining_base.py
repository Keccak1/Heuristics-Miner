import unittest
from implementation.process_mining_base import ProcessEvent


class ProcessEventTest(unittest.TestCase):
    
    def setUp(self):
        self.process1 = ProcessEvent('activity1', 1)
        self.process2 = ProcessEvent('activity2', 2)
        
    def acitivity_test(self):
        self.assertEqual(self.process1.activity, 'activity1')
        self.assertEqual(self.process2.activity, 'activity2')
        
    def datatime_test(self):
        self.assertEqual(self.process1.datetime, 1)
        self.assertEqual(self.process2.datetime, 2)
        
    def compare_test(self):
        self.assertTrue(self.process1 < self.process2)