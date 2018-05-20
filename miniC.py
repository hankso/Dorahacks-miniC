# -*- coding: utf-8 -*-
"""
Created on Sat May 19 22:54:21 2018

@author: jxy
"""
import numpy as np
keyword = ['auto','double','int','struct','break','else','long','switch','case','enum','register','typedef','char',
    'extern','return','union','const','float','short','unsigned','continue','for','signed','void','default','goto',
    'sizeof','volatile','do','while','static','if','inline','restrict','_Alignas','_alignof','_Atomic','_Bool','_Complex'
    '_Generic','_Imaginary','_Noreturn','_Static_assert','_Therad_local']
symbol = ['==','!=','>','<','<=','>=','!','&','?','\'','\"','{','}','[',']','(',')','*','+','-','=',':',';']

def IsDigital(a):
    if ord(a) > 47 and ord(a) < 58:
        return 1;
    return 0;
def IsLetter(a):
    if (ord(a) > 64 and ord(a) < 91) or ( ord(a) > 96 and ord(a) < 123 ) or a == '_':
        return 1;
    return 0;
def IsSymbol(a):
    for k in symbol:
        if a == k:
            return 1
    return 0
def IsKeyword(a):
    for k in keyword:
        if a == k:
            return 1
    return 0
def main():
    level = 0
    level_list = [0]
    rst = []
    result = '['
    f = open('test.c','rb')
    content = f.read().decode('utf-8')#可能会超，之后改成读一行？
    f.close()
    start=0
    end=0
    continuity=0
    digital=0
    qMark=0#标准双引号
    point=0#标记指针
    insertPoint=0
    bucketCount = 1
    for i in range(len(content)):
        if qMark==1:
            if content[i]=='\"':
                end=i
                temp=content[start:end]
                print('字符串 '+temp+'\"')
                result=result+temp+'\"'
                rst.append(temp+'\"')
                if level > level_list[-1]:
                    rst.insert(-1, '[')
                elif level < level_list[-1]:
                    rst.insert(-1, ']')
                level_list.append(level)
                qMark=0
            continue
        if point==1:
            if IsDigital(content[i])==0 and IsLetter(content[i])==0:
                end=i
                temp=content[start:end]
                print('指针 '+temp)
                point=0
            continue
        if IsDigital(content[i]):
            if continuity==0:
                start=i
                continuity=1
                digital=1
        elif IsLetter(content[i]):
            if continuity==0:
                #print('fuck'+content[i])
                start=i
                continuity=1
        elif content[i]=='\"':
            if continuity==0:
                #print('fuck'+content[i])
                start=i
                qMark=1
        elif IsSymbol(content[i]):
            if continuity==1:
                end=i
                temp=content[start:end]
                if content[i]=='(':
                    print('函数名 '+temp)
                    result=result+','+temp+'['
                    rst.append(temp)
                    if level > level_list[-1]:
                        rst.insert(-1, '[')
                    elif level < level_list[-1]:
                        rst.insert(-1, ']')
                    level_list.append(level)
                elif IsKeyword(temp):
                    print('保留字 '+temp)
                    if temp=='if' or temp=='while'or temp=='for':
                        result=result+','+temp
                    rst.append(temp)
                    if level > level_list[-1]:
                        rst.insert(-1, '[')
                    elif level < level_list[-1]:
                        rst.insert(-1, ']')
                    level_list.append(level)
                elif digital==1:
                    print('数字 '+temp)
                    result=result+','+temp
                    rst.append(temp)
                    if level > level_list[-1]:
                        rst.insert(-1, '[')
                    elif level < level_list[-1]:
                        rst.insert(-1, ']')
                    level_list.append(level)
                    digital=0
                else:
                    print('变量名 '+temp)
                    result=result+','+temp
                    rst.append(temp)
                    if level > level_list[-1]:
                        rst.insert(-1, '[')
                    elif level < level_list[-1]:
                        rst.insert(-1, ']')
                    level_list.append(level)
                continuity=0
            elif content[i]=='*':
                if IsLetter(content[i+1]):
                    start=i
                    point=1
                    continue
            print ('符号 '+content[i])
            if content[i]=='{' or content[i] == '(':
                level += 1
                result=result+',['
            if content[i]=='}' or content[i] == ')':
                level -= 1
                result=result+']'
            if content[i]=='='or content[i]=='+'or content[i]=='-'or content[i]=='*'or content[i]=='/' or content[i]=='>'or content[i]=='<' :
                result=result+','+content[i]
                rst.append(content[i])
                if level > level_list[-1]:
                    rst.insert(-1, '[')
                elif level < level_list[-1]:
                    rst.insert(-1, ']')
                level_list.append(level)
        elif continuity==1:
                end=i
                temp=content[start:end]
                if IsKeyword(temp):
                    print('保留字 '+temp)
                    if temp=='if' or temp=='while'or temp=='for' or temp=='return':
                        result=result+','+temp
                        rst.append(temp)
                        if level > level_list[-1]:
                            rst.insert(-1, '[')
                        elif level < level_list[-1]:
                            rst.insert(-1, ']')
                        level_list.append(level)
                elif digital==1:
                    print('数字 '+temp)
                    digital=0
                    result=result+','+temp
                    rst.append(temp)
                    if level > level_list[-1]:
                        rst.insert(-1, '[')
                    elif level < level_list[-1]:
                        rst.insert(-1, ']')
                    level_list.append(level)
                else:
                    print('变量名 '+temp)
                    result=result+','+temp
                    rst.append(temp)
                    if level > level_list[-1]:
                        rst.insert(-1, '[')
                    elif level < level_list[-1]:
                        rst.insert(-1, ']')
                    level_list.append(level)
                continuity=0
            
    result=result+']'       
    fout =open('result.txt','w',encoding='utf-8')
    print(result)
    print('')
    print(level_list)
    print(str(rst))
    print(' '.join(rst))
    fout.write(result)
    fout.close()
    return level_list, rst

if __name__ == '__main__':
    main()