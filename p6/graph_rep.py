from operator import truediv
import re
import search_replace
import copy

class state:
    def __init__(self, label: str, symboltable: list, programCounters: list):
        self.label = label
        #connections to other states
        self.outgoing = []
        #connections to this state
        self.ingoing = []
        self.symboltable = copy.deepcopy(symboltable)
        self.programCounters = copy.deepcopy(programCounters)
    
    #add transition from current state to another state
    def addTransition(self, state):
        state.ingoing.append(self)
        self.outgoing.append(state)
        

    def addVar(self, vardict):
        search_replace.replaceVars(vardict, self.symboltable)

    #check if the state is an end state
    def isEndpoint(self):
        if len(self.outgoing) == 0:
            return True
        else:
            return False

    def __eq__(self, other):
        eqSymboltable = True
        eqProgramCounters = False
        counter = 0
        for dictionary in self.symboltable.symboltable:
            for var in dictionary['varList']:
                result = other.symboltable.retrieve_symbol(var.copy())
                if result == None or var['value'] != result:
                    eqSymboltable = False
                
        for ppc in self.programCounters:
            for opc in other.programCounters:
                if ppc['name'] == opc['name'] and ppc['counter'] == opc['counter']:
                    counter += 1
        if counter == len(self.programCounters) and counter == len(other.programCounters):
            eqProgramCounters = True
        return eqSymboltable and eqProgramCounters

    def link_ingoing_outgoing(self):
        if len(self.ingoing) == 1 and len(self.outgoing) == 1:
            self.ingoing[0].addTransition(self.outgoing[0])

            ingoingState = self.ingoing[0]
            outgoingState = self.outgoing[0]
            for state in ingoingState.outgoing:
                if state == self:
                    ingoingState.outgoing.pop(ingoingState.outgoing.index(state))
            
            for state in outgoingState.ingoing:
                if state == self:
                    outgoingState.ingoing.pop(outgoingState.ingoing.index(state))
            
            return True
        return False

class transition:
    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination
        destination.ingoing.append(origin)


