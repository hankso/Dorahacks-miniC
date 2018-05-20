#!/usr/bin/env python
# coding=utf-8

operators = ['-', '~', '++', '--', '*', '!', '/', '*', '%', '+', '-', 
             '>', '>=', '<', '<=', '==', '!=', '&&', '||', '=']
types = ['int ', 'double ', 'float ', 'char ']
toDelete = types + ['struct ']
toRepleace = [('printf(', 'print('), ('++', ' += 1'), ('--', ' -= 1'),
              ('/*', "'''"), ('*/', "'''"), ('//','#'),
              ('&&', 'and'), ('||', 'or')]

def isDigit(c):
    return c > '0' and c < '9'

def isChar(c):
    return (c > 'a' and c < 'z') or (c > 'A' and c < 'Z')

def isOperator(c):
    return c in operators

def isDefun(line):
    return '(' in line and ')' in line and sum([i in line for i in toDelete])

def isDefStruct(line):
    return 'struct ' in line and len(line.split(' ')) == 2

def isUseStruct(line):
    return 'struct ' in line and len(line.split(' ')) == 3

def isClarify(line):
    return sum([line.startswith(i) for i in types]) and '=' not in line

def isPoint(line):
    index = line.index('*') if '*' in line else -1
    return index != -1 and len(line) > (index + 1) and isChar(line[index + 1]) and \
           (sum([line.startswith(i) for i in types]) or '=' in line)
            

def isList(line):
    return sum([line.startswith(i) for i in types]) and '[' in line and ']' in line

def parseInt(s, start=0):
    tmp = ''
    while start < len(s):
        if isDigit(s[start]):
            tmp += s[start]
        elif len(tmp):
            break
        start += 1
    return int(tmp), start - len(tmp)

def parseVar(s, start=0):
    tmp = ''
    while start < len(s):
        if isChar(s[start]):
            tmp += s[start]
        elif isDigit(s[start]) and len(tmp):
            break
        start += 1
    return tmp, start - len(tmp)

def parseOperator(s, start=0):
    tmp = ''
    while start < len(s):
        if not isDigit(s[start]) and not isChar(s[start]) and s[start] != ' ':
            tmp += s[start]
        elif len(tmp) and isOperator(tmp):
            return tmp, start - len(tmp)
        else:
            tmp = ''
        start += 1
    
def main1(filename, output=None):
    with open(filename, 'r') as f:
        lines = f.readlines()
    if not output:
        output = filename + '.py'
    f = open(output, 'w')
    indent = ''
    instruct = False
    inFor = ''
    for line in lines:
        line = line.lstrip(' ').rstrip(';\n')
        if line.startswith('#'):
            continue
        if '{' in line:
            if instruct:
                f.write(indent + '{\n')
            indent += '    '
        elif '}' in line:
            if inFor:
                f.write('%s%s\n' % (indent, inFor))
                inFor = ''
            indent = indent[:-4]
            if instruct:
                instruct = False
                f.write(indent + '}\n')
#                indent = indent[:-4]
        else:
            s = indent
            if line.startswith('//'):
                s += '{}'
            elif isDefun(line):
                s += 'def {}:'
            elif isUseStruct(line):
                l = line.split(' ')[1:]
                s += ('{} = [{}.copy() for i in range({})]'
                      '').format(l[1][:l[1].index('[')],
                                 l[0], parseInt(l[1], l[1].index('['))[0])
                s += '{}'
                line = ''
            elif isDefStruct(line):
#                indent += '    '
#                s += 'class {}:\n' + indent + 'def __init__(self):'
                s += '{} = \\'
                instruct = True
            elif 'if' in line or 'while ' in line:
                s += '{}:'
            elif 'printf' in line and '%' in line:
                s += '{})'
                first_comma = line.index(',')
                line = line[:first_comma] + ' % (' + line[first_comma + 2:]
            elif 'for' in line:
                line = line[3:].replace('(', '').replace(')', '').strip()
                line = [l.strip() for l in line.split(';')]
                if line[0] and line[1]:
                    s += '%s\n%swhile %s:{}' % (line[0], s, line[1])
                if not line[0] and line[1]:
                    s += 'while %s:{}' % (line[1])
                if line[0] and not line[1]:
                    s += '%s\n%swhile 1:{}' % (line[0], s)
                if not line[0] and not line[1]:
                    s += 'while 1:{}'
                inFor = line[2]
                line = ''
            elif instruct:
#                s += 'self.{} = None'
                s += '"{}": None,'
            elif isClarify(line):
                s += '# Clarify `{}` is skiped'
            else:
                s += '{}'
            if isPoint(line):
                index = -1
                for i in range(line.count('*')):
                    index = line.index('*', index + 1)
                    if isChar(line[index + 1]):
                        line = line[:index] + 'p_' + line[index + 1:]
            s = s.format(line.strip())
            for i, j in toRepleace:
                while i in s:
                    s = s.replace(i, j)
            if not s.strip().startswith('#'):
                for i in toDelete:
                    while i in s:
                        s = s.replace(i, '')
            f.write(s + '\n')
    f.write('if __name__ == "__main__":\n    main()')
    f.close()
    
def main2(filename, output=None):
    with open(filename, 'r') as f:
        lines = f.readlines()
    if not output:
        output = filename + '.py'
    f = open(output, 'w')
    rst = []
    for line in lines:
        line = line.lstrip(' ').rstrip(';\n')
        if line.startswith('#'):
            continue
        
        
    f.close()    
            
if __name__ == '__main__':
    main1('test.c', output='replace.py')
#    main2('test.c', output='list.py')
            