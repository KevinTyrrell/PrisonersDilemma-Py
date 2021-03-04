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
from Genome import Genome
from Genetics import Genetics


class Simulation:
    @staticmethod
    def run(population: int, generations: int, mutation_rate: float, tests: int, seed: int) -> None:
        random.seed(seed)

        # Population of prisoners -- modified each generation.
        prisoners = [Prisoner(Genome()) for _ in range(population)]
        # Controls mutation, crossover, and repopulation.
        genetics = Genetics(mutation_rate)

        for generation in range(0, generations):
            costs = [0] * population  # Initialize costs to zero each generation.
            random.shuffle(prisoners)  # De-segregate parents and children.

            # Group up each prisoner with a random unique partner.
            for i in range(0, population, 2):
                # Perform the prisoner's dilemma test with the two subjects N times.
                for k in range(0, tests):
                    Simulation.__cost(prisoners, costs, i, i + 1)

            # Sort the prisoners by cost, in ascending order.
            order = {v: i for i, v in enumerate(prisoners)}
            prisoners.sort(key=lambda x: costs[order[x]])

            i = 0
            cutoff_limit = population // 2

            # Called when a new child is born and added to the population.
            def born_child_cb(child: Prisoner) -> None:
                nonlocal i
                # Replace an under-performing prisoner with a new child.
                prisoners[cutoff_limit + i] = child
                i += 1

            while i in range(0, population):  # Loop incremented via callback.
                j = random.randrange(i + 1, cutoff_limit)
                mother, father = prisoners[i], prisoners[j]
                # Switch the father with the mother's right neighbor.
                prisoners[j] = prisoners[i + 1]
                prisoners[i + 1] = father
                genetics.conceive(mother.genome, father.genome, born_child_cb)

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
