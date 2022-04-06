from operator import truediv
import re
import search_replace
import copy

#Class state definition.
class state:
    def __init__(self, label: str, symboltable: list, programCounters: list):
        #Node-label identifier.
        self.label = label

        #Connections/edges (pointer) to children/outgoing states.
        self.outgoing = []

        #Connections/edges to this state from parent node(s).
        self.ingoing = []

        #copy.deepcopy copies the entire object rather than assigning a pointer to the original one.
        self.symboltable = copy.deepcopy(symboltable)
        self.programCounters = copy.deepcopy(programCounters)
    
    def addTransition(self, state):
        """A function that adds a transition from the current state to another state."""
        state.ingoing.append(self)
        self.outgoing.append(state)
        

    def addVar(self, vardict):
        """A function that replaces or updates a variable in a symbol table. Uses regex tokens to filter input (vardict)."""
        search_replace.replaceVars(vardict, self.symboltable)

    def isEndpoint(self):
        """An internal function that checks whether a state is an end state. Checks whether it has no children."""
        if len(self.outgoing) == 0:
            return True
        else:
            return False

    def __eq__(self, other):
        """An overwrite of the == function to check if a state is equal to another by comparing their symbol tables and program counters. 
        Returns True or False."""
        eqSymboltable = True
        eqProgramCounters = False

        # A counter that keeps track of program counter matches.
        counter = 0

        #Loop through each variable (dictionary) in the state's dictionary.
        for dictionary in self.symboltable.symboltable:
            for var in dictionary['varList']:

                #Save the intermediate result by extracting each variable from the other state.
                #If the variable of the compared state is either NULL or not equal the one in the original state, return false.
                result = other.symboltable.retrieve_symbol(var.copy())
                if result == None or var['value'] != result:
                    eqSymboltable = False
        
        #Loop through each program counter in the primary (ppc) program counters 
        #and compare against the compared (other, opc) program counter.
        for ppc in self.programCounters:
            for opc in other.programCounters:

                #If the name and counters of the symbol tables match, add a match to the counter.
                if ppc['name'] == opc['name'] and ppc['counter'] == opc['counter']:
                    counter += 1

        #If the counter is equal to the number of elements in each programCounters list, then the program counters are equal.
        if counter == len(self.programCounters) and counter == len(other.programCounters):
            eqProgramCounters = True
        
        #Return the combined result (True, True) returns True.
        return eqSymboltable and eqProgramCounters

    def link_ingoing_outgoing(self):
        """First-order graph reduction. 
        If a sequence of nodes X, Y and Z are connected, and X and Z are Y's only parent and child state, respectively, Y is omitted."""
        
        #If the node only has one ingoing (parent) and child (outgoing) state.
        #Create a transition directly from the parent to the child state.
        if len(self.ingoing) == 1 and len(self.outgoing) == 1:
            self.ingoing[0].addTransition(self.outgoing[0])

            ingoingState = self.ingoing[0]
            outgoingState = self.outgoing[0]

            #If the parents child note is the current state itself, remove it from the parent state's child nodes list (the only one).
            for state in ingoingState.outgoing:
                if state == self:
                    ingoingState.outgoing.pop(ingoingState.outgoing.index(state))
            
            #Same procedure as above, but for current node's child state. Remove it from the parent nodes list of the current state child.
            for state in outgoingState.ingoing:
                if state == self:
                    outgoingState.ingoing.pop(outgoingState.ingoing.index(state))
            
            return True
        return False

#The transition class used to represent edges in the graph.
class transition:
    def __init__(self, origin, destination):
        """Initializer function: A transition origin and destination are states. Both are connected by a transition."""
        self.origin = origin
        self.destination = destination
        destination.ingoing.append(origin)


