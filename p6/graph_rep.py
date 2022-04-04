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
        eqSymboltable = True
        eqProgramCounters = False
        counter = 1
        for dictionary in self.symboltable.symboltable:
            for var in dictionary['varList']:
                result = other.symboltable.retrieve_symbol(var.copy())
                if result == None:
                    eqSymboltable = False
                
        for ppc in self.programCounters:
            for opc in other.programCounters:
                if ppc['name'] == opc['name'] and ppc['counter'] == opc['counter']:
                    counter += 1
        #print(f"self.symboltable: {self.symboltable.symboltable}")
        #print(f"other.symboltable: {other.symboltable.symboltable}")
        #print(counter, len(self.programCounters), len(other.programCounters))
        if counter == len(self.programCounters) and counter == len(other.programCounters):
            eqProgramCounters == True
         
        #print(eqSymboltable, eqProgramCounters)
        return eqSymboltable and eqProgramCounters
        #if self.symboltable.symboltable.sort() == other.symboltable.symboltable.sort() and self.programCounters.sort() == other.programCounters.sort():
        #    return True
        #elif self.symboltable.symboltable.sort() != other.symboltable.symboltable.sort and self.programCounters.sort() != other.programCounters.sort():
        #    return False

class transition:
    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination
        destination.ingoing.append(origin)


