import re

class state:
    def __init__(self, label):
        self.label = label
        #connections to other states
        self.outgoing = []
        #connections to this state
        self.ingoing = []
        self.variables = []
    
    #add transition from current state to another state
    def addTransition(self, state):
        self.outgoing.append(transition(self, state))

    def addVar(self, var: dict, predecessorState):
        #check if variable already exist in state and remove if yes
        variableRegex = re.compile('^[a-zA-Z][a-zA-Z0-9]*$')
        #TODO make it do the math in the expressions
        mylist = []
        for v in self.variables:
            if v['name'] == var['name']:
                self.variables.remove(v)
            mylist.append(re.findall(variableRegex, v['value']))
            print(mylist, v['value'])
        self.variables.append(var)

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


