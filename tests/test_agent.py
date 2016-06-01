import entities as e
import unittest
import os
from time import sleep

class TestAgent(unittest.TestCase):
    def setUp(self):
        self.dispatch_object = e.Dispatch()
        self.agent = e.Agent(e.Point(10,1,1), self.dispatch_object, hunger_percent=100)
	
	
    def tearDown(self):
        self.agent.exit()


    def test_subprocess(self):
        assert os.getpid() != self.agent.process.pid


    def test_move_during_tick(self):
        original_location = self.agent.location
        self.agent.tick()
        sleep(.1)
        self.agent.tick()
        current_location = self.agent.location
        assert current_location != original_location


    def test_exit_of_child(self):
        for x in xrange(0,10):
            self.agent.tick()
            sleep(.1)
        assert not self.agent.alive

    
    def test_child_eating(self):
        assert self.agent.alive
        self.dispatch_object.create_item_at('food/plant/apple', e.Point(10,2,2))
        # There's food, and we should already be hungry
        for x in xrange(0,10):
            self.agent.tick()
            sleep(.1)
        assert self.agent.alive
        
        
                
		

	
