from Statement import ProgramStatement
from TokenHandler import TokenHandler

filename = "prog1.txt"
tokens = []
t = TokenHandler(tokens)
t.create_Tokens(filename)

program = ProgramStatement(t.tokens)
program.execute(False)