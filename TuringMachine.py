# Michael Mullings
# mcm14n
# COT4420 - TuringMachine.py

def moveCursor(s):
    if s=='L':
        return -1
    else:
        return 1

class TuringMachine:
    def __init__(self, turing):
        self.machine = {}
        self.start, self.final, self.state = '','', ''
        with open(turing, 'r') as file:
            for line in file:
                li=str(line).split()
                if len(li) > 0:
                    self.start+=li[0]+' '
                    self.final+=li[3]+' '
                    self.machine[li[0]+' '+li[1]]=[li[2], li[3], moveCursor(li[4])]
            else:
                if self.start.split()[0]+' *' not in self.machine.keys():
                    self.machine[self.start.split()[0]+' *']=['*', self.start.split()[0],1]
                
    def compute(self, tape):
        self.state, offset=self.start.split()[0], 0
        with open(tape, 'r+') as tapefile:
            with open(tape, 'r+') as tf:
                for line in tapefile:
                    for char in line:
                        if len(char.strip()) > 0:
                            if str(self.state+' '+char) in self.machine and offset > -1:
                                tf.write(self.machine[self.state+' '+char][0])
                                offset+=int(self.machine[self.state+' '+char][2])
                                self.state=self.machine[self.state+' '+char][1]
                                tf.seek(offset)
                            elif str(self.state+' '+char) in self.machine and offset < 0:
                                offset=0
                                tf.write(self.machine[self.state+' '+char][0])
                                offset+=int(self.machine[self.state+' '+char][2])
                                self.state=self.machine[self.state+' '+char][1]
                                tf.seek(offset)
                            else:
                                return 
                        else:
                            return

