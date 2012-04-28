from Statement import ProgramStatement
from TokenHandler import TokenHandler

filename = "C:/David/School/prog3.txt"
t = TokenHandler()
tokens = t.create_Tokens(filename)

program = ProgramStatement(tokens)
program.execute(False)