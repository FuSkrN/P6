class state:
    def __init__(self, label):
        self.label = label
        #connections to other states
        self.outgoing = []
        #connections to this state
        self.ingoing = []
        self.discovered = False
        self.explored = False
    
    #add transition from current state to another state
    def addTransition(self, state):
        self.outgoing.append(transition(self, state))

    #check if the state is an end state
    def isEndpoint(self):
        if len(self.outgoing) == 0:
            return True
        else:
            return False

class transition:
    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination
        destination.ingoing.append(origin)

def depthFirstSearch(state):
    state.discovered = True
    #if state is endpoint, it needs to be has been explored
    if state.isEndpint() == True:
        state.discovered = True
        state.explored = True
        return
    else:
        #if it has not, every sub state is recursivly searched through
        for transition in len(state.outgoing):
            if !(state.outgoing[transition].discovered or state.outgoing[transition].explored):
                depthFirstSearch(state.outgoing[transition])
        #after substates has been explored, label state as explored and return
        state.discovered = True
        state.explored = True
        return

