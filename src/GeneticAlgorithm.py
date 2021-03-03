"""
Simulates and attempts to solve the prisoner's dilemma using a genetic algorithm.
    Copyright (C) 2021  Kevin Tyrrell

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from random import seed, randrange, getrandbits, random, shuffle
from sys import maxsize

# How many prisoners in the simulation.
PRISONER_POP = 1000
# How often mutations occur while copying each gene-bit.
MUTATION_RATE = 0.15
# Amount of times two prisoners are subjugated to the dilemma per generation.
TESTS_PER_GENERATION = 3
# Number of generations to be performed.
MAX_GENERATIONS = 100
# Seed for this particular simulation.
SEED = 155966

# Name of the program.
PROGRAM_NAME = "GeneticAlgorithm"


_print = print
def print(x):
    _print("{}: {}".format(PROGRAM_NAME, str(x)))
    
"""
Source: https://stackoverflow.com/a/10322018/4718288
@param n Integer to be parsed as a bitfield. Cannot be negative.
@return Bitfield of the passed integer, not including the sign bit.
"""
def bitfield(n):
    return [1 if digit=='1' else 0 for digit in bin(n)[2:]] # [2:] to chop off the "0b" part

"""
Performs the cost function on the group of prisoners.
Two prisoners are pulled aside and are tested whether they wish to defect.
@param prisoners List of prisoners, size of PRISONER_POP.
@param costs List of costs corresponding to the prisoner.
@param i Index of the first prisoner.
@param j Index of the second prisoner.
"""
def cost(prisoners, costs, i, j):
    if not isinstance(prisoners, list) or not isinstance(costs, list):
        raise TypeError("Prisoner and Cost parameters must be lists")
    if len(prisoners) != PRISONER_POP or len(costs) != PRISONER_POP:
        raise ValueError("Prisoner and Cost lists must be of length PRISONER_POP")
    if not isinstance(i, int) or not isinstance(j, int):
        raise TypeError("Prisoner and Cost indexes must be integers")
    if i < 0 or j < 0 or i >= PRISONER_POP or j >= PRISONER_POP or j == i:
        raise ValueError("Indexes {} and {} must be unique and within bounds [0, PRISONER_POP)".format(str(i), str(j)))
    pi, pj = prisoners[i], prisoners[j]
    pi_defect, pj_defect = pi.defect(), pj.defect()
    if pi_defect and pj_defect:
        costs[i], costs[j] = 2 + costs[i], 2 + costs[j]
    elif pi_defect:
        costs[i] = 3 + costs[i]
    elif pj_defect:
        costs[j] = 3 + costs[j]
    else:
        costs[i], costs[j] = 1 + costs[i], 1 + costs[j]

"""
Calculates a rolling average, averaging values as it is called.
The first call to 'rolling_average' sets up the rolling average closure.
@return Inner function

Inner function
Calls without parameters will just return the average.
@param [next] Next value to be averaged into the rolling average.
@return Current rolling average, after averaging the specified value.
"""
def rolling_average():
    count = 0
    avg = None
    def roll(next = None):
        nonlocal count
        nonlocal avg
        if next != None:
            avg = next if count <= 0 else avg + (next - avg) / (count + 1.0)
            count += 1
        return avg
    return roll

def main():
    print("Starting up.")
    if MUTATION_RATE < 0 or MUTATION_RATE > 1:
        raise ValueError("Mutation rate of {} is not within acceptable bounds of [0.0, 1.0]".format(str(MUTATION_RATE)))
    if PRISONER_POP <= 0 or PRISONER_POP % 4 != 0:
        raise ValueError("Initial population of {} must a positive number and a multiple of four".format(str(PRISONER_POP)))
    seed(SEED)
    
    # Indicates the status of the current population.
    def assess_pop(pop_list):
        roll_avg_align = rolling_average()
        roll_avg_age = rolling_average()
        
        for i in range(PRISONER_POP):
            p = pop_list[i]
            roll_avg_align(p.get_alignment())
            roll_avg_age(p.get_age())
        print("Average defection rate: {}%".format(str(roll_avg_align() / ALIGNMENT_MAX)))
        print("Average prisoner age  : {}".format(str(roll_avg_age())))
    
    # Cost for each prisoner's decisions.
    costs = [0] * PRISONER_POP
    population = [None] * PRISONER_POP
    for i in range(PRISONER_POP):
        population[i] = Prisoner()
    
    for i in range(MAX_GENERATIONS):
        print("--- Generation: {} ---".format(str(i)))
        assess_pop(population)
        
        for j in range(PRISONER_POP):
            costs[j] = 0
        for j in range(TESTS_PER_GENERATION):
            # Shuffle both lists to 'smooth out' results.
            temp_seed = randrange(maxsize)
            seed(temp_seed)
            shuffle(population)
            if j > 0: # No need to shuffle costs if it's the first test.
                seed(temp_seed)
                shuffle(costs)
            for k in range(0, PRISONER_POP, 2):
                cost(population, costs, k, k + 1)
    
        # Sort prisoner population by weight.
        order = {v:i for i,v in enumerate(population)}
        population.sort(key=lambda x: costs[order[x]])
    
        # Destroy half of the population -- Repopulate them randomly.
        cutoff_i = PRISONER_POP // 2
        for j in range(0, cutoff_i, 2):
            # Father is j, choose mother randomly among the population.
            mother_i = randrange(j + 1, cutoff_i)
            mother = population[mother_i]
            children = mother.crossover(population[j])
            # Replace two of the underperforming prisoners with two children.
            population[cutoff_i + j] = children[0]
            population[cutoff_i + j + 1] = children[1]
            # Swap the mother with whatever is to the right of the father.
            population[mother_i] = population[j + 1]
            population[j + 1] = mother
    
    print("Terminating.")
main()
