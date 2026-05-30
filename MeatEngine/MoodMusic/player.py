import random
import glob

class Player:
    def __init__(self, musicLibrary):
        
        # states will be keyed by name
        self.states={}
        
        # transitions will be keyed by a tuple (from,to) of names of
        # the states being transitioned between. Instead of a state
        # name, None may also be used as a wildcard
        self.transitions={}

        self.moodStack=[]

        self.musicLibrary=musicLibrary

    def addState(self, name):
        assert name not in self.states

        self.states[name]=[]

    def addTransition(self, fromState, toState):
        pair=(fromState,toState)
        assert pair not in self.transitions

        self.transitions[pair]=[]

    def addMusicToState(self, stateName, trackName):
        self.states[stateName].append(trackName)

    def addMusicDirectoryToState(self, stateName, directoryName):
        exts=["*.mp3", "*.wav", "*.mid", "*.ogg"]
        for e in exts:
            g=directoryName+"/"+e
            for gn in glob.glob(g):
                self.states[stateName].append(gn)
            

    def addMusicToTransition(self, fromName, toName, trackName):
        self.transitions[(fromName,toName)].append(trackName)

    def addMusicDirectoryToTransition(self, fromName, toName, directoryName):
        exts=["*.mp3", "*.wav", "*.mid", "*.ogg"]
        for e in exts:
            g=directoryName+"/"+e
            for gn in glob.glob(g):
                self.transitions[(fromName,toName)].append(gn)
            
    def getState(self):
        if len(self.moodStack)==0:
            return None
        return self.moodStack[0]
        

    def setState(self, stateName):
        """
        You might instead want to use pushState, which handles
        transitions
        """
        self.moodStack=[stateName]

    def pushState(self, stateName):
        """
        this adds a state to the end of the current mood stack -
        transitions will be played to get the player to the
        destination
        """
        print "pushing transition to:",stateName
        self.moodStack.append(stateName)

    def tick(self):
        """
        if the music is still playing, do nothing.
        if we're at the end of a song, if there's only one state on
        the stack, pick a new song.
        
        if there's more than one state, look at the top two - if there
        is a transition, play that transition.
        otherwise, if there's a wildcard transition, play that
        otherwise, simply jump to the new state, and play a song
        randomly there.

        pop the top state off
        """

        if self.musicLibrary.isPlaying():
            #print "is playing"
            return

        numMoods=len(self.moodStack)

        print "moodStack size:",numMoods
        
        if numMoods==0:
            return

        if numMoods==1:
            newTrack=random.choice(self.states[self.moodStack[0]])
            self.musicLibrary.play(newTrack)
            return

        oldMood=self.moodStack[0]
        newMood=self.moodStack[1]

        self.moodStack=self.moodStack[1:]

        possTransitions=[(oldMood,newMood),
                         (oldMood,None),
                         (None,newMood)]

        for pt in possTransitions:
            if pt in self.transitions:
                newTrack=random.choice(self.transitions[pt])
                self.musicLibrary.play(newTrack)
                return

        # otherwise, there's no transition - just play a random song
        # from the new state

        newTrack=random.choice(self.states[newMood])
        self.musicLibrary.play(newTrack)


        

        

        
            
            
        
        
        
