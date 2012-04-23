

class ProgramStatement(Statement):

    programName = None

    def __init__(self, tokens):
        super(ProgramStatement, self).__init__(tokens)
        
    def execute(self, skip):
        statement = Statement(self.tokens)
        
        statement.match("program", self.tokens)
        currentToken = statement.getCurrentToken()
        if not skip:
            self.programName = currentToken
        statement.match(currentToken, self.tokens)
        c = CompoundStatement(self.tokens)
        tokensExecuted = c.execute(skip)
        statement.moveAhead(tokensExecuted)
        return Statement.resetTokens()