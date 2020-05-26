from random import randrange
import random
import time


def initialPopulation():
    pop = []
    size = 200
    for i in range(size):
        chrome = []

        for i in range(8):
            chrome.append(randrange(8))

        pop.append(chrome)

    return pop


def fitnessFunction(list):
    grade = 49
    slant = 0
    for i in range(0, 8):
        for j in range(i + 1, 8):
            slant = j - i
            if list[i] == list[j]:
                grade = grade - 2
            else:
                if list[i] + slant == list[j] or list[i] - slant == list[j]:
                    grade = grade - 2
    return grade


def mutation(list, i):
    list[i] = random.randint(0, 7)
    return list


def crossOver(list1, list2):
    #determine wether to do crossover
    crossOver_rate = 2
    randNum = random.randint(0, 9)
    if (randNum < crossOver_rate):
        return list1, list2

    childrenList1 = []
    childrenList2 = []
    for j in range(0, 8):
        i = random.randint(0, 1)
        if (i == 1):
            childrenList1.append(list1[j])
            childrenList2.append(list2[j])
        else:
            childrenList1.append(list2[j])
            childrenList2.append(list1[j])

    # determine wether to do mutation
    mutation_rate = 1
    for i in range(0, 8):
        randNum = random.randint(0, 99)
        if (randNum < mutation_rate):
            childrenList1 = mutation(childrenList1, i)
        randNum = random.randint(0, 99)
        if (randNum < mutation_rate):
            childrenList2 = mutation(childrenList2, i)
    return childrenList1, childrenList2


def createNextGen(currGen, grades):
    nextGen = []

    grades, currGen = zip(*sorted(zip(grades, currGen)))
    pool = []
    nextGen.append(currGen[len(currGen) - 1])
    nextGen.append(currGen[len(currGen) - 2])
    help = 1
    for i in range(len(grades)):
        count = help
        while count > 0:
            pool.append(currGen[i])
            count = count - 1
        help = help + 1

    # do 100 times: select 2, crossover, mutation, add to new gen
    poll = []
    for i in range(len(grades)):
        count = grades[i]
        while count > 0:
            poll.append(currGen[i])
            count = count - 1

    for k in range(98):
        #choose parents
        choose = randrange(len(poll))
        parent1 = poll[choose]
        choose = randrange(len(poll))
        parent2 = poll[choose]

        #create children
        child1, child2 = crossOver(parent1, parent2)
        nextGen.append(child1)
        nextGen.append(child2)

    return nextGen


def main():
    start_time = time.time()
    grades = []
    currGen = initialPopulation()
    #first grades
    for l in currGen:
        grades.append(fitnessFunction(l))
    gen = 0

    perfect_score = 49
    f = open("q.txt", "w")

    while perfect_score not in grades:
        #create next gen
        currGen = createNextGen(currGen, grades)
        # if havnt solved yet, initiate population again
        if gen % 400 == 0:
            currGen = initialPopulation()
        grades = []
        ## grade gen
        for l in currGen:
            grades.append(fitnessFunction(l))
        gen = gen + 1
        f.write(str(max(grades)))
        f.write(", ")
        f.write(str(sum(grades) / len(grades)))
        f.write("\n")



    index = grades.index(perfect_score)

    print("Solution using GA found after " + str(gen) + " generations.")
    print("Running time: %s " % (time.time() - start_time) + "seconds.")
    print("The solution is: " + str(currGen[index]))

    #print solution
    for i in range(8):
        for j in range(8):
            if currGen[index][i] == j:
                print("Q", end = " ")
            else:
                print("-", end = " ")
        print("")


if __name__ == "__main__":
    main()
