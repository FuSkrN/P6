import graphrep
import python_reader

class graph:
    def __init__(self, variables):
        self.variables = variables
        self.stateArray = []

        # Define starting state (s0)
        self.startState = graphrep.state('s0')
        self.stateArray.append(self.startState)

        # Counter used to name states s1, s2, ..., sN
        counter = 1
        currentState = self.startState

        # For each tuple in the list of dictionaries
        # Create a new state, append the counter
        for var in self.variables:
            newState = graphrep.state('s' + str(counter))
            counter += 1
            
            # For each tuple in the previous state, add its variables
            # to the current state ...
            for v in currentState.variables:
                newState.addVar(v, currentState)

            # Append the new variables of the current state to a new state
            newState.addVar(var, currentState)
            
            # Add a transition to the new state from current state
            currentState.addTransition(newState)
            
            # Update current state to the new state and append to STA
            currentState = newState
            self.stateArray.append(currentState)
    

a = python_reader.C_Reader('pthread_setting_variables.c')
a.get_scopes(a.file)
b = graph(a.result)
for x in b.stateArray:
    if len(x.variables) != 0:
        #pass
        print(len(x.variables), x.variables[0], x.variables[-1])
print("a.result:", a.result)
