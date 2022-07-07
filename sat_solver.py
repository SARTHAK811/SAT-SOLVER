from pickle import FALSE
import math
import itertools
import numpy as np 
import copy

def get_formula():
     
    file=open("test_code.cnf",'r')#opening the input file
    lines=file.readlines()
    file.close()
    form=[]
    count_of_c=0
    num_clauses=0
    for i in lines:
        if(i[0]!='c'):
            if(i[0]=='p'):
                num_var=int(i.split()[2])#following the DIMAC representation
                num_clauses=int(i.split()[3])#following the DIMAC representation
                break
        else:
            count_of_c=count_of_c+1
    #print(num_clauses)
    for i in range(count_of_c+1,count_of_c+num_clauses+1):
        temp=[]
        temp.append([int(j) for j in lines[i].split()])#temp is a list of list
        #print(temp)
        temp[0].remove(0)#so removing 0 from temp[0]
        form.append(temp[0])#form should also be list of list so we append temp[0] to form
    return form,num_var

def check_empty_clause(formula):#check for empty clause
    for i in formula:
        if(len(i)==0):
            return True

def check_unit_literal(formula):# check for unit literals
    unit_array=[]
    flag=1
    if(len(formula)==0):
        return 0
    for i in formula:
        if(len(i)==1):
            literal=i[0]
            flag=0
            return literal
        
    return 0
          
def check_pure_literal(formula,num):
     final=1
     start=1
     flag=1#check for the literal with the same polarity called as pure literal
     for i in range(1,num+1):
         final=1
         start=1
         flag=1
         for j in formula:
             if(final==0):
                 break
             for k in j:
                 if(k==i or k==(-i)):
                    if ( k>0 and start==1):
                         start=0
                         flag=1
                    elif( k<0 and start==1):
                         start=0
                         flag=0
                    elif( k>0 and flag==0):
                        final=0
                    elif( k<0 and flag==1):
                         final=0 
                 else:
                    continue
                     
         if(final==1 and start==0 and flag==1):
             return i 
         elif(final==1 and start==0 and flag==0):
            return -i
     return 0

def dpll_algorithm(formula,literal,num):#dpll algorithm for sat solver
    global final_ans
    temp=[]
    if(literal>0):#setting final_ans[literal-1] as True if literal>0 and false if it is <0
        temp.append(literal-1)
        final_ans[literal-1]=1
    elif(literal<0):
        temp.append(-literal-1)
        final_ans[-literal-1]=0
    delete=[]
    for i in formula:
        for j in i:
            if(j==literal):
                delete.append(i)
            elif((-j)==literal):
                i.remove(j)#removing (-literal) from each clause if it is present
                
    for j in delete:
        formula.remove(j)#removing the entire clause as the entire clause becomes true

    if(len(formula)==0):#if formula is empty then return true
        return True
    elif(check_empty_clause(formula)):#if a clause is empty then return false
        for i in temp:
                    
                    final_ans[i]=0
        return False
    global array
    
    len_initial=len(formula)
    while(True):#set all the unit literals recursively as possible
        var=check_unit_literal(formula)
        delete=[]
        if(var!=0):
            if(var>0):
                final_ans[var-1]=1
                temp.append(var-1)
            elif(var<0):
                final_ans[-var-1]=0
                temp.append(-var-1)
            for i in formula:
                for j in i:
                    if(j==var):
                        delete.append(i)
                    elif((-j)==var):
                        i.remove(j)#removing -var from the clauses wherever it is present
            for j in delete:
                 formula.remove(j)#removing all the clauses which contain var
       
        len_new=len(formula)
        if(len_new==len_initial):
            break
        len_initial=len_new    
        if(var==0):
            break

    if(len(formula)==0):#check if formula is empty then return true
        return True
    elif(check_empty_clause(formula)):#if a clause is empty then return false
        for i in temp:
                    
                    final_ans[i]=0
        return False
    while(True):#set all the possible pure literals(literals with the same polarity throughout) recursively as possible
        char=check_pure_literal(formula,num)
        del_2=[]
        if(char!=0):
            if(char>0):
                final_ans[char-1]=1
                temp.append(char-1)
            elif(var<0):
                final_ans[-char-1]=0
                temp.append(-char-1)
            for i in formula:
                for j in i:
                  if(j==char):
                     del_2.append(i)
                  elif((-j)==char):
                    i.remove(j)#removing -char from the clauses wherever it is present
                
            for j in del_2:
                 formula.remove(j)#removing all the clauses which contain char
        
        len_new=len(formula)
        if(len_new==len_initial):
            break
        len_initial=len_new 
        if(char==0):
            break
    if(len(formula)==0):#check if formula is empty then return true
        return True
    elif(check_empty_clause(formula)):#if a clause is empty then return false
        for i in temp:
                    
                    final_ans[i]=0
        return False
    
    new=[]
    length=[]
    for i in formula:#MOM's heuristic  i.e maximum occurences in minimum length clauses
         new.append(i)
         length.append(len(i))
    size=min(length)#finding the minimum possible length of clauses present in the formula

    freq=[0 for i in range(num)]
    for i in formula:
        if(len(i)==size):
           for j in i:
               freq[abs(j)-1]=freq[abs(j)-1]+1
    max_freq=max(freq)#finding maximum frequency of a literal in the set of minimum length clauses
    for i in range(0,num):
        if(freq[i]==max_freq):
            x=i+1#finding that literal 

    if(len(formula)==0):
        return True
    else:
        input_1=copy.deepcopy(formula)
        if(dpll_algorithm(input_1,x,num)):#setting x as true
            return True
        else:
            input_2=copy.deepcopy(formula)
            if(dpll_algorithm(new,-x,num)):#setting x as false
                return True
            else :
                for i in temp:
                    
                    final_ans[i]=0
                return False


global final_ans
ques,number=get_formula()
#print(ques)
#print(number)
final_ans=[0 for i in range(number)]
if(dpll_algorithm(ques,0,number)):
    print("SAT")
    #print(final_ans)
    answer=[]
    for i in range(0,number):
        if(final_ans[i]==1):
            answer.append(i+1)
        elif(final_ans[i]==0):
            answer.append(-(i+1))
    print("The model is:",end=" " )
    print(answer)
else:
    print("UNSAT")