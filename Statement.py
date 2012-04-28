import re
from TokenHandler import TokenHandler
from ParserException import ParserException
import VariableException

class Statement(object):

    def __init__(self, tokens):
        self.tokens = tokens
        self.executedtokens = []

    def getCurrentToken(self):
        return self.tokens[0]

    def createStatement(self, tokens):
        currenttoken = self.getCurrentToken()

        t = TokenHandler()
        
        if currenttoken == "begin":
            s = CompoundStatement(tokens)
            return s
        
        elif t.isVariable(currenttoken):
            a = Assignment(tokens)
            return a
        
        elif currenttoken == "print":
            p = Print(tokens)
            return p
        
        elif currenttoken == "if":
            i = IF(tokens)
            return i
        
        elif currenttoken == "while":
            w = While(tokens)
            return w
        
        else:
            raise ParserException('Reserved word \'end\' expected. Got \'' + currenttoken + '\' instead.')
        

    def ConditionIsTrue(self, tokens, outcondition):
        t = TokenHandler()        
        currenttoken = tokens[0]
        leftvalue = t.readTokenValue(currenttoken)
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
        t = TokenHandler()
        outcondition.append(currenttoken)
        self.match(currenttoken, tokens)
        currenttoken = tokens[0]
        rightvalue = t.readTokenValue(currenttoken)
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
        copytokens = list(self.tokens)
        c = CompoundStatement(copytokens)
        tokensExecuted = c.execute(skip)
        self.moveAhead(tokensExecuted)
        return self.resetTokens()
    
class CompoundStatement(Statement):

    def __init__(self, tokens):
        super(CompoundStatement, self).__init__(tokens)
        
    def execute(self, skip):     
        self.match("begin", self.tokens)
        currenttoken = self.getCurrentToken()
        
        while currenttoken != "end":
            copytokens = list(self.tokens)
            currentstatement = self.createStatement(copytokens)
            tokensexecuted = currentstatement.execute(skip)
            self.moveAhead(tokensexecuted)
            currenttoken = self.getCurrentToken()
            
        self.match("end", self.tokens)
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
            TokenHandler.variables[variablebeingassigned] = variablevalue
        self.match(currenttoken, self.tokens)
        
        currenttoken = self.getCurrentToken()
        while(t.isMathOperator(currenttoken)):
            if currenttoken == "+":
                self.match("+", self.tokens)
                currenttoken = self.getCurrentToken()
                if not skip:
                    operand = t.readTokenValue(currenttoken)
                    variablevalue += operand
                    TokenHandler.variables[variablebeingassigned] = variablevalue
                self.match(currenttoken, self.tokens)
                
            elif currenttoken == "-":
                self.match("-", self.tokens)
                currenttoken = self.getCurrentToken()
                if not skip:
                    operand = t.readTokenValue(currenttoken)
                    variablevalue -= operand
                    TokenHandler.variables[variablebeingassigned] = variablevalue
                self.match(currenttoken, self.tokens)
                
            elif currenttoken == "*":
                self.match("*", self.tokens)
                currenttoken = self.getCurrentToken()
                if not skip:
                    operand = t.readTokenValue(currenttoken)
                    variablevalue *= operand
                    TokenHandler.variables[variablebeingassigned] = variablevalue
                self.match(currenttoken, self.tokens)          
                
            elif currenttoken == "/":
                self.match("/", self.tokens)
                currenttoken = self.getCurrentToken()
                if not skip:
                    operand = t.readTokenValue(currenttoken)
                    if operand == 0:
                        raise ParserException("Can't divide by zero.")
                    variablevalue /= operand
                    TokenHandler.variables[variablebeingassigned] = variablevalue
                self.match(currenttoken, self.tokens)
                
            currenttoken = self.getCurrentToken()
            
        return self.resetTokens()
    
class Print(Statement):

    def __init__(self, tokens):
        super(Print, self).__init__(tokens)

    def execute(self, skip):
        t = TokenHandler()
        self.match("print", self.tokens)
        nexttoken = self.getCurrentToken()
        if not skip:
            print t.readTokenValue(nexttoken)
        self.match(nexttoken, self.tokens)
        return self.resetTokens()
    
class IF(Statement):
    
    def __init__(self, tokens):
        super(IF, self).__init__(tokens)
        
    def execute(self, skip):
        self.match("if", self.tokens)
        currenttoken = self.getCurrentToken()
        
        if(skip):
            while(currenttoken != "else"):
                self.match(currenttoken, self.tokens)
                currenttoken = self.getCurrentToken()
            
            self.match("else", self.tokens)
            copytokens = list(self.tokens)
            s = self.createStatement(copytokens)
            tokensexecuted = s.ececute(skip)
            self.moveAhead(tokensexecuted)
            
        if(self.ConditionIsTrue(self.tokens, outcondition = [])):
            self.match("then", self.tokens)
            copytokens = list(self.tokens)
            s = self.createStatement(copytokens)
            tokensexecuted = s.execute(skip)
            self.moveAhead(tokensexecuted)
            
            self.match("else", self.tokens)
            copytokens = list(self.tokens)
            s = self.createStatement(copytokens)
            tokensexecuted = s.execute(True)
            self.moveAhead(tokensexecuted)
            
        else:
            currenttoken = self.getCurrentToken()
            while(currenttoken != "else"):
                self.match(currenttoken, self.tokens)
                currenttoken = self.getCurrentToken()
            
            self.match("else", self.tokens)
            copytokens = list(self.tokens)
            s = self.createStatement(copytokens)
            tokensexecuted = s.execute(skip)
            self.moveAhead(tokensexecuted)
            
        return self.resetTokens()
    
class While(Statement):
    
    def __init__(self, tokens):
        super(While, self).__init__(tokens)
        
    def execute(self, skip):
        self.match("while", self.tokens)
        conditiontokens = []
        conditionistrue = self.ConditionIsTrue(self.tokens, conditiontokens)
        
        self.match("do", self.tokens)

        tokensexecuted = None
        
        while(conditionistrue):
            copytokens = list(self.tokens)
            s = self.createStatement(copytokens)
            tokensexecuted = s.execute(skip)
            copytokens = list(conditiontokens)
            conditiontokens = None
            conditiontokens = []
            conditionistrue = self.ConditionIsTrue(copytokens, conditiontokens)
            size = len(self.executedtokens)
            
            i = size - 1
            while(i >= size - len(conditiontokens)):
                self.executedtokens.pop(i)
                i -= 1
            
        self.moveAhead(tokensexecuted)
        return self.resetTokens()