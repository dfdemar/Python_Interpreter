import re
from Print import Print
from TokenHandler import TokenHandler
from IF import IF
from While import While
from ParserException import ParserException

class Statement(object):

    tokens = []
    executedTokens = []

    def __init__(self, tokenlist):
        self.tokens = tokenlist

    def getCurrentToken(self):
        print self.tokens[0]
        return self.tokens[0]

    def createStatement(self):
        currenttoken = self.getCurrentToken()

        t = TokenHandler()
        
        if currenttoken == "print":
            p = Print(self.tokens)
            return p
        
        elif t.isVariable(currenttoken):
            a = self.Assignment(self.tokens)
            return a
        
        elif currenttoken == "if":
            i = IF(self.tokens)
            return i
        
        elif currenttoken == "while":
            w = While(self.tokens)
            return w
        
        elif currenttoken == "begin":
            s = self.CompoundStatement(self.tokens)
            return s
        
        else:
            raise ParserException('Reserved word \'end\' expected')
        

    def ConditionIsTrue(self, tokens = [], outcondition = []):
        currenttoken = tokens[0]
        leftvalue = TokenHandler.readTokenValue(self, currenttoken)
        outcondition.extend(currenttoken)
        self.matchToken(currenttoken, tokens)
        currenttoken = tokens(0)
        
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
        outcondition.extend(currenttoken)
        self.matchToken(currenttoken, tokens)
        currenttoken = tokens(0)
        rightvalue = TokenHandler.readTokenValue(self, currenttoken)
        outcondition.extend(currenttoken)
        self.matchToken(currenttoken, tokens)
        return rightvalue;
        
    def matchToken(self, token, matchTokens):
        if(matchTokens is None):
            self.matchToken(token, self.tokens)
        if token == matchTokens[0]:
            self.executedTokens.extend(token)
            del matchTokens[0]
        
        else:
            raise ParserException("Unexpected token: " + token)
        
    def resetTokens(self):
        del self.tokens
        self.tokens = self.executedTokens
        tokenSize = len(self.executedTokens)
        del self.executedTokens
        return tokenSize
    
    def moveAhead(self, numberofElements):
        for index in range(len(numberofElements)):
            self.matchToken(self.getCurrentToken(), self.tokens)

    def execute(self, skip):
        raise NotImplementedError("Subclass must implement abstract method")

    