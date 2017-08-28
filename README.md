# Too Deep

Too Deep is a Python re-implementation of Tarn Adams' Dwarf Fortress.[1][2]  It is currently in a state of extreme infancy and it currently not playable.

Dwarf Fortress has consumed hundreds, if not thousands, of hours of my life, and is inspiring in it's depth and scope.  It's biggest downside, however, it that it does not take advantage of modern multiprocessor machines.  This leads to significant slow-downs when simulating larger maps and fortresses.  Rumor has it that Tarn is not interested in taking advantages of the parallelization options of modern processors.  I certainly haven't seen any evidence of improvement in this area.

I started Too Deep as a demonstration of Dwarf Fortress mechanics in a modern, multiprocessing implementation.

Currently not much of Dwarf Fortress has actually been duplicated.  The one thing that *is* working is the multi-processing.  All "agents" (all mobile characters) are implemented as sub-processes.  All path finding and decision making for the individual agents happens in the sub-process, which can then be scheduled by the OS onto any of the available cores.  Communication between the sub-processes and the rest of the game happens via Python inter-process communication primitives.

The entire application has relatively good unit test coverage.  I'm trying to keep coverage at 85% across the entire project.

[1] http://bay12games.com/dwarves/
[2] https://en.wikipedia.org/wiki/Dwarf_Fortress


