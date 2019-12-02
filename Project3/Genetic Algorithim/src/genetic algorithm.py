import random
import re
from operator import itemgetter
from time import sleep


def categorize_variables(codeArray):
    variables = {"string": [],
                 "number": [],
                 "variable": [],
                 "array": []
                }
    for line in codeArray:
        if '=' in line:
            line = re.sub('\s+', '', line)
            variable_name, value = line.split('=')

            string_rules = ['\'' in value,
                            '"' in value,
                            '\'' in value,
                            value not in variables["string"]]
            number_rules = [bool(re.search(r'\d', value)) == True,
                            not all(string_rules),
                            value not in variables["number"]
                            ]
            array_rules = [value[0] == '[',
                           value not in variables["array"]
                           ]
            variable_rules = [not all(string_rules),
                              bool(re.search('[a-zA-Z]', value)) == True,
                              value not in variables["variable"]
                              ]
            if all(number_rules):
                variables["number"].append(variable_name)
            elif all(string_rules):
                variables["string"].append(variable_name)
            elif all(variable_rules):
                variables["variable"].append(variable_name)
            elif all(array_rules):
                variables["array"].append(variable_name)

    return variables
def swap_variables(codeArray):
    variables = categorize_variables(codeArray)
    output = []
    for line in codeArray:
        decider = random.randint(0, 1)
        if decider >= 1:
            for key, value in variables.items():
                if any(var in value for var in line):
                    matching = [s for s in value if s in line]
                    for var in matching:
                        line = line.replace(var, random.choice(value))
        output.append(line)
    return output


def mutate(code):
    codeArray = code.splitlines()
    codeArray = change_order(codeArray)
    codeArray = swap_variables(codeArray)
    codeArray = ChangeAssignmentOperation(codeArray)
    return '\n'.join(str(e) for e in codeArray)


def Crossover(parents):
    previous = ''
    genes = {"top": [], "bottom": [] }
    children = []
    for parent in parents:
        if parent != previous:
            previous = parent
            end = parent.count('\n')+1
            middle = int(end / 2)
            genes['top'].append(parent.splitlines()[0:middle])
            genes['bottom'].append(parent.splitlines()[middle:end])
    for r in range(0, len(genes["top"])):
        for j in range(0, len(genes["bottom"])):
            if r != j:
                children.append('\n'.join(genes["top"][r] + genes["bottom"][j]))
    return children



def ChangeAssignmentOperation(codeArray):
    for i in range(0, len(codeArray)):
        assignmentCheck = codeArray[i].split(" ")
        if len(assignmentCheck) > 1:
            if assignmentCheck[1] == "=" or assignmentCheck[1] == "+=" or assignmentCheck[1] == "-=" or assignmentCheck[1] == "/=" or assignmentCheck[1] == "*=":
                decider = random.randint(0, 11)
                if decider == 0:
                    codeArray[i] = codeArray[i].replace("+", "*")
                if decider == 1:
                    codeArray[i] = codeArray[i].replace("+", "/")
                if decider == 2:
                    codeArray[i] = codeArray[i].replace("+", "-")
                if decider == 3:
                    codeArray[i] = codeArray[i].replace("-", "*")
                if decider == 4:
                    codeArray[i] = codeArray[i].replace("-", "/")
                if decider == 5:
                    codeArray[i] = codeArray[i].replace("-", "+")
                if decider == 6:
                    codeArray[i] = codeArray[i].replace("/", "*")
                if decider == 7:
                    codeArray[i] = codeArray[i].replace("/", "+")
                if decider == 8:
                    codeArray[i] = codeArray[i].replace("/", "-")
                if decider == 9:
                    codeArray[i] = codeArray[i].replace("*", "+")
                if decider == 10:
                    codeArray[i] = codeArray[i].replace("*", "/")
                if decider == 11:
                    codeArray[i] = codeArray[i].replace("*", "-")

    return codeArray


def change_order(codeArray):
    swapOne = random.randint(0, len(codeArray) - 1)
    swapTwo = random.randint(0, len(codeArray) - 1)
    temp = codeArray[swapOne]
    codeArray[swapOne] = codeArray[swapTwo]
    codeArray[swapTwo] = temp
    return codeArray


# noinspection PyUnresolvedReferences
def fitness(code, anwser):
    score = 0
    arrayTest = []
    try:
        arrayTest = makeArray()
        for i in range(0, len(arrayTest)):
            if arrayTest[i] == answer[i]:
                score += 1
    except:
        print("Unexpected error:")
        score = -1
    return score



code = """def makeArray():
\tarray = []
\tx = 0 + 1
\ty = x1 + 1
\tarray.append(x)
\tz = 2 - 2
\tx.append(x)
\tx = 4 * 2
\tarray.append(x)
\treturn array"""

answer = [0, 4, 2]

codes = []

random.seed()

codes.append(code)
codes.append(code)
codes.append(code)

offspring_per_pop = 6
steps = 10
highest_score = 0
while highest_score != 3:
    highest_score = 0
    ranks = {}
    for i in range(0, len(codes)):
        score = 0
        codes[i] = mutate(codes[i])
        try:
            exec(codes[i])
            score = fitness(codes[i], answer)
            print("Compiles")
        except:
            print("Doesn't compile")
        ranks[i] = score
        if score >= highest_score:
            highest_score = score
        if score == 3:
            break
    top_3 = sorted(ranks.keys(), key=ranks.get, reverse=True)[:3]

    #Need to decide which ones get sent into crossover
    codes = Crossover(list(itemgetter(*top_3)(codes)))
for x in codes:
    print(x)
