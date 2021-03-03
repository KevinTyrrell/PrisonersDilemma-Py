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


from __future__ import annotations
from random import randrange
from typing import Tuple


class Prisoner:
    # 2 raised to the power of the maximum number of bits in Prisoner's alignments.
    __ALIGNMENT_LIMIT = 2 ** 32

    """
    Constructs a prisoner instance.
    If no alignment is specified, the prisoner is assigned a random alignment.

    @param [alignment] Likelihood to defect, ranging from [0, ALIGNMENT_MAX).
    @field __alignment Likelihood to defect, ranging from [0, ALIGNMENT_MAX).
    @field __age Number of generations of offspring of the prisoner.
    """
    def __init__(self, alignment: int = None):
        if alignment is None:
            self.__alignment = randrange(Prisoner.__ALIGNMENT_LIMIT)
        elif isinstance(alignment, int):
            if alignment >= Prisoner.__ALIGNMENT_LIMIT or alignment < 0:
                raise ValueError("Alignment of {} was out of bounds [0, ALIGNMENT_MAX)".format(str(alignment)))
            self.__alignment = alignment
        else:
            raise TypeError("Alignment must be an integer")
        self.__age = 0

    """
    Conceives with another prisoner, yielding two offspring.
    
    @param other Prisoner to reproduce with.
    @return Tuple of two prisoners, with alignments similar to their parents.
    """
    def conceive(self, other) -> Tuple[Prisoner, Prisoner]:
        if not isinstance(other, Prisoner):
            raise TypeError("Expected Prisoner instance, received: {}".format(type(other)))
        if self == other:
            raise ValueError("Prisoner cannot crossover with itself.")
        return None

    """
    Determines if the prisoner wishes to defect, if given the chance to cooperate.
    
    A prisoner's defection is based on chance, influenced by his alignment at birth.
    A prisoner with an alignment > 0.5 is more likely to defect,
    while a prisoner with an alignment of < 0.5 is more likely to cooperate.
    @return True if the prisoner wishes to defect.
    """
    def defect(self) -> bool:
        return randrange(Prisoner.__ALIGNMENT_LIMIT) < self.__alignment

    """
    @return Likelihood to defect, ranging from [0, __ALIGNMENT_LIMIT).
    """
    @property
    def alignment(self) -> int:
        return self.__alignment

    """
    @return Number of generations of offspring of the prisoner.
    """
    @property
    def age(self) -> int:
        return self.__age
    """
    @return String representation of the prisoner.
    """
    def __str__(self):
        return "Prisoner{{age={}, alignment={}}}".format(str(self.__age), str(self.__alignment))
