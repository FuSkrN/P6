import python_reader

class Symboltable:
    def __init__(self):
        #create symboltable
        self.symboltable = [{"scope": "global",
                            "varList": []}]

    def add_symbol(self, symbolDict, symbolList):
        #add a symbol to the symboltable
        tempDict = {"name": symbolDict['name'],
                    "value": symbolDict['value'],
                    "scope": symbolDict['scope']}
        scopeFound = False

        for sAdd in symbolList:
            if sAdd['scope'] == tempDict['scope']:
                sAdd['varList'].append(tempDict)
                scopeFound = True
                break
        if scopeFound == False:
            symbolList.append({"scope": tempDict['scope'],
                                "varList": [tempDict]})
        return symbolList

    def update_symbol_value(self, symbolDict, symbolList):
        #update the value of a symbol in the symboltable
        seperator = "."

        varFound = False
        while varFound == False:
            for sUpdate in symbolList:
                if sUpdate['scope'] == symbolDict['scope']:
                    for var in sUpdate['varList']:
                        if var['name'] == symbolDict['name']:
                            var['value'] = symbolDict['value']
                            varFound = True
                            break
                    break
            tempName = symbolDict['scope'].split(".")
            tempName.pop()
            symbolDict['scope'] = seperator.join(tempName)

        return symbolList

    def update_symbol(self, dictionary):
        if dictionary['commandType'] == "declaration":
            #add variable to dictionary
            self.symboltable = self.add_symbol(dictionary, self.symboltable)
            
        elif dictionary['commandType'] == "assignment":
            #replace value in dictionary
            self.symboltable = self.update_symbol_value(dictionary, self.symboltable)

        else:
            #something went wrong
            pass

    def retrieve_symbol(self, dictionary):
        seperator = "."
        while True:
            for sRetrieve in self.symboltable:
                if sRetrieve['scope'] == dictionary['scope']:
                    for var in sRetrieve['varList']:
                        if var['name'] == dictionary['name']:
                            return var

            tempName = dictionary['scope'].split(".") 
            tempName.pop()
            dictionary['scope'] = seperator.join(tempName)

           


reader = python_reader.C_Reader("pthread_setting_variables.c")
reader.get_scopes(reader.file)
st = Symboltable()
for test in reader.result:
    st.update_symbol(test)
for wad in st.symboltable:
    print(wad)
print('\n\n')
fmwaioff = {'scope': 'global.setY', 'name': 'x'}

one = st.retrieve_symbol(fmwaioff)
print(one)
