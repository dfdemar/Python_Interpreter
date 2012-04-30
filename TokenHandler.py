import re
from ParserException import ParserException
import VariableException

class TokenHandler(object):

    variables = {}
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.executedtokens = []
    
    def create_Tokens(self, filename):
        lines = []
        scan = open(filename, "r")
        for text in scan:
            lines.extend(text.lower().split())
        scan.close()
      
        for text in lines:
            self.tokens.extend(text.split())
    
    def getCurrentToken(self):
        return self.tokens[0]

    def isVariable(self, token):
        return (token.isalpha() and len(token) == 1)
    
    def isMathOperator(self, token):
        return (token is "+" or token is "-" or token is "*" or token is "/")
    
    def isConstant(self, token):
        return re.match(r'\d+', token)
    
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

    def ConditionIsTrue(self, tokens, outcondition):
        currenttoken = tokens[0]
        leftvalue = self.readTokenValue(currenttoken)
        outcondition.append(currenttoken)
        self.match(currenttoken, tokens)
        currenttoken = tokens[0]
        
        if(currenttoken == "<"):
            return leftvalue < self.readBooleanTokens(outcondition, tokens, currenttoken)
        
        if(currenttoken == ">"):
            return leftvalue > self.readBooleanTokens(outcondition, tokens, currenttoken)
        
        if(currenttoken == "<="):
            return leftvalue <= self.readBooleanTokens(outcondition, tokens, currenttoken)
        
        if(currenttoken == ">="):
            return leftvalue >= self.readBooleanTokens(outcondition, tokens, currenttoken)
        
        if(currenttoken == "="):
            return leftvalue == self.readBooleanTokens(outcondition, tokens, currenttoken)
        
        if(currenttoken == "/="):
            return leftvalue != self.readBooleanTokens(outcondition, tokens, currenttoken)
        
        raise ParserException("Not a valid condition")
            
    def readBooleanTokens(self, outcondition, tokens, currenttoken):
        outcondition.append(currenttoken)
        self.match(currenttoken, tokens)
        currenttoken = tokens[0]
        rightvalue = self.readTokenValue(currenttoken)
        outcondition.append(currenttoken)
        self.match(currenttoken, tokens)
        return rightvalue;
        
    def match(self, token, matchtokens):
        #print("[%s]" % ', '.join(matchtokens))
        if token == matchtokens[0]:
            self.executedtokens.append(token)
            del matchtokens[0]
        else:
            raise ParserException("Unexpected token: " + token)
        
    def resetTokens(self):
        self.tokens = self.executedtokens
        tokenSize = len(self.executedtokens)
        self.executedtokens = None
        return tokenSize
    
    def moveAhead(self, numberofElements):
        for i in range(numberofElements):
            self.match(self.getCurrentToken(), self.tokens)
