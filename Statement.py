from TokenHandler import TokenHandler
from ParserException import ParserException
import VariableException

class Statement(object):

    def __init__(self, tokens):
        self.t = TokenHandler(tokens)

    def createStatement(self, tokens):
        currenttoken = self.t.getCurrentToken()
    
        if currenttoken == "begin":
            s = CompoundStatement(tokens)
            return s
        
        elif self.t.isVariable(currenttoken):
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
            raise ParserException('\';\' expected. Got \'' + currenttoken + '\' instead.')

    def execute(self, skip):
        raise NotImplementedError("Subclass must implement abstract method")
    
class ProgramStatement(Statement):

    programName = None

    def __init__(self, tokens):
        self.t = TokenHandler(tokens)

    def execute(self, skip):   
        self.t.match("program", self.t.tokens)
        currentToken = self.t.getCurrentToken()
        if not skip:
            self.programName = currentToken
        self.t.match(currentToken, self.t.tokens)
        copytokens = list(self.t.tokens)
        c = CompoundStatement(copytokens)
        tokensExecuted = c.execute(skip)
        self.t.moveAhead(tokensExecuted)
        return self.t.resetTokens()
    
class CompoundStatement(Statement):

    def __init__(self, tokens):
        self.t = TokenHandler(tokens)
        
    def execute(self, skip):     
        self.t.match("begin", self.t.tokens)
        currenttoken = self.t.getCurrentToken()
        condition = True
        
        while condition == True:
            copytokens = list(self.t.tokens)
            currentstatement = self.createStatement(copytokens)
            tokensexecuted = currentstatement.execute(skip)
            self.t.moveAhead(tokensexecuted)
            currenttoken = self.t.getCurrentToken()
            if currenttoken == ";":
                condition = True
                self.t.match(";", self.t.tokens)
            else:
                condition = False
            
        self.t.match("end", self.t.tokens)
        return self.t.resetTokens()

class Assignment(Statement):

    def __init__(self, tokens):
        self.t = TokenHandler(tokens)

    def execute(self, skip):
        currenttoken = self.t.getCurrentToken()
        if not self.t.isVariable(currenttoken):
            raise VariableException("Not a variable: " + currenttoken)
        variablebeingassigned = currenttoken
        self.t.match(currenttoken, self.t.tokens)
        self.t.match(":=", self.t.tokens)
        currenttoken = self.t.getCurrentToken()
        variablevalue = None
        if not skip:
            variablevalue = self.t.readTokenValue(currenttoken)
            TokenHandler.variables[variablebeingassigned] = variablevalue
        self.t.match(currenttoken, self.t.tokens)
        
        currenttoken = self.t.getCurrentToken()
        while(self.t.isMathOperator(currenttoken)):
            if currenttoken == "+":
                self.t.match("+", self.t.tokens)
                currenttoken = self.t.getCurrentToken()
                if not skip:
                    operand = self.t.readTokenValue(currenttoken)
                    variablevalue += operand
                    TokenHandler.variables[variablebeingassigned] = variablevalue
                self.t.match(currenttoken, self.t.tokens)
                
            elif currenttoken == "-":
                self.t.match("-", self.t.tokens)
                currenttoken = self.t.getCurrentToken()
                if not skip:
                    operand = self.t.readTokenValue(currenttoken)
                    variablevalue -= operand
                    TokenHandler.variables[variablebeingassigned] = variablevalue
                self.t.match(currenttoken, self.t.tokens)
                
            elif currenttoken == "*":
                self.t.match("*", self.t.tokens)
                currenttoken = self.t.getCurrentToken()
                if not skip:
                    operand = self.t.readTokenValue(currenttoken)
                    variablevalue *= operand
                    TokenHandler.variables[variablebeingassigned] = variablevalue
                self.t.match(currenttoken, self.t.tokens)          
                
            elif currenttoken == "/":
                self.t.match("/", self.t.tokens)
                currenttoken = self.t.getCurrentToken()
                if not skip:
                    operand = self.t.readTokenValue(currenttoken)
                    if operand == 0:
                        raise ParserException("Can't divide by zero.")
                    variablevalue /= operand
                    TokenHandler.variables[variablebeingassigned] = variablevalue
                self.t.match(currenttoken, self.t.tokens)
                
            currenttoken = self.t.getCurrentToken()
            
        return self.t.resetTokens()
    
class Print(Statement):

    def __init__(self, tokens):
        self.t = TokenHandler(tokens)

    def execute(self, skip):
        self.t.match("print", self.t.tokens)
        nexttoken = self.t.getCurrentToken()
        if not skip:
            print(self.t.readTokenValue(nexttoken))
        self.t.match(nexttoken, self.t.tokens)
        return self.t.resetTokens()
    
class IF(Statement):
    
    def __init__(self, tokens):
        self.t = TokenHandler(tokens)
        
    def execute(self, skip):
        self.t.match("if", self.t.tokens)
        currenttoken = self.t.getCurrentToken()
        
        if(skip):
            while(currenttoken != "else"):
                self.t.match(currenttoken, self.t.tokens)
                currenttoken = self.t.getCurrentToken()
            
            self.t.match("else", self.t.tokens)
            copytokens = list(self.t.tokens)
            s = self.createStatement(copytokens)
            tokensexecuted = s.execute(skip)
            self.moveAhead(tokensexecuted)
            
        if(self.t.ConditionIsTrue(self.t.tokens, outcondition = [])):
            self.t.match("then", self.t.tokens)
            copytokens = list(self.t.tokens)
            s = self.createStatement(copytokens)
            tokensexecuted = s.execute(skip)
            self.t.moveAhead(tokensexecuted)
            
            self.t.match("else", self.t.tokens)
            copytokens = list(self.t.tokens)
            s = self.createStatement(copytokens)
            tokensexecuted = s.execute(True)
            self.t.moveAhead(tokensexecuted)
            
        else:
            currenttoken = self.t.getCurrentToken()
            while(currenttoken != "else"):
                self.t.match(currenttoken, self.t.tokens)
                currenttoken = self.t.getCurrentToken()
            
            self.t.match("else", self.t.tokens)
            copytokens = list(self.t.tokens)
            s = self.createStatement(copytokens)
            tokensexecuted = s.execute(skip)
            self.t.moveAhead(tokensexecuted)
            
        return self.t.resetTokens()
    
class While(Statement):
    
    def __init__(self, tokens):
        self.t = TokenHandler(tokens)
        
    def execute(self, skip):
        self.t.match("while", self.t.tokens)
        conditiontokens = []
        conditionistrue = self.t.ConditionIsTrue(self.t.tokens, conditiontokens)
        
        self.t.match("do", self.t.tokens)

        tokensexecuted = None
        
        while(conditionistrue):
            copytokens = list(self.t.tokens)
            s = self.createStatement(copytokens)
            tokensexecuted = s.execute(skip)
            copytokens = list(conditiontokens)
            conditiontokens = None
            conditiontokens = []
            conditionistrue = self.t.ConditionIsTrue(copytokens, conditiontokens)
            size = len(self.t.executedtokens)
            
            i = size - 1
            while(i >= size - len(conditiontokens)):
                self.t.executedtokens.pop(i)
                i -= 1
            
        self.t.moveAhead(tokensexecuted)
        return self.t.resetTokens()