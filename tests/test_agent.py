import entities as e
import unittest
import os
from time import sleep

class TestAgent(unittest.TestCase):
	def setUp(self):
		map_object = e.Map(10)
		dispatch_object = e.Dispatch(map_object)
		self.agent = e.Agent(e.Point(10,1,1), dispatch_object)
	
	
	def tearDown(self):
		self.agent.exit()


	def test_subprocess(self):
		assert os.getpid() != self.agent.process.pid

	def test_move_during_tick(self):
		original_location = self.agent.location
		self.agent.tick()
		sleep(1)
		self.agent.tick()
		current_location = self.agent.location
		assert current_location != original_location

	def test_exit_of_child(self):
		for x in xrange(0,40):
			self.agent.tick()
			sleep(.1)
		assert not self.agent.alive
		

	
