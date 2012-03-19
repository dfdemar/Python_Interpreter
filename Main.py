from ProgramStatement import ProgramStatement

lines = []
scan = open("C:/David/School/prog1.txt", "r")

for text in scan:
    lines.extend(text.split())
    
tokens = []
    
for text in lines:
    if(";" not in text):
        tokens.extend(text.split())
        
print tokens

program = ProgramStatement(tokens)
program.execute(False)