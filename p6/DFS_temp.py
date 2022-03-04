import grapRep

class stateDFSNode(state):
    def __init__(self):
        super().__init__()
        self.discovered = False
        self.explored = False

def depthFirstSearch(state: stateDFSNode):
    #TODO make it print tuples instead
    print(state.label, state.outgoing)
    state.discovered = True
    #if state is endpoint, it needs to be labelled as has been explored
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

