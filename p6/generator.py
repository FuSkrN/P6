import graph_rep
import python_reader
import symboltable
import search_replace
import copy
import re

class graph:
    """Class to define a graph consisting of states. Input is a list of variable dictionaries"""
    def __init__(self, variables):
        self.variables = copy.deepcopy(variables)
        self.stateArray = []
        self.funcNameCounter = 0

        # Define starting state (s0)
        self.startState = graph_rep.state('s0', symboltable.Symboltable(), [], [])
        self.stateArray.append(self.startState)

        # Counter used to name states s1, s2, ..., sN
        self.nameCounter = 1
        currentState = self.startState
        
        foundFirstThread = False
        foundMain = False

        # For each tuple in the list of dictionaries
        # Create a new state, append the counter
        # Once main has been found, call simulate_new_states, which will generate all subsequent states
        for var in self.variables:
            #initialize the new state. label is s + 1 and symboltable is copied from previous state
            newState = graph_rep.state('s' + str(self.nameCounter), currentState.symboltable, currentState.programCounters, currentState.ifList)
            self.nameCounter += 1
            if var['scope'] == 'global.main' and len(newState.programCounters) == 0:
                thread = {"name": "main",
                        "function": "main",
                        "counter": 0}
                newState.programCounters.append(thread)
                foundMain = True

            elif foundMain == False:
                # Append the new variables of the current state to a new state
                newState.addVar(var)
            
            # Add a transition to the new state from current state
            currentState.addTransition(newState)

            # Update current state to the new state and append to state array
            currentState = newState
            self.stateArray.append(currentState)

            # If pthread_create was found, break out of the for each loop and run simulate_new_states
            if foundMain == True:
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

    def check_if_condition(self, conditionalDictionary, symboltable):
        """Returns the evaluated conditional statement"""
        conditionalDictionary = search_replace.replace_vars_without_update(conditionalDictionary, symboltable)
        result = search_replace.evaluateExpression(conditionalDictionary['value'])
        if result == "True":
            return True
        else:
            return False

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
                    #if thread['function'].split("(")[0] == splitScopeName[-1]:
                    if self.check_if_in_scope(thread, variable):

                        #If the function is a match, check whether their line counters are equivalent (correct line).
                        if thread['counter'] == variable['lineCounter']:

                            #Make new state with the found variable and an increased thread counter (thread['counter'])
                            #A variable is any input type, such as declaration, assignment or a function.
                            newState = graph_rep.state('s' + str(self.nameCounter), stateQueue[0].symboltable, stateQueue[0].programCounters, stateQueue[0].ifList)
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

                            elif variable['commandType'] == 'ifStatement':
                                if self.check_if_condition(variable, newState.symboltable) == True and self.check_if_parents_exist(newState, variable):
                                    self.add_if_to_ifList(newState, variable)
                                else:
                                    self.skip_if_section(newState, thread, variable)

                            elif variable['commandType'] == 'ifElseStatement':
                                previousIfExecuted = self.check_if_exists(variable, newState)
                                if self.check_if_condition(variable, newState.symboltable) == True and previousIfExecuted == False and self.check_if_parents_exist(newState, variable):
                                    self.add_if_to_ifList(newState, variable)
                                else:
                                    self.skip_if_section(newState, thread, variable)
    
                            elif variable['commandType'] == 'elseStatement':
                                previousIfExecuted = self.check_if_exists(variable, newState)
                                if previousIfExecuted == False and self.check_if_parents_exist(newState, variable):
                                    newState.ifList.append(variable['name'])
                                else:
                                    self.skip_if_section(newState, thread, variable)
                            #If the variable is not a function call, add it directly to the new state's list of variables (Symbol table).
                            else:
                                self.add_variable_to_newState(variable, thread, newState)

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
                    newState = graph_rep.state('s' + str(self.nameCounter), stateQueue[0].symboltable, stateQueue[0].programCounters, stateQueue[0].ifList)
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

    def skip_if_section(self, newState, thread, variable):
        flag = True

        while flag:
            for i in range(0, len(newState.programCounters)):
                if thread['function'] == newState.programCounters[i]['function']:
                    for variableInList in self.variables:
                        if newState.programCounters[i]['counter'] == variableInList['lineCounter']:
                            if self.find_root_if(variableInList['scope'], variable['scope']) == False:
                                flag = False
                    if newState.programCounters[i]['counter'] >= len(self.variables):
                        flag = False

                    if flag == True:
                        newState.programCounters[i]['counter'] += 1
                    elif flag == False:
                        newState.programCounters[i]['counter'] -= 1

    def check_if_in_scope(self, thread, variable):
        splitScopeName = variable['scope'].split(".")
        funcName = thread['function'].split("(")
        for scope in splitScopeName:
            if scope == funcName[0]:
                return True
        return False

    def check_if_parents_exist(self, newState, variable):
        match = re.compile("(if)\(([0-9]+)(-[0-9]+)?\)")
        splitScope = variable['scope'].split(".")
        splitScope.reverse()
        for i in range(len(splitScope)):
            if i != 0 and re.search(match, splitScope[i]) != None:
                ifFound = False
                for element in newState.ifList:
                    if element == splitScope[i]:
                        ifFound = True
                if ifFound == False:
                    return False
        return True
                    

        newState.ifList

    def find_root_if(self, firstScope, secondScope):
        splitFirstScope = firstScope.split(".")
        splitSecondScope = secondScope.split(".")
        counter = 0
        if len(splitFirstScope) != len(splitSecondScope):
            return False
        match = re.compile("(if|ifElse|else)\(([0-9]+)(-[0-9]+)?\)")
        for i in range(len(splitFirstScope)):
            for j in range(len(splitSecondScope)):
                if splitFirstScope[i] == splitSecondScope[j]:
                    counter += 1

        return counter == len(splitFirstScope)

    def add_if_to_ifList(self, newState, variable):
        match = re.compile("(if|ifElse)\(([0-9]+)(-[0-9]+)?\)")
        searchResult = re.search(match, variable['scope'].split(".")[-1])
        ifName = f"if({searchResult.group(2)})"
        newState.ifList.append(ifName)

    def check_if_exists(self, variable, newState):
        match = re.compile("(ifElse|else)\(([0-9]+)(-[0-9]+)?\)")
        searchResult = re.search(match, variable['scope'].split(".")[-1])
        ifName = f"if({searchResult.group(2)})"
        return (ifName in newState.ifList)

    def add_variable_to_newState(self, variable, thread, newState):
        #tempVar is used to change the scope name, to allow for multiple calls of the same function.
        tempVar = variable.copy()
        tempVarScopeSplit = tempVar['scope'].split(".")
        tempVarScopeSplit.pop()
        tempVarScopeSplit.append(thread['function'])
        tempVarScope = tempVarScopeSplit[0]

        #add the scope to the variable dictionary
        for scope in tempVarScopeSplit:
            if scope != 'global':
                tempVarScope = tempVarScope + '.' + scope
            tempVar['scope'] = tempVarScope

        newState.addVar(tempVar)
        

# DEBUGGING PURPOSES - DO NOT REMOVE
#a = python_reader.C_Reader("pthread_setting_variables.c")

#a.get_scopes(a.file)
#b = graph(a.result)
#for state in b.stateArray:
#    state.symboltable.find_global_vars()

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
