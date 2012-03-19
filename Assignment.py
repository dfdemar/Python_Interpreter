from Statement import Statement
from TokenHandler import TokenHandler
import VariableException

class Assignment(Statement):

    def __init__(self, tokens = []):
        super(Assignment, self).__init__(tokens)
        
    def execute(self, skip):
        statement = Statement(self.tokens)
        t = TokenHandler()
        currenttoken = statement.getCurrentToken()
        if not t.isVariable(currenttoken):
            raise VariableException("Not a variable: " + currenttoken)
        variablebeingassigned = currenttoken[0]
        statement.matchToken(currenttoken, self.tokens)
        variablevalue = None
        if not skip:
            variablevalue = t.readTokenValue(currenttoken)
            t.variables = {variablebeingassigned:variablevalue}
        statement.matchToken(currenttoken, self.tokens)
        
        currenttoken = statement.getCurrentToken()
        while(t.isMathOperator(currenttoken)):
            if currenttoken == "+":
                statement.matchToken("+", self.tokens)
                currenttoken = statement.getCurrentToken()
                if not skip:
                    operand = t.readTokenValue(currenttoken)
                    variablevalue += operand
                    t.variables.update(variablebeingassigned, variablevalue)
                statement.matchToken(currenttoken, self.tokens)
                
            elif currenttoken == "-":
                statement.matchToken("-", self.tokens)
                currenttoken = statement.getCurrentToken()
                if not skip:
                    operand = t.readTokenValue(currenttoken)
                    variablevalue -= operand
                    t.variables.update(variablebeingassigned, variablevalue)
                statement.matchToken(currenttoken, self.tokens)
                
            elif currenttoken == "*":
                statement.matchToken("*", self.tokens)
                currenttoken = statement.getCurrentToken()
                if not skip:
                    operand = t.readTokenValue(currenttoken)
                    variablevalue *= operand
                    t.variables.update(variablebeingassigned, variablevalue)
                statement.matchToken(currenttoken, self.tokens)          
                
            elif currenttoken == "/":
                statement.matchToken("/", self.tokens)
                currenttoken = statement.getCurrentToken()
                if not skip:
                    operand = t.readTokenValue(currenttoken)
                    variablevalue /= operand
                    t.variables.update(variablebeingassigned, variablevalue)
                statement.matchToken(currenttoken, self.tokens)
                
            currenttoken = statement.getCurrentToken()
            
        return statement.resetTokens()   
                