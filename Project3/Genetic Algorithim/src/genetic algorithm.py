import random
import re
from operator import itemgetter


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
    if random.randint(1, 3) == 1:
        mutation = random.randint(1, 3)
        if mutation == 1:
            codeArray = change_order(codeArray)
        if mutation == 2:
            codeArray = swap_variables(codeArray)
        if mutation == 3:
            codeArray = ChangeAssignmentOperation(codeArray)
    return '\n'.join(str(e) for e in codeArray)


def Crossover(parents):
    genes = {"top": [], "bottom": []}
    children = []
    for parent in parents:
        end = parent.count('\n') + 1
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
            if assignmentCheck[1] == "=" or assignmentCheck[1] == "+=" or assignmentCheck[1] == "-=" or assignmentCheck[
                1] == "/=" or assignmentCheck[1] == "*=":
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
        #NEED TO CHANGE THIS WHEN TESTING OTHER FUNCTIONS
        arrayTest = makeArray()
        for i in range(0, len(arrayTest)):
            if arrayTest[i] == answer[i]:
                score += 1
            if answer[1] in arrayTest:
                score += 1
    except:
        print("Unexpected error:")
        score = -1
    return score

def results(iteration, gen_high, max_score, highest_score, highest_score_gen, gen_size, pass_count, fail_count, codes = []):
    if(len(codes) > 0):
        print("\n\nFinal Generation Code: ")
        for x in codes:
            print(x, end="\n\n")
        print("\n\nFinal Results: ")

    print("\nIteration: {0}  \
              \n\tHighest Score in Current Gen: {1} / {2} \
              \n\tHighest Total Score: {3} (Gen {4}) \
              \n\tGen Info (Size, Pass, Fail): {5}, {6}, {7}"
          .format(iteration, gen_high, max_score, highest_score, highest_score_gen, gen_size, pass_count, fail_count))


# def Sequential_Search(dlist, item):
#     pos = 0
#     found = False
#     while pos < len(dlist) and not found:
#         if dlist[pos] == item:
#             found = True
#         else:
#             pos = pos + 1
#     return found, pos
#
# Sequential_Search([11, 23, 58, 31, 56, 77, 43, 12, 65, 19], 31))
# Correct Output: (True, 3)
#
# FINAL RESULT
#     Iteration: 1000
#         Highest Score in Current Gen: 6 / 6
#         Highest Total Score: 6 (Gen 20)
#         Gen Info (Size, Pass, Fail): 6, 6, 0

# def bubbleSort():
# \tarr = [64, 34, 25, 12, 22, 11, 90]
# \tn = len(arr)
# \tfor i in range(n):
# \t\tfor j in range(0, n - i - 1):
# \t\t\tif arr[j] > arr[j + 1]:
# \t\t\t\tarr[j], arr[j + 1] = arr[j + 1], arr[j]
# \treturn arr
#
# bubbleSort([64, 34, 25, 12, 22, 11, 90])
# Correct Output: [11, 12, 22, 25, 34, 64, 90]
#
# FINAL RESULT
#     Iteration: 1000
#         Highest Score in Current Gen: 6 / 6
#         Highest Total Score: 6 (Gen 13)
#         Gen Info (Size, Pass, Fail): 6, 6, 0


code = """def makeArray():
\tarray = []
\tx = 0 + 1
\tarray.append(x)
\tx = 2 - 2
\tarray.append(x)
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
max_score = len(answer) * 2
max_iterations = 1000
highest_score = [0, 1]
iteration = 0
while True:
    iteration += 1
    gen_high = 0
    ranks = {}
    fail_count = 0
    gen_size = len(codes)
    for i in range(0, gen_size):
        score = 0
        codes[i] = mutate(codes[i])
        try:
            exec(codes[i])
            score = fitness(codes[i], answer)
        except Exception as e:
            fail_count += 1
            score = -1
        ranks[i] = score
        if score >= gen_high:
            gen_high = score
    top_3 = sorted(ranks.keys(), key=ranks.get, reverse=True)[:3]
    pass_count = gen_size - fail_count

    if gen_high > highest_score[0]:
        highest_score[0], highest_score[1] = gen_high, iteration
    if highest_score == max_score or max_iterations <= iteration:
        results(iteration, gen_high, max_score, highest_score[0], highest_score[1], gen_size, pass_count, fail_count, codes)
        break
    else:
        results(iteration, gen_high, max_score, highest_score[0], highest_score[1], gen_size, pass_count, fail_count)
    codes = Crossover(list(itemgetter(*top_3)(codes)))

