from operator import truediv
import re

class state:
    def __init__(self, label):
        self.label = label
        #connections to other states
        self.outgoing = []
        #connections to this state
        self.ingoing = []
        self.variables = []
    
    #add transition from current state to another state
    def addTransition(self, state):
        self.outgoing.append(transition(self, state))

    def addVar(self, var: dict, predecessorState):
        #print("var: ", var)
        #check if variable already exist in state and remove if yes
        variableRegex = re.compile('[a-zA-Z][a-zA-Z0-9]*')
        values = []
        isMatch = False
        #TODO make it do the math in the expressions

        # print('old:', self.variables, "\n\n")

        for v in self.variables:
            print(f"v['name'], var['name']: ({v['name']}, {var['name']})\n")
            if v['name'] == var['name']:
                # print(f"Updated {v['name']}'s value {v['value']} to {var['name']}'s value {var['value']}...\n")
                isMatch = True
                v['value'] = var['value']

                # print(f"v after update: {v['value']}\n")

            # FIND UDTRYK OG TILFØJ DEM TIL EN LISTE ...
            valueVariables = re.findall(variableRegex, v['value'])
            if len(valueVariables) != 0:
                for i in valueVariables:
                    for var in predecessorState.variables:
                        if var['name'] == i:
                            values.append(var)

        # if len(values) != 0:
        if isMatch == False:
            # print(f"Added new dict {var['name']}:{var['value']}")
            self.variables.append(var)
            print(f"isMatch == False -> ({var})\n")
            print(f"self.variables (from isMatch == False): {self.variables}\n")
            # print('values: ', values)
        values.sort(key=self.sortByNameLength, reverse=True)
        
        for j in values: # FOR HVER DICTIONARY I LISTEN VALUES (sorteret liste af udtryk på højre-siden af lighedstegnet ...)
            for n in self.variables: # FOR HVER DICTIONARY I LISTEN VARIABLES (liste af variabler i staten [navn, værdi])
                if n['name'] == j['name']: # HVIS NAVNET PÅ BEGGE DICTS ER DET SAMME (SAMME VARIABEL)
                    q = n['value'].replace(j['name'], j['value']) # Kig på værdien (value) i variabel n, som indeholder udtryk fra values og erstat dem med deres værdier
                                                                  # fx: x = b (13) - c (-7) + 20 -> x = 13 - (-7) + 20 ...
                    print(f"q: {q}\n")
                else:
                    print(f"n['name'], n['value']: ({n['name']}, {n['value']})\n")
        print(f"self.variables (from addVar): {self.variables}\n")
        # self.variables.append(var)
        # print('new:', self.variables, "\n\n")

    def sortByNameLength(self, x):
        return len(x['name'])

    #check if the state is an end state
    def isEndpoint(self):
        if len(self.outgoing) == 0:
            return True
        else:
            return False

class transition:
    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination
        destination.ingoing.append(origin)


