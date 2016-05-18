import entities as e
import unittest
import os

class TestAgent(unittest.TestCase):
	def setUp(self):
		map_object = e.Map(10)
		dispatch_object = e.Dispatch(map_object)
		self.agent = e.Agent(e.Point(0,0,0), dispatch_object)
	
	
	def tearDown(self):
		self.agent.exit()


	def test_subprocess(self):
		assert os.getpid() != self.agent.process.pid

	
