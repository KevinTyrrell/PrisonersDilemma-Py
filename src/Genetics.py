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

from typing import Callable
from random import random, getrandbits
from Prisoner import Prisoner
from Genome import Genome


class Genetics:
    def __init__(self, mutation_rate: float):
        if mutation_rate < 0.0 or mutation_rate > 1.0:
            raise ValueError("Mutation rate of {} must be of the domain [0.0, 1.0]".format(mutation_rate))
        self.__mutation_rate = mutation_rate

    """
    Callback function for a uniform mutation.
    Frequency of mutation is dictated by the mutation rate.
    """
    def __uniform_mutation(self):
        return random() < self.__mutation_rate

    """
    Callback function for a uniform crossover.
    Approximately half of the bits will be exchanged between parents.
    """
    @staticmethod
    def __uniform_crossover():
        return getrandbits(1) == 0

    def conceive(self, mother: Genome, father: Genome, prisoner_cb: Callable[[Prisoner], None]) -> None:
        # Construct duplicates of the mother and father.
        mother = Genome(mother.genes)
        father = Genome(father.genes)

        # Perform a uniform crossover.
        mother.crossover(father, Genetics.__uniform_crossover)

        # Mutate both sets of genes.
        mother.mutate(self.__uniform_mutation)
        father.mutate(self.__uniform_mutation)

        # Pass the two children to the callback.
        prisoner_cb(Prisoner(mother))
        prisoner_cb(Prisoner(father))
