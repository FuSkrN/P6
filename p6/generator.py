import graph_rep
import python_reader
import symboltable
import copy

class graph:
    def __init__(self, variables):
        self.variables = variables
        self.stateArray = []

        # Define starting state (s0)
        self.startState = graph_rep.state('s0', symboltable.Symboltable(), [])
        self.stateArray.append(self.startState)

        # Counter used to name states s1, s2, ..., sN
        counter = 1
        currentState = self.startState

        # For each tuple in the list of dictionaries
        # Create a new state, append the counter
        for var in self.variables:
            #initialize the new state. label is s + 1 and symboltable is copied from previous state
            newState = graph_rep.state('s' + str(counter), copy.deepcopy(currentState.symboltable), currentState.programCounters.copy())
            counter += 1

            if var['scope'] == 'global.main' and len(newState.programCounters) == 0:
                thread = {"name": "main",
                        "function": "main",
                        "counter": 0}
                newState.programCounters.append(thread)
            if var['commandType'] == "functionCall":
                pthreadReturn = self.find_pthread(var, newState)
                if pthreadReturn['type'] == "create":
                    break

                        

            # Append the new variables of the current state to a new state
            newState.addVar(var)
            
            # Add a transition to the new state from current state
            currentState.addTransition(newState)

            # Update current state to the new state and append to state array
            currentState = newState
            self.stateArray.append(currentState)

        #do something once the first pthread_create has been found
        self.simulate_new_states(currentState)

# String compares the name of a dictionary (assumed functionCall) with pthread matches
# Figures out whether the function is a pthread_create or pthread_join call, otherwise returns null
    def find_pthread(self, dictionary, state):
        dictValueSplit = dictionary['value'].split(",")
        x = dictionary["name"]
        if x == "pthread_create":

            thread = {"name": dictValueSplit[0].lstrip("&"), 
                        "function": dictValueSplit[2],
                        "counter": 0}
            
            state.programCounters.append(thread)

            return {"type": "create", "thread": dictValueSplit[0].lstrip("&")}

        elif x == "pthread_join":
            return {"type": "join", "thread": dictValueSplit[0]}

        else:
            return None


    def simulate_new_states(self, currentState):
        #for each programcounter in currentState, simulate the next child states
        for counter in currentState.programCounters:
            #find and execute the variable then append the new state to the list
            offsetCounter = 0
            firstVarFound = False
            
            #looking through the variables to find the correct scope
            for variable in self.variables:
                splitVariable = variable['scope'].split(".")

                #identify the correct function
                if counter['function'] == splitVariable[-1]:
                    #find the start of the function and set that to 0
                    if firstVarFound == False:
                        offsetCounter = variable['lineCounter']
                        firstVarFound == True
                    #use offset to find corresponding line and create a new state from it
                    #new state should have the programcounter for a given function increased by one
                    #TODO: lineCounter needs correct implementation in python_reader

           

a = python_reader.C_Reader('pthread_setting_variables.c')
a.get_scopes(a.file)
#for r in a.result:
#    print(r)
b = graph(a.result)
for x in b.stateArray:
     print(x.symboltable.symboltable, "\n\n")
