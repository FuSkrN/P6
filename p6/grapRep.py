class state:
    def __init__(self, label):
        self.label = label
        #connections to other states
        self.outgoing = []
        #connections to this state
        self.ingoing = []
    
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
    if state.isEndpint() == True:
        return
    else:
        for transition in len(state.outgoing):
            depthFirstSearch(state.outgoing[transition])
