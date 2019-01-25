import numpy
import fitnessGA
import math
import random
import time
import pandas as pd
import sqlite3
import multiprocessing
import pprint
import itertools

dbName = "bitfinex"
dcmTS = 1
priceIndex = 1
if dbName == "kraken":
    dcmTS = 10000
    priceIndex = 2
elif dbName == "bitfinex":
    dcmTS = 1000
    priceIndex = 2
# print("historySize, candleSize, ATRFilterHigh, ATRFilterLow, profitTarget, lossTarget,loosingTrades,profitableTrades,totalTrades,finalEquity,profit")

conn = sqlite3.connect(dbName + ".db")
cur = conn.cursor()
cur.execute("SELECT * FROM quotes_BTC_LTC WHERE ts >=? AND ts<=?", (1483228800 * dcmTS, 1545472800 * dcmTS))
results = cur.fetchall()

tStart = (round(results[0][0] / dcmTS))
tEnd = (round(results[len(results) - 1][0] / dcmTS))
start = tStart - (tStart % 3600) - 3 * 3600
end = tEnd - (tEnd % 3600) + 3 * 3600
# print("start", tStart)
# print("end", tEnd)
index = 0
price = 0
candleSize = 60
historySize = 24
roundDec = 5
makerFee = 0.00 / 100
takerFee = 0.03 / 100
candleList = []

for i in range(start, end, 120 * candleSize):
    tup = ((i - 60 * candleSize), i)
    candleList.append(tup)
    index += 1

# Number of the weights we are looking to optimize.
num_weights = 4

"""
Genetic algorithm parameters:
    Mating pool size
    Population size
"""

# ABC
# A -> B
# A -> C
# B -> C

# ABCD
# A -> B
# A -> C
# A -> D
# B -> C
# B -> D
# C -> D

# ABCDF
# A -> B
# A -> C
# A -> D
# A -> F
# B -> C
# B -> D
# B -> F
# C -> D
# C -> F
# D -> F


# sol_per_pop = 2
num_parents_mating = 4
sol_per_pop = num_parents_mating + int(
    math.factorial(num_parents_mating) / (math.factorial(2) * math.factorial(num_parents_mating - 2)))
# Defining the population size.
pop_size = (num_weights, sol_per_pop)
# The population will have sol_per_pop chromosome where each chromosome has num_weights genes.
# Creating the initial population.
# new_population = [[0] * pop_size[0]] * pop_size[1]

# for num1 in range(0, pop_size[0]):
#     for num2 in range(0, pop_size[1]):
#         new_population[num1][num2] = (random.randrange(0, 100, 10))  # uniform(low=-4.0, high=4.0, size=pop_size)

new_pop = []
for i in range(0, sol_per_pop):
    profitTarget = int(numpy.random.randint(1, 10, 1))  # [0.0005, 0.0005, 0.0005]  #
    lossTarget = int(numpy.random.randint(1, 10, 1))  # range(5, 25, 5)
    ATRLow = int(numpy.random.randint(1, 9, 1))
    ATRHight = int(numpy.random.randint(ATRLow, 10, 1))  # range(5, 11, 1)
    candleSize = 60
    new_pop.append([-99, profitTarget / 10000, lossTarget / 10000, ATRHight / 10000, ATRLow / 10000, candleSize])

# new_pop = [[random.randrange(1, 10, 1)
#             for i in range(pop_size[0])]
#            for j in range(pop_size[1])]

# print(new_pop)
#
num_generations = 10
#
print("new_pop", new_pop)
for generation in range(num_generations):

    print("Generation : ", generation)
    startTimer = time.time()

    fitness = fitnessGA.cal_pop_fitness(new_pop, candleList, results)
    print("fitness:", fitness)

    fitness.sort(key=lambda x: x[0])
    parents = fitness[-num_parents_mating:index]
    print("parents:", parents)

    new_pop = fitnessGA.crossover(parents)
    print("new_pop:", new_pop)

    endTimer = time.time()
    print("Time to complete: ", (endTimer - startTimer))

# Measing the fitness of each chromosome in the population.

# parents = [[0.020615053504643654, 0.0006, 0.0004, 0.0005, 0.0001, 60],
#            [0.03861745902968572, 0.0008, 0.0002, 0.0009, 0.0003, 60],
#            [0.0990719451151083, 0.0008, 0.0002, 0.0009, 0.0002, 60],
#            [0.12045820992643641, 0.0005, 0.0001, 0.0009, 0.0002, 60]]

# ABCD
# A -> B
# A -> C
# A -> D
# B -> C
# B -> D
# C -> D

# offspring_size=(pop_size[0] - parents.shape[0], num_weights))
# parents =[[0.020615053504643654, 0.0006, 0.0004, 0.0005, 0.0001, 60], [0.03861745902968572, 0.0008, 0.0002, 0.0009, 0.0003, 60], [0.0990719451151083, 0.0008, 0.0002, 0.0009, 0.0002, 60], [0.12045820992643641, 0.0005, 0.0001, 0.0009, 0.0002, 60]]
#
# offspring_crossover = fitnessGA.crossover(parents)
#                                           offspring_size=(pop_size[0] - parents.shape[0], num_weights))
#
# # Adding some variations to the offsrping using mutation.
# offspring_mutation = fitnessGA.mutation(offspring_crossover)
#
# # # Creating the new population based on the parents and offspring.
# # for i in range(0, len(offspring_mutation+parents[i])):
# #     if (i < len(parents)):
# #         new_pop[i] = [i] + parents[i]
# #     else:
# #         new_pop[i] = [i] + offspring_mutation[i]
#
# # for i in range(0, len(new_pop)):
# #     new_pop.pop(0)
# print("parents", parents)
# print("offspring_crossover", offspring_crossover)
# print("offspring_mutation", offspring_mutation)
# new_pop[0:parents.shape[0], :] = parents
# new_pop[parents.shape[0]:, :] = offspring_mutation

# for i in range(0, len(new_pop)):
#     new_pop[i].insert(0, i)

# The best result in the current iteration.
# print("Best result : ", numpy.max(numpy.sum(new_population * equation_inputs, axis=1)))

# Getting the best solution after iterating finishing all generations.
# At first, the fitness is calculated for each solution in the final generation.
# fitness = fitnessGA.cal_pop_fitness(new_pop, candleList, results)
# # Then return the index of that solution corresponding to the best fitness.
# best_match_idx = numpy.where(fitness == numpy.max(fitness))
#
# print("Best solution : ", new_pop[best_match_idx, :])
# print("Best solution fitness : ", fitness[best_match_idx])
