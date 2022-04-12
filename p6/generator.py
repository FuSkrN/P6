import graph_rep
import python_reader
import symboltable
import copy

class graph:
    """Class to define a graph consisting of states. Input is a list of variable dictionaries"""
    def __init__(self, variables):
        self.variables = copy.deepcopy(variables)
        self.stateArray = []
        self.funcNameCounter = 0

        # Define starting state (s0)
        self.startState = graph_rep.state('s0', symboltable.Symboltable(), [])
        self.stateArray.append(self.startState)

        # Counter used to name states s1, s2, ..., sN
        self.nameCounter = 1
        currentState = self.startState
        
        foundFirstThread = False

        # For each tuple in the list of dictionaries
        # Create a new state, append the counter
        # Once a pthread_create has been found, call simulate_new_states, which will generate all subsequent states
        for var in self.variables:
            #initialize the new state. label is s + 1 and symboltable is copied from previous state
            newState = graph_rep.state('s' + str(self.nameCounter), currentState.symboltable, currentState.programCounters)
            self.nameCounter += 1
            if var['scope'] == 'global.main' and len(newState.programCounters) == 0:
                thread = {"name": "main",
                        "function": "main",
                        "counter": 0}
                newState.programCounters.append(thread)
            # Check if the variable is a call to pthread_create, and prepares to call simulate_new_states if it is found
            if var['commandType'] == "functionCall":
                pthreadReturn = self.find_pthread(var)
                if pthreadReturn['type'] == "create":
                    pthread = pthreadReturn['thread']
                    # Appends the thread to programCounters of the new state
                    newState.programCounters.append(pthread)
                    foundFirstThread = True

            else:
                # Append the new variables of the current state to a new state
                newState.addVar(var)

            # Increments the programCounter by one, to represent that the next statement in the program has been executed
            i = 0
            for i in range(0, len(newState.programCounters)):
                if thread['function'] == newState.programCounters[i]['function']:
                    newState.programCounters[i]['counter'] += 1

            # Add a transition to the new state from current state
            currentState.addTransition(newState)

            # Update current state to the new state and append to state array
            currentState = newState
            self.stateArray.append(currentState)

            # If pthread_create was found, break out of the for each loop and run simulate_new_states
            if foundFirstThread == True:
                break

        #do something once the first pthread_create has been found
        self.simulate_new_states(currentState)

