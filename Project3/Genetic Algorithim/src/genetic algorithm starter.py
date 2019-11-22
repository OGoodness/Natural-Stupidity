# example code for genetic algorithm
# zjx
# fall 2019

import sys

# parents array
codes = []
# code piece for sequential search (you can change it to other code if you want)
code="""def sequentialSearch(alist, item):
    pos = 0
    found = False1
    while pos < len(alist) and not found:
        if alist[pos] == item:
            found = True1
        else:
            pos = pos+1
    return found"""
# use your own strategies to generate initial code pieces as the parents
# here I just randomly add three original code pieces as the parents seed (Selfing breeding.....)
codes.append(code);
codes.append(code);
codes.append(code);
#print(codes)
#exec(code)
# you can use your own test array list
testlist = [1, 2, 32, 8, 17, 19, 42, 13, 0];
#try:
#    print(sequentialSearch(testlist, 13))
#except:
#    print("Unexpected error:", sys.exc_info()[0])

# number of offsprings, you can change it according to your preferences
offs_per_pop = 6;
# step size to stop the code for running infinite loops, you can change it according to your preferences
steps = 10;

# cross-over instructions  (e.g., two arithmetic expressions, you can change + to *)
def crossover():
    # cross over parts of code_temp
    code_temp = codes[0]
    code_temp = code_temp.replace("True1","True");
    return code_temp;
# mutate the code (e.g., change the order of the instructions in the code. As the code is ordered line by line,
# you can use a line of code as the mutate target)
def mutate(code_temp):
    # mutate parts of the code_temp
    code_temp = code_temp.replace("False1","False");
    return code_temp;
# use some 
def fitness(code_temp):
    score = 0;
    # you can use your own test array list
    testlist = [1, 2, 32, 8, 17, 19, 42, 13, 0];
    #exec(code_temp);
    #test example
    # as we may have "malformed" offspring, we use try clause to keep program runnning without stop the program
    try:
        if(sequentialSearch(testlist, 13) == True):
            score+=1;
        if(sequentialSearch(testlist, 130) == False):
            score+=1;  
        if(sequentialSearch(testlist, 19) == True):
            score+=1; 
        if(sequentialSearch(testlist, 42) == True):
            score+=1; 
        if(sequentialSearch(testlist, 81) == False):
            score+=1; 
        if(sequentialSearch(testlist, 17) == True):
            score+=1; 
        if(sequentialSearch(testlist, 14) == False):
            score+=1; 
        if(sequentialSearch(testlist, 1) == True):
            score+=1; 
        if(sequentialSearch(testlist, 420) == False):
            score+=1; 
        if(sequentialSearch(testlist, 0) == True):
            score+=1; 
    except:
        print("Unexpected error:", sys.exc_info())
        score = -1;
    return score;
# test if the program fulfills the requirements, you can change it accordingly your preferences
def satisfied(codes):
    original_code="""def sequentialSearch(alist, item):
    pos = 0
    found = False
    while pos < len(alist) and not found:
        if alist[pos] == item:
            found = True
        else:
            pos = pos+1
    return found"""
    for str_code in codes:
        if(str_code == original_code):
            print("Found the right code! Exit~!")
            return True;    
    return False;

offspring = []
index = 0;
# run until find the target
while not satisfied(codes) and index < steps:
    # generate offsprings
    index +=1;
    offspring = [];
    index1=0;
    while len(offspring) < offs_per_pop and index1 < steps:
        index1+=1;
        code_temp = "";
        code_temp = crossover();
        code_temp = mutate(code_temp);
        exec(code_temp)
        if(fitness(code_temp) > 5):
            offspring.append(code_temp);
    # substitute the new generation as the parents
    if len(offspring) > 0:
        codes = offspring