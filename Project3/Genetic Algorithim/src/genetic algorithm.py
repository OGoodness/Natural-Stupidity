import random


# def makeArray():
#   array = []
#    array.append(0)
#    array.append(1)
#    array.append(2)
#    array.append(3)
#    array.append(4)
#    array.append(5)
#    array.append(6)
#    array.append(7)
#    array.append(8)
#    array.append(9)
#    return array


def mutate(code):
    codeArray = code.splitlines()
    codeArray = change_order(codeArray)
    codeArray = ChangeAssignmentOperation(codeArray)

    return '\n'.join(str(e) for e in codeArray)


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

    except:
        print("Unexpected error:")
        score = -1
    for i in range(0, len(arrayTest)):
        if arrayTest[i] == answer[i]:
            score += 1
    return score


# code = """def makeArray():
#     array = []
#     array.append(0)
#     array.append(1)
#     array.append(2)
#     array.append(3)
#     array.append(4)
#     array.append(5)
#     array.append(6)
#     array.append(7)
#     array.append(8)
#     array.append(9)
#     return array"""

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

offs_per_pop = 6
steps = 10
score = 0

while score != 3:
    for i in range(0, len(codes)):
        codes[i] = mutate(codes[i])
        try:
            exec(codes[i])
        except:
            print("Doesn't compile")
        score = fitness(codes[i], answer)
        print(score)

#This is just a test break
        if score == 3:
            break
for x in codes:
    print(x)
