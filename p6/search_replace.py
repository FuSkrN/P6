import re

def findVars(expression):
    variableRegex = re.compile('[a-zA-Z][a-zA-Z0-9]*')
    variables = re.findall(variableRegex, expression)
    return variables

def replaceVars(expression):
    varsInExpression = findVars(expression)
    varsInExpression.sort(key=sortByNameLength, reverse=True)

    #replace the value with found value
    for variable in varsInExpression:
        #first step is to find the actual value in the symbol table
        #here a dummy value is provided. TODO: change this!
        varVal = "1"

        expression = expression.replace(variable, f"({varVal})")
    return expression

def evaluateExpression(expression):
    return str(eval(expression))

def sortByNameLength(x):
    return len(x)
