import graph_rep
import python_reader
import symboltable
import copy

class graph:
    def __init__(self, variables):
        self.variables = variables
        self.stateArray = []

        # Define starting state (s0)
        self.startState = graph_rep.state('s0', symboltable.Symboltable())
        self.stateArray.append(self.startState)

        # Counter used to name states s1, s2, ..., sN
        counter = 1
        currentState = self.startState

        # For each tuple in the list of dictionaries
        # Create a new state, append the counter
        for var in self.variables:
            #initialize the new state. label is s + 1 and symboltable is copied from previous state
            newState = graph_rep.state('s' + str(counter), copy.deepcopy(currentState.symboltable))
            counter += 1

            # Append the new variables of the current state to a new state
            newState.addVar(var)
            
            # Add a transition to the new state from current state
            currentState.addTransition(newState)
            # Update current state to the new state and append to STA
            currentState = newState
            self.stateArray.append(currentState)

a = python_reader.C_Reader('pthread_setting_variables.c')
a.get_scopes(a.file)
b = graph(a.result)
for x in b.stateArray:
     print(x.symboltable.symboltable, "\n\n")

