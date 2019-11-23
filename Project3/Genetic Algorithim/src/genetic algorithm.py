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
    swapOne = random.randint(0, len(codeArray) - 1)
    swapTwo = random.randint(0, len(codeArray) - 1)
    temp = codeArray[swapOne]
    codeArray[swapOne] = codeArray[swapTwo]
    codeArray[swapTwo] = temp

    return '\n'.join(str(e) for e in codeArray)


# noinspection PyUnresolvedReferences
def fitness(code):
    score = 0
    arrayTest = []
    answer = []
    try:
        arrayTest = makeArray()
        answer.append(0)
        answer.append(1)
        answer.append(2)
        answer.append(3)
        answer.append(4)
        answer.append(5)
        answer.append(6)
        answer.append(7)
        answer.append(8)
        answer.append(9)
    except:
        print("Unexpected error:")
        score = -1
    for i in range(0, len(arrayTest) - 1):
        if arrayTest[i] == answer[i]:
            score += 1
    return score


code = """def makeArray():
    array = []
    array.append(0)
    array.append(1)
    array.append(2)
    array.append(3)
    array.append(4)
    array.append(5)
    array.append(6)
    array.append(7)
    array.append(8)
    array.append(9)
    return array"""

codes = []

random.seed()

codes.append(code)
codes.append(code)
codes.append(code)

offs_per_pop = 6
steps = 10
score = 0

while score != 10:
    for i in range(0, len(codes)):
        codes[i] = mutate(codes[i])
        try:
            exec(codes[i])
        except:
            print("Doesn't compile")
        score = fitness(codes[i])
        print(score)


        if score == 10:
            break
for x in codes:
    print(x)