import graphrep
import python_reader

class graph:
    def __init__(self, variables):
        self.variables = variables
        self.stateArray = []
        self.startState = graphrep.state('s0')
        self.stateArray.append(self.startState)
        counter = 1
        currentState = self.startState
        for var in self.variables:
            newState = graphrep.state('s' + str(counter))
            counter += 1
            
            for v in currentState.variables:
                newState.addVar(v, currentState)

            newState.addVar(var, currentState)
            currentState.addTransition(newState)
            currentState = newState
            self.stateArray.append(currentState)
    

a = python_reader.C_Reader('pthread_setting_variables.c')
a.get_scopes(a.file)
b = graph(a.result)
for x in b.stateArray:
    if len(x.variables) != 0:
        #pass
        print(len(x.variables), x.variables[0], x.variables[-1])
