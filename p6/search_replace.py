import re
import python_reader
import symboltable

def findVars(expression):
    variableRegex = re.compile('[a-zA-Z][a-zA-Z0-9]*')
    variables = re.findall(variableRegex, expression)
    return variables

def replaceVars(variabledict, symboltable):
    if variabledict['commandType'] == 'functionCall':
        return
    varsInExpression = findVars(variabledict['value'])
    varsInExpression.sort(key=sortByNameLength, reverse=True)
    #replace the value with found value
    for variable in varsInExpression:
        #first step is to find the actual value in the symbol table
        tempdict = {"name": variable, "scope": variabledict['scope']}
        varVal = symboltable.retrieve_symbol(tempdict)

        #replace value
        variabledict['value'] = variabledict['value'].replace(variable, f"({varVal})")

    #update the value stored in the symboltable
    if variabledict['value'] != None or variabledict['value'] != "":
        variabledict['value'] = evaluateExpression(variabledict['value'])
    symboltable.update_symbol(variabledict)


def evaluateExpression(expression):
    try:
        return eval(expression)
    except:
        pass

def sortByNameLength(x):
    return len(x)


