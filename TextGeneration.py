from random import randrange
import random
import time
import numpy as np
from numpy.random import choice

PUP_SIZE = 1200
MAX_FITNESS = 298
crossOver_rate = 0.25
mutation_rate = 0.005
priority = np.zeros(shape=(PUP_SIZE))
sum = 0

for i in range(PUP_SIZE):
    sum = sum + i + 1

for i in range(PUP_SIZE):
    priority[i] = (i + 1) / sum


def initialPopulation():
    pop = np.zeros(shape=(PUP_SIZE, MAX_FITNESS))
    size = PUP_SIZE
    for i in range(size):
        for j in range(MAX_FITNESS):
            pop[i][j] = randrange(28)
    return pop

def fitnessFunction(ans, chrom):
    return np.count_nonzero(ans == chrom)


def createNextGen(currGen, grades):
    order = grades.argsort()
    currGen = currGen[order]
    grades = grades[order]
    nextGen = np.zeros(shape=(PUP_SIZE, MAX_FITNESS))
    parents = random.choices(population=currGen, weights=priority, k=len(grades))
    for k in range((int)(len(grades) / 2)):
        #        parents = np.random.choices(a = currGen, size = 2, p=priority)

        child1, child2 = crossOver(parents[2 * k], parents[2 * k + 1])
        nextGen[2 * k] = child1
        nextGen[2 * k + 1] = child2

    return nextGen


def crossOver(p1, p2):
    if (np.random.random() < crossOver_rate):
        return p1, p2
    c1 = np.zeros(shape=(MAX_FITNESS))
    c2 = np.zeros(shape=(MAX_FITNESS))
    randArr = np.random.random(size=MAX_FITNESS)

    for j in range(MAX_FITNESS):
        if (randArr[j] < 0.5):
            c1[j] = p1[j]
            c2[j] = p2[j]
        else:
            c1[j] = p2[j]
            c2[j] = p1[j]

    # decide wether to make mutation or not
    c1, c2 = mutation(c1, c2)
    return c1, c2


# mutation for a single char in solution
def mutation(c1, c2):
    randArr = np.random.random(size=MAX_FITNESS * 2)
    mutArr = np.random.random_integers(low=0, high=27, size=MAX_FITNESS * 2)
    for i in range(MAX_FITNESS):
        if (randArr[i * 2] < mutation_rate):
            c1[i] = mutArr[i * 2]
        if (randArr[i * 2 + 1] < mutation_rate):
            c2[i] = mutArr[i * 2 + 1]
    return c1, c2


def main():
    start_time = time.time()
    # create correct ans
    correctAns = np.array(
        [19, 14, 27, 1, 4, 27, 14, 17, 27, 13, 14, 19, 27, 19, 14, 27, 1, 4, 27, 19, 7, 0, 19, 27, 8, 18, 27, 19, 7, 4,
         27, 16, 20, 4, 18, 19, 8, 14, 13, 26, 27, 22, 7, 4, 19, 7, 4, 17, 27, 19, 8, 18, 27, 13, 14, 1, 11, 4, 17, 27,
         8, 13, 27, 19, 7, 4, 27, 12, 8, 13, 3, 27, 19, 14, 27, 18, 20, 5, 5, 4, 17, 26, 27, 19, 7, 4, 27, 18, 11, 8,
         13, 6, 18, 27, 0, 13, 3, 27, 0, 17, 17, 14, 22, 18, 27, 14, 5, 27, 14, 20, 19, 17, 0, 6, 4, 14, 20, 18, 27, 5,
         14, 17, 19, 20, 13, 4, 26, 27, 14, 17, 27, 19, 14, 27, 19, 0, 10, 4, 27, 0, 17, 12, 18, 27, 0, 6, 0, 8, 13, 18,
         19, 27, 0, 27, 18, 4, 0, 27, 14, 5, 27, 19, 17, 14, 20, 1, 11, 4, 18, 27, 0, 13, 3, 27, 1, 24, 27, 14, 15, 15,
         14, 18, 8, 13, 6, 27, 4, 13, 3, 27, 19, 7, 4, 12, 26, 27, 19, 14, 27, 3, 8, 4, 27, 19, 14, 27, 18, 11, 4, 4,
         15, 26, 27, 13, 14, 27, 12, 14, 17, 4, 26, 27, 0, 13, 3, 27, 1, 24, 27, 0, 27, 18, 11, 4, 4, 15, 27, 19, 14,
         27, 18, 0, 24, 27, 22, 4, 27, 4, 13, 3, 26, 27, 19, 7, 4, 27, 7, 4, 0, 17, 19, 0, 2, 7, 4, 27, 0, 13, 3, 27,
         19, 7, 4, 27, 19, 7, 14, 20, 18, 0, 13, 3, 27, 13, 0, 19, 20, 17, 0, 11, 27, 18, 7, 14, 2, 10, 18, 26])

    # first set of grades
    grades = np.array(np.zeros(shape=(PUP_SIZE)))
    currGen = initialPopulation()
    for i in range(len(currGen)):
        grades[i] = fitnessFunction(correctAns, currGen[i])
    gen = 1

    perfect_score = MAX_FITNESS
    bStop = False
    while not bStop:  # perfect_score not in grades:
        currGen = createNextGen(currGen, grades)
        for i in range(len(currGen)):
            grades[i] = fitnessFunction(correctAns, currGen[i])
            if grades[i] == MAX_FITNESS:
                bStop = True
        gen = gen + 1

    # print solution
    print("Solution found after " + str(gen) + " generations.")
    print("Running time: %s " % (time.time() - start_time) + "seconds.")


if __name__ == "__main__":
    main()
