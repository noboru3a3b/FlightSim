"""

Meat Engine Mood Music


MeatEngine.MoodMusic is a module for selecting music adaptively based
on the mood of the game. It is intended to support multiple players
(PyGame, BASS, FMod, OpenAL), but only PyGame's sound system is
currently supported.

Each distinct "state" that the game can be in is called a
"mood". Music can be associated with a mood, or with a transition
between moods.

At initialization time, first create an instance of the library
wrapper object (currently LibraryPyGame is the only one
supported). Then create a player object with the library as an
argument.

You then define the states ("moods") by calling addState on the player
object. You may add transitions between states if you plan on using
this feature. If you do not want music playing between states, you
don't need to set them up.

Next, assign music to the states and transitions (if any). This can be
done a directory at a time with addMusicDirectoryToState and
addMusicDirectoryToTransition. There are also methods to add
individual files to states or transitions.

Finally, call setState() to establish the initial state.

At runtime, call the player's tick() function periodically (once per
frame is convenient, but if you call it less frequently, you may get
gaps in your transitions). When a song ends, the player checks the
current mood and plays an appropriate song.

Moods can be changed by either calling setState() or pushState(). When
calling setState(), you are strictly controlling the mood of the next
song (the current song still plays to completion). This may be useful
for states that change frequently, more often than the length of a
song.

Alternately, you can use pushState(), and the player will maintain a
stack of states. As a song finishes, if the stack is more than one
mood deep, the player will see if a transition has been established
for those two states, and it will play a song from the list
associated with that transtion. When the transition song is finished,
the stack is again inspected. If there are still more than one mood
deep, another transition is played, until the stack is down to a
single mood.




"""

