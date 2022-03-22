# Used to identify types of dictionaries used as input in symbol table

import python_reader
import symboltable

def update_symboltable(variableArr):
    table = symboltable

    for dictionary in variableArr:
        if dictionary['commandType'] = "declaration":
            #add variable to dictionary
            table.add_symbol(dictionary)

        elif dictionary['commandType'] = "assignment":
            #replace value in dictionary
            pass
        elif dictionary['commandType'] = "functionCall":
            #do something with functions?
            pass
        else:
            #something went wrong
            pass



