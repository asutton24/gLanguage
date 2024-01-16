import sys

def binConvert(x):
    temp = ''
    for i in range(6):
        if x >= 2**(5-i):
            temp += '1'
            x -= 2**(5-i)
        else:
            temp += '0'
    return temp

class Machine:
    def __init__(self):
        self.ram = []
        self.chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ .0123456789#*'
        for i in range(64):
            self.ram.append(0)

    def printRam(self):
        counter = 0
        temp = ''
        for i in self.ram:
            temp += binConvert(i)
            if counter % 8 == 7:
                print(temp)
                temp = ''
            else:
                temp += ' '
            counter += 1

    def error(self):
        print('Error')
        sys.exit(0)

    def execute(self, path):
        with open(path, 'r') as file:
            program = file.readlines()
            file.close()
        index = 0
        while index < len(program):
            move = self.sysCall(program[index])
            if move == 1:
                index += 1

    def getAddress(self, x):
        if x[0:1] == '#':
            temp = int(x[1])
            if temp > 63 or temp < 0:
                self.error()
            return temp
        if x[0:1] == '*':
            temp = self.ram[int(x[1])]
            if temp > 63:
                self.error()
            return temp
        self.error()

    def sysCall(self, cmd):
        words = cmd.split()
        if words[0] == 'ITER' or words[0] == 'DITER':
            if len(words) != 2:
                self.error()
            address = self.getAddress(words[1])
            if words[0] == 'ITER':
                self.ram[address] += 1
            else:
                self.ram[address] -= 1
            self.ram[address] %= 64
            return 1
        if words[0] == 'RAM':
            if len(words) != 1:
                self.error()
            self.printRam()
            return 1
        if words[0] == 'RESET':
            if len(words) != 1:
                self.error()
            for i in range(64):
                self.ram[i] = 0
            return 1
        if words[0] == 'SET':
            if len(words) != 3:
                self.error()
            address = self.getAddress(words[1])
            if words[2][0:1] != '#' and words[2][0:1] != '*':
                self.ram[address] = int(words[2])
            else:
                add2 = self.getAddress(words[2])
                self.ram[address] = self.ram[add2]
            self.ram[address] %= 64
            return 1
        if words[0] == 'INC' or words[0] == 'DEC':
            if words[0] == 'INC':
                sign = 1
            else:
                sign = -1
            if len(words) != 3:
                self.error()
            address = self.getAddress(words[1])
            if words[2][0:1] != '#' and words[2][0:1] != '*':
                self.ram[address] += (sign * int(words[2]))
            else:
                add2 = self.getAddress(words[2])
                self.ram[address] += (sign * self.ram[add2])
            self.ram[address] %= 64
            return 1
        if words[0] == 'ADD' or words[0] == 'SUB':
            if words[0] == 'ADD':
                sign = 1
            else:
                sign = -1
            if len(words) != 4:
                self.error()
            if words[1][0:1] != '#' and words[1][0:1] != '*':
                val1 = int(words[1])
            else:
                val1 = self.ram[self.getAddress(words[1])]
            if words[2][0:1] != '#' and words[2][0:1] != '*':
                val2 = int(words[2])
            else:
                val2 = self.ram[self.getAddress(words[2])]
            val2 *= sign
            self.ram[self.getAddress(words[3])] = (val1 + val2) % 64
            return 1
        if words[0] == 'PRINT':
            if words[1][0:1] == '#':
                print(self.ram[int(words[1][1])])
            else:
                print(cmd.split(maxsplit=1)[1])
            return 1
        if words[0] == 'INP':
            if len(words) != 2:
                self.error()
            self.ram[self.getAddress(words[1])] = int(input()) % 64
            return 1
        if words[0] == 'RUN':
            if len(words) != 2:
                self.error()
            self.execute(words[1])
            return 1


mac = Machine()
while True:
    mac.sysCall(input())