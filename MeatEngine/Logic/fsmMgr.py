"""Meat Engine Hierarchical Finite State Machine (hFSM) Manager

This could be refactored so that a fsmMgr is an instatiatable class,
but for now it uses the "lazy singleton" pattern - the state stack is
a module global, and methods are just module functions. This is
adequate for my needs so far.

Use: create State objects, push them on the stack. Periodically call
the update and draw functions, and pass the handleKey and
handleMouseButton events in as appropriate. The top state will get
delegated to, which may choose to delegate further. For example, a
dialog box may choose to call the next state's draw code first, before
drawing itself.
"""


class State:
    def __init__(self):
        self.parent=None

    def handleMouseButton(self, bDown, buttonIndex):
        return False

    def handleKey(self, key, unicode):
        return False

    def init(self):
        pass

    def activateApp(self, bNowActive):
        return False

        

gStateStack=[]

def pushState(newState):
    try:
        oldTop=gStateStack[-1]
    except:
        oldTop=None

    gStateStack.append(newState)
    newState.parent=oldTop
    newState.init()
        

def popState():
    gStateStack.pop()
    

def popAll():
    global gStateStack
    gStateStack=[]


def handleKey(k, unicode):
    for s in reversed(gStateStack):
        if s.handleKey(k, unicode):
            return True
    return False

def handleActivate(bNowActive):
    for s in reversed(gStateStack):
        if s.activateApp(bNowActive):
            return True
    return False

def handleMouseButton(bDown, button):
    for s in reversed(gStateStack):
        if s.handleMouseButton(bDown, button):
            return True
    return False

def update(ms):
    if not len(gStateStack):
        return False
    
    gStateStack[-1].update(ms)
    return True

def draw():
    if not len(gStateStack):
        return

    gStateStack[-1].draw()

def isTop(state):
    return len(gStateStack)>0 and state==gStateStack[-1]
        
