import graph_rep
import python_reader
import symboltable
import copy

class graph:
    def __init__(self, variables):
        self.variables = copy.deepcopy(variables)
        self.stateArray = []

        # Define starting state (s0)
        self.startState = graph_rep.state('s0', symboltable.Symboltable(), [])
        self.stateArray.append(self.startState)

        # Counter used to name states s1, s2, ..., sN
        self.nameCounter = 1
        currentState = self.startState
        
        foundFirstThread = False

        # For each tuple in the list of dictionaries
        # Create a new state, append the counter
        for var in self.variables:
            #initialize the new state. label is s + 1 and symboltable is copied from previous state
            newState = graph_rep.state('s' + str(self.nameCounter), currentState.symboltable, currentState.programCounters)
            self.nameCounter += 1
            if var['scope'] == 'global.main' and len(newState.programCounters) == 0:
                thread = {"name": "main",
                        "function": "main",
                        "counter": 0}
                newState.programCounters.append(thread)
            if var['commandType'] == "functionCall":
                pthreadReturn = self.find_pthread(var, newState)
                if pthreadReturn['type'] == "create":
                    pthread = pthreadReturn['thread']
                    newState.programCounters.append(pthread)
                    foundFirstThread = True

            else:
                # Append the new variables of the current state to a new state
                newState.addVar(var)
            i = 0
            for i in range(0, len(newState.programCounters)):
                if thread['function'] == newState.programCounters[i]['function']:
                    newState.programCounters[i]['counter'] += 1

            # Add a transition to the new state from current state
            currentState.addTransition(newState)

            # Update current state to the new state and append to state array
            currentState = newState
            self.stateArray.append(currentState)
            if foundFirstThread == True:
                break
        #do something once the first pthread_create has been found
        self.simulate_new_states(currentState)

# String compares the name of a dictionary (assumed functionCall) with pthread matches
# Figures out whether the function is a pthread_create or pthread_join call, otherwise returns null
    def find_pthread(self, dictionary, state):
        dictValueSplit = dictionary['value'].split(",")
        x = dictionary["name"]
        if x == "pthread_create":
            thread = {"name": dictValueSplit[0].lstrip("&").strip(), 
                        "function": dictValueSplit[2].strip(),
                        "counter": 0}

            return {"type": "create","threadName": thread["name"], "thread": thread}

        elif x == "pthread_join":
            return {"type": "join", "threadName": dictValueSplit[0].strip(), "thread": None}

        else:
            return {"type": "", "threadName": "", "thread": None}


    def simulate_new_states(self, currentState):
        #for each programcounter in currentState, simulate the next child states
        stateQueue = [currentState]
        while len(stateQueue) != 0:
            print(f"----------\nstateQueue.label: {stateQueue[0].label}, programCounters: {stateQueue[0].programCounters}")
            for thread in stateQueue[0].programCounters:
                stateFound = False
                #find and execute the variable then append the new state to the list
                varFound = False
                #looking through the variables to find the correct scope
                for variable in self.variables:
                    splitScopeName = variable['scope'].split(".")
                    #identify the correct function
                    if thread['function'] == splitScopeName[-1]:
                        #identify the correct line within the variables list
                        if thread['counter'] == variable['lineCounter']:
                            #make new state with the found variable and an increased thread['counter']
                            newState = graph_rep.state('s' + str(self.nameCounter), stateQueue[0].symboltable, stateQueue[0].programCounters)
                            self.nameCounter += 1

                            # Append the new variables of the current state to a new state
                            if variable['commandType'] == 'functionCall':
                                pthreadReturn = self.find_pthread(variable, newState)
                                if pthreadReturn['type'] == "create":
                                    test = pthreadReturn['thread']
                                    newState.programCounters.append(test)
                                elif pthreadReturn['type'] == "join":
                                    foundThread = False
                                    for pc in newState.programCounters:
                                        if pthreadReturn['threadName'] == pc['name']:
                                            foundThread = True
                                    if foundThread == True:
                                        self.nameCounter -= 1
                                        varFound = True
                                        break
                            else:
                                newState.addVar(variable.copy())
                                #for counter in newState.programCounters:
                            i = 0
                            for i in range(0, len(newState.programCounters)):
                                if thread['function'] == newState.programCounters[i]['function']:
                                    newState.programCounters[i]['counter'] += 1
                            print(f"----------newState.label: {newState.label}, programCounters: {newState.programCounters}")
                            print(f"newState.symboltable: {newState.symboltable.symboltable}")
                            varFound = True
                            stateFound = self.find_eq(newState, stateQueue[0])
                            print(stateFound)
                            if stateFound == True:
                                #stateQueue[0].addTransition(state)
                                self.nameCounter -= 1
                            if stateFound == False:
                                # Add a transition to the new state from current state
                                stateQueue[0].addTransition(newState)

                                # Update current state to the new state and append to state array
                                stateQueue.append(newState)
                                self.stateArray.append(newState)

                    #use offset to find corresponding line and create a new state from it
                    #new state should have the programcounter for a given function increased by one
                    #TODO: lineCounter needs correct implementation in python_reader
                if varFound == False:
                    newState = graph_rep.state('s' + str(self.nameCounter), stateQueue[0].symboltable, stateQueue[0].programCounters)
                    self.nameCounter += 1
                    #stateQueue[0].programCounters.pop(stateQueue[0].programCounters.index(thread))
                    #print(f"popping: {newState.programCounters[(newState.programCounters.index(thread))]} from {newState.label}")
                    #print(f"with thread counter: {thread['counter']} on {thread['name']}")
                    newState.programCounters.pop(newState.programCounters.index(thread))
                    stateFound = self.find_eq(newState, stateQueue[0])
                    if stateFound == True:
                        self.nameCounter -= 1
                    if stateFound == False:
                        stateQueue[0].addTransition(newState)
                        stateQueue.append(newState)
                        self.stateArray.append(newState)
                    #for state in self.stateArray:
                    #    if state.label == 
                        #if state.label == stateQueue[0].label:
                        #    self.stateArray[self.stateArray.index(state)].programCounters = stateQueue[0].programCounters
            #print(f"popping {stateQueue[0].label}, {stateQueue[0].programCounters}\n\n")
            #if len(stateQueue[0].programCounters) == 0:
            #print(len(stateQueue))
            stateQueue.pop(0)

    def find_eq(self, newState, currentState):
        stateFound = False
        returnState = None
        for state in self.stateArray:
            if newState == state:
                #print(f"newState: {newState.label}, state: {state.label}")
                returnState = state
                stateFound = True
                currentState.addTransition(state)
                #print(f"state: {state.label}\n{state.symboltable}\n{state.programCounters}")
                #print(f"newstate: {newState.label}\n{newState.symboltable}\n{newState.programCounters}\n")
                #print(f"state {state.label} is considered the same as state {newState.label}")
                #if len(newState.ingoing) != 0:
                #    state.ingoing.append(newState.ingoing[0])
        return stateFound

a = python_reader.C_Reader('pthread_setting_variables.c')
a.get_scopes(a.file)
b = graph(a.result)
#for r in a.result:
#    print(r)
for x in b.stateArray:
    print(f"stateName: {x.label}")
    print(f"programCounters: {x.programCounters:}")
    for p in x.symboltable.symboltable:
        print(p)
    for y in x.ingoing:
        print(f"ingoing: {y.label}")
    for z in x.outgoing:
        print(f"outgoing: {z.destination.label}")
    print("\n")
