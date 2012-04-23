import re
from TokenHandler import TokenHandler
from ParserException import ParserException
import VariableException

class Statement(object):

    #tokens = []
    #executedtokens = []

    def __init__(self, tokens):
        self.tokens = tokens
        self.executedtokens = []

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
            a = Assignment(self.tokens)
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
        self.match(currenttoken, tokens)
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
        self.match(currenttoken, tokens)
        currenttoken = tokens(0)
        rightvalue = TokenHandler.readTokenValue(self, currenttoken)
        outcondition.extend(currenttoken)
        self.match(currenttoken, tokens)
        return rightvalue;
        
    def match(self, token, matchtokens):
        if token == matchtokens[0]:
            self.executedtokens.append(token)
            del matchtokens[0]
        else:
            raise ParserException("Unexpected token: " + token)
        
    def resetTokens(self):
        del self.tokens[:]
        self.tokens = self.executedtokens
        tokenSize = len(self.executedtokens)
        del self.executedtokens[:]
        return tokenSize
    
    def moveAhead(self, numberofElements):
        for index in range(numberofElements):
            self.match(self.getCurrentToken(), self.tokens)

    def execute(self, skip):
        raise NotImplementedError("Subclass must implement abstract method")
    
class ProgramStatement(Statement):

    programName = None

    def __init__(self, tokens):
        super(ProgramStatement, self).__init__(tokens)
        
    def execute(self, skip):   
        self.match("program", self.tokens)
        currentToken = self.getCurrentToken()
        if not skip:
            self.programName = currentToken
        self.match(currentToken, self.tokens)
        c = CompoundStatement(self.tokens)
        tokensExecuted = c.execute(skip)
        self.moveAhead(tokensExecuted)
        return Statement.resetTokens()
    
class CompoundStatement(Statement):

    def __init__(self, tokens):
        super(CompoundStatement, self).__init__(tokens)
        
    def execute(self, skip):     
        self.match("begin", self.tokens)
        currenttoken = self.getCurrentToken()
        
        while currenttoken is not "end":
            currentstatement = self.createStatement()
            tokensexecuted = currentstatement.execute(skip)
            self.moveAhead(tokensexecuted)
            currenttoken = self.getCurrentToken()
            
        self.matchToken("end", self.tokens)
        return self.resetTokens()

class Assignment(Statement):

    def __init__(self, tokens):
        super(Assignment, self).__init__(tokens)

    def execute(self, skip):
        t = TokenHandler()
        currenttoken = self.getCurrentToken()
        if not t.isVariable(currenttoken):
            raise VariableException("Not a variable: " + currenttoken)
        variablebeingassigned = currenttoken
        self.match(currenttoken, self.tokens)
        self.match(":=", self.tokens)
        currenttoken = self.getCurrentToken()
        variablevalue = None
        if not skip:
            variablevalue = t.readTokenValue(currenttoken)
            t.variables = {variablebeingassigned:variablevalue}
        self.match(currenttoken, self.tokens)
        
        currenttoken = self.getCurrentToken()
        while(t.isMathOperator(currenttoken)):
            if currenttoken == "+":
                Statement.match("+", self.tokens)
                currenttoken = self.getCurrentToken()
                if not skip:
                    operand = t.readTokenValue(currenttoken)
                    variablevalue += operand
                    t.variables.update(variablebeingassigned, variablevalue)
                self.match(currenttoken, self.tokens)
                
            elif currenttoken == "-":
                self.match("-", self.tokens)
                currenttoken = self.getCurrentToken()
                if not skip:
                    operand = t.readTokenValue(currenttoken)
                    variablevalue -= operand
                    t.variables.update(variablebeingassigned, variablevalue)
                self.match(currenttoken, self.tokens)
                
            elif currenttoken == "*":
                self.match("*", self.tokens)
                currenttoken = self.getCurrentToken()
                if not skip:
                    operand = t.readTokenValue(currenttoken)
                    variablevalue *= operand
                    t.variables.update(variablebeingassigned, variablevalue)
                self.match(currenttoken, self.tokens)          
                
            elif currenttoken == "/":
                self.match("/", self.tokens)
                currenttoken = self.getCurrentToken()
                if not skip:
                    operand = t.readTokenValue(currenttoken)
                    variablevalue /= operand
                    t.variables.update(variablebeingassigned, variablevalue)
                self.match(currenttoken, self.tokens)
                
            currenttoken = self.getCurrentToken()
            
        return self.resetTokens()
    
class Print(object):

    def __init__(self, tokens):
        super(Print, self).__init__(tokens)

    def execute(self, skip):
        self.match("print", self.tokens)
        nexttoken = self.getCurrentToken()
        if not skip:
            print TokenHandler.readTokenValue(self, nexttoken)
        self.match(nexttoken, self.tokens)
        return self.resetTokens()