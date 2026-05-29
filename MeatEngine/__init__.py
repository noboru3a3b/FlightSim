"""Meat Engine

Copyright (C) 2007, Big Dice Games

One practical definition of a "game engine" is "the code you reuse on
your second game". That's mostly tongue-in-cheek, but it isn't far
from the philosophy of what's currently included in MeatEngine.

I've included a variety of pieces of code, not because they're all
appropriate for the game you want to make, and they're certainly not
all appropriate for any particular game, but instead, each piece might
be useful for some game, or for some game-related-project.

MeatEngine is more of a toolbox than a framework - you're responsible
for the main loop of your program. Some of the code makes certain
assumptions about being called periodically. This should not be
difficult to handle, regardless of the structure of your game.

Included (currently) are modules for adaptive music, GUI display, AI,
and low-level math. Also included is the beginnings of a ray tracer -
not that you'd want to use a ray tracer in your game (certainly not
this ray tracer, anyway), but it may be of benefit in creating
assets. Also, it serves as a test harness for the math module.


Version History
--------------------

0.0.1 - Initial packaging in advance of PyWeek5
"""

__all__ = ['MoodMusic', 'Math', 'Widgets', 'AI', 'RayTrace', 'Logic']

__version__ = "0.0.1"

__docformat__="restructuredtext en"
