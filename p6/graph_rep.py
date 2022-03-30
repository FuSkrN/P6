from operator import truediv
import re
import search_replace

class state:
    def __init__(self, label, symboltable):
        self.label = label
        #connections to other states
        self.outgoing = []
        #connections to this state
        self.ingoing = []
        self.symboltable = symboltable
    
    #add transition from current state to another state
    def addTransition(self, state):
        self.outgoing.append(transition(self, state))

    def addVar(self, vardict):
        search_replace.replaceVars(vardict, self.symboltable)

    #check if the state is an end state
    def isEndpoint(self):
        if len(self.outgoing) == 0:
            return True
        else:
            return False
    
    def __eq__(self, other):
        if self.__dict__ == other.__dict__:
            return True
        else if self.__dict__ != other.__dict__:
            return False

class transition:
    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination
        destination.ingoing.append(origin)


