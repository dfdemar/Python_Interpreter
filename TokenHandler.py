import re
from ParserException import ParserException
import VariableException

class TokenHandler(object):

    variables = {}

    def isVariable(self, token):
        return (re.match(r'[a-zA-Z]', token) and len(token) == 1)
    
    def isMathOperator(self, token):
        return (token is "+" or token is "-" or token is "*" or token is "/")
    
    def isConstant(self, token):
        return re.match("\d+", token)
    
    def isComparisonOperator(self, token):
        return (token is "<" or token is ">" or token is "<=" or token is ">=" or token is "=" or token is "/=")
    
    def readTokenValue(self, token):
        if(self.isVariable(token)):
            variablevalue = self.variables.get(token)
            if variablevalue == None:
                raise ParserException("Variable " + token + " not assigned.")
            return variablevalue
        
        elif(self.isConstant(token)):
            return int(token)
        
        else:
            raise VariableException("Not a valid variable: " + token)
