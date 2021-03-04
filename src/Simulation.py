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

import random
from typing import List
from Prisoner import Prisoner


class Simulation:
    @staticmethod
    def run(population: int, generations: int, mutation_rate: float, tests: int, seed: int) -> None:
        random.seed(seed)

    __COOPERATION_COST, __DEFECTION_COST, __BETRAYAL_COST = 1, 2, 3

    """
    Performs a prisoner's dilemma test of two prisoners.
    
    The prisoner's dilemma is a game-theory situation with four outcomes:
    * Both prisoners defect: mutual bad outcome.
    * Prisoner A defects: bad outcome for Prisoner B.
    * Prisoner B defects: bad outcome for Prisoner A.
    * Both prisoners cooperate: mutual good outcome.
    
    @:param prisoners: List of all prisoners in the population.
    @:param costs: List of the cost (fitness) of each prisoner.
    @:param p1: Index of the prisoner in the list.
    @:param p2: Index of the prisoner in the list.
    """
    @staticmethod
    def __cost(prisoners: List[Prisoner], costs: List[int], p1: int, p2: int) -> None:
        p1_defect = prisoners[p1].defect()
        p2_defect = prisoners[p2].defect()
        if p1_defect and p2_defect:
            costs[p1] += Simulation.__DEFECTION_COST
            costs[p2] += Simulation.__DEFECTION_COST
        elif p2_defect:
            costs[p1] += Simulation.__BETRAYAL_COST
        elif p1_defect:
            costs[p2] += Simulation.__BETRAYAL_COST
        else:
            costs[p1] += Simulation.__COOPERATION_COST
            costs[p2] += Simulation.__COOPERATION_COST


#     if MUTATION_RATE < 0 or MUTATION_RATE > 1:
#         raise ValueError("Mutation rate of {} is not within acceptable bounds of [0.0, 1.0]".format(str(MUTATION_RATE)))
#     if PRISONER_POP <= 0 or PRISONER_POP % 4 != 0:
#         raise ValueError("Initial population of {} must a positive number and a multiple of four".format(str(PRISONER_POP)))
#     seed(SEED)
#
#     # Indicates the status of the current population.
#     def assess_pop(pop_list):
#         roll_avg_align = rolling_average()
#         roll_avg_age = rolling_average()
#
#         for i in range(PRISONER_POP):
#             p = pop_list[i]
#             roll_avg_align(p.get_alignment())
#             roll_avg_age(p.get_age())
#         print("Average defection rate: {}%".format(str(roll_avg_align() / ALIGNMENT_MAX)))
#         print("Average prisoner age  : {}".format(str(roll_avg_age())))
#
#     # Cost for each prisoner's decisions.
#     costs = [0] * PRISONER_POP
#     population = [None] * PRISONER_POP
#     for i in range(PRISONER_POP):
#         population[i] = Prisoner()
#
#     for i in range(MAX_GENERATIONS):
#         print("--- Generation: {} ---".format(str(i)))
#         assess_pop(population)
#
#         for j in range(PRISONER_POP):
#             costs[j] = 0
#         for j in range(TESTS_PER_GENERATION):
#             # Shuffle both lists to 'smooth out' results.
#             temp_seed = randrange(maxsize)
#             seed(temp_seed)
#             shuffle(population)
#             if j > 0: # No need to shuffle costs if it's the first test.
#                 seed(temp_seed)
#                 shuffle(costs)
#             for k in range(0, PRISONER_POP, 2):
#                 cost(population, costs, k, k + 1)
#
#         # Sort prisoner population by weight.
#         order = {v:i for i,v in enumerate(population)}
#         population.sort(key=lambda x: costs[order[x]])
#
#         # Destroy half of the population -- Repopulate them randomly.
#         cutoff_i = PRISONER_POP // 2
#         for j in range(0, cutoff_i, 2):
#             # Father is j, choose mother randomly among the population.
#             mother_i = randrange(j + 1, cutoff_i)
#             mother = population[mother_i]
#             children = mother.crossover(population[j])
#             # Replace two of the underperforming prisoners with two children.
#             population[cutoff_i + j] = children[0]
#             population[cutoff_i + j + 1] = children[1]
#             # Swap the mother with whatever is to the right of the father.
#             population[mother_i] = population[j + 1]
#             population[j + 1] = mother
