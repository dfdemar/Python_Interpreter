from Statement import ProgramStatement

lines = []
scan = open("C:/David/School/prog3.txt", "r")

for text in scan:
    lines.extend(text.lower().split())
scan.close()
    
tokens = []
    
for text in lines:
    if(";" not in text):
        tokens.extend(text.split())
        
print tokens

program = ProgramStatement(tokens)
program.execute(False)