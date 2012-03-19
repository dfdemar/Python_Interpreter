from Statement import Statement

class CompoundStatement(Statement):

    def __init__(self, tokens = []):
        super(CompoundStatement, self).__init__(tokens)
        
    def execute(self, skip):
        statement = Statement(self.tokens)        
        statement.matchToken("begin", self.tokens)
        currenttoken = statement.getCurrentToken()
        
        while currenttoken is not "end":
            currentstatement = statement.createStatement()
            tokensexecuted = currentstatement.execute(skip)
            statement.moveAhead(tokensexecuted)
            currenttoken = statement.getCurrentToken()
            
        statement.matchToken("end", self.tokens)
        return statement.resetTokens()