# String compares the name of a dictionary (assumed functionCall) with pthread matches
# Figures out whether the function is a pthread_create or pthread_join call, otherwise returns null
    def find_pthread(self, dictionary):
        """Checks if an input dictionary is a pthread_create or pthread_join function. It takes a function dictionary as input and outputs a dictionary containing: type (create or join), threadName and a thread dictionary"""
        dictValueSplit = dictionary['value'].split(",")
        x = dictionary["name"]
        if x == "pthread_create":
            thread = {"name": dictValueSplit[0].lstrip("&").strip(), 
                    "function": dictValueSplit[2].strip() + "(" + str(self.funcNameCounter) + ")",
                        "counter": 0}
            self.funcNameCounter += 1

            return {"type": "create","threadName": thread["name"], "thread": thread}

        elif x == "pthread_join":
            return {"type": "join", "threadName": dictValueSplit[0].strip(), "thread": None}

        else:
            return {"type": "", "threadName": "", "thread": None}


    def simulate_new_states(self, currentState):
        """Creates new states to be appended to the State array in the correct manner. 
        If a state node already exists, a transition is instead made from its parents to the existing node.
        Takes an input state node to be added to the state array graph. Outputs (not returns) an updated state array graph."""
        stateQueue = [currentState]
        while len(stateQueue) != 0:
            
            #For each programcounter in currentState, simulate the next child states.
            for thread in stateQueue[0].programCounters:

                #Flag used to identify existing states, which are not to be appended but rather updated.
                stateFound = False

                #Flag used to identify if an existing thread (in programCounters) is still running.
                varFound = False

                #Looking through the variables to find the correct scope
                for variable in self.variables:
                    splitScopeName = variable['scope'].split(".")
                    #Identify whether a thread function is equivalent to the current scope. If true, then it is within the same scope.
                    if thread['function'].split("(")[0] == splitScopeName[-1]:

                        #If the function is a match, check whether their line counters are equivalent (correct line).
                        if thread['counter'] == variable['lineCounter']:

                            #Make new state with the found variable and an increased thread counter (thread['counter'])
                            #A variable is any input type, such as declaration, assignment or a function.
                            newState = graph_rep.state('s' + str(self.nameCounter), stateQueue[0].symboltable, stateQueue[0].programCounters)
                            self.nameCounter += 1

                            #Check whether the variable in question is a function.
                            if variable['commandType'] == 'functionCall':

                                #Check whether said function call is a pthread type (create or join).
                                pthreadReturn = self.find_pthread(variable)

                                #If a pthread_create function call is read, create a new thread and add it to the state's new programcounters list.
                                if pthreadReturn['type'] == "create":
                                    newThread = pthreadReturn['thread']
                                    newState.programCounters.append(newThread)
                                elif pthreadReturn['type'] == "join":
                                    foundThread = False

                                    #If a pthread_join function call is read in an existing thread/state, 
                                    #revert and do not add the temporary (new) state.
                                    for pc in newState.programCounters:
                                        if pthreadReturn['threadName'] == pc['name']:
                                            foundThread = True
                                    if foundThread == True:
                                        self.nameCounter -= 1
                                        varFound = True
                                        break

                            #If the variable is not a function call, add it directly to the new state's list of variables (Symbol table).
                            else:
                                #tempVar is used to change the scope name, to allow for multiple calls of the same function.
                                tempVar = variable.copy()
                                tempVarScopeSplit = tempVar['scope'].split(".")
                                tempVarScopeSplit.pop()
                                tempVarScopeSplit.append(thread['function'])
                                tempVarScope = tempVarScopeSplit[0]

                                for scope in tempVarScopeSplit:
                                    tempVarScope = tempVarScope + '.' + scope
                                tempVar['scope'] = tempVarScope

                                newState.addVar(tempVar)

                            #Loop through the programCounters list for a state and check if the current variable has been executed.
                            #Once done, increment the corresponding thread's program counter.
                            #Equivalent to reading a line in a thread and incrementing the counter by one.
                            i = 0
                            for i in range(0, len(newState.programCounters)):
                                if thread['function'] == newState.programCounters[i]['function']:
                                    newState.programCounters[i]['counter'] += 1
                            
                            #Flag to a mark that a variable has been found.
                            varFound = True

                            #Check if the current state is a duplicate of any state in the state array.
                            stateFound = self.find_eq(newState, stateQueue[0])
                            if stateFound == True:
                                self.nameCounter -= 1
                            if stateFound == False:

                                #Add a transition to the new state from its working parent state.
                                #The 1st queue element (stateQueue[0]) is the parent node.
                                stateQueue[0].addTransition(newState)

                                #Append the new state to the state queue and the state array.
                                stateQueue.append(newState)
                                self.stateArray.append(newState)

                #Once a thread finishes as no variable is read, 
                #its corresponding state array node is created and the program counter is removed.
                if varFound == False:
                    newState = graph_rep.state('s' + str(self.nameCounter), stateQueue[0].symboltable, stateQueue[0].programCounters)
                    self.nameCounter += 1
                    newState.programCounters.pop(newState.programCounters.index(thread))

                    #At the end, check if the finished thread already exists.
                    stateFound = self.find_eq(newState, stateQueue[0])
                    if stateFound == True:
                        self.nameCounter -= 1
                    if stateFound == False:
                        stateQueue[0].addTransition(newState)
                        stateQueue.append(newState)
                        self.stateArray.append(newState)

            #Pop the first state in the state queue in a FIFO manner.
            stateQueue.pop(0)

    def find_eq(self, newState, currentState):
        """Checks if a newState already exists, and if it does, adds a transition from the parent of newState to the duplicate state. 
        Inputs are (newState, parentState)"""
        stateFound = False
        for state in self.stateArray:

            #Uses __eq__ to check whether the newState is equal to the current state.
            if newState == state:
                returnState = state
                stateFound = True

                #Add a transition from the parent of newState to the duplicate state.
                currentState.addTransition(state)
        return stateFound

# DEBUGGING PURPOSES - DO NOT REMOVE

#a.get_scopes(a.file)
#b = graph(a.result)
#for r in a.result:
#    print(r)
#for x in b.stateArray:
#    print(f"stateName: {x.label}")
#    print(f"programCounters: {x.programCounters:}")
#    for p in x.symboltable.symboltable:
#        print(p)
#    for y in x.ingoing:
#        print(f"ingoing: {y.label}")
#    for z in x.outgoing:
#        print(f"outgoing: {z.destination.label}")
#    print("\n")
