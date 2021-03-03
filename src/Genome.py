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
from typing import Callable
from random import getrandbits


class Genome:
    # Number of genes in each genome.
    __GENES = 32

    """
    Number of genes in the genome.
    
    @:return Number of genes in the genome.
    """
    @staticmethod
    def gene_len() -> int:
        return Genome.__GENES

    """
    Constructs a new genome.

    @:param genes Genes of the genome.
    """
    def __init__(self, genes: int = getrandbits(__GENES)):
        self.__genes = genes

    @property
    def genes(self) -> int:
        return self.__genes

    """
    Mutates the genome in accordance with the callable mutation function.
    
    :param mutation_cb Callback function which returns true if a mutation should occur.
    """
    def mutate(self, mutation_cb: Callable[[], bool]) -> None:
        for i in range(Genome.__GENES):
            if mutation_cb():
                self.__flip_bit(i)

    """
    Performs crossover on the genome and its partner.
    
    :param crossover_cb Callback function which returns true if crossover should occur.
    """
    def crossover(self, other: Genome, crossover_cb: Callable[[], bool]) -> None:
        stop = min(self.__genes, other.__genes)
        bit = 0
        while stop > 0:
            if crossover_cb():
                temp = self.__genes
                self.__copy_bit(other.__genes, bit)
                other.__copy_bit(temp, bit)
            # Iterate over all bits that the genomes share in common (no leading zeroes).
            bit += 1
            stop >>= 1

    """
    @:param bit Bit to be set.
    """
    def __set_bit(self, bit: int) -> None:
        assert 0 <= bit < Genome.__GENES
        self.__genes = self.__genes | (1 << bit)

    """
    @:param bit Bit to be cleared.
    """
    def __clear_bit(self, bit: int) -> None:
        assert 0 <= bit < Genome.__GENES
        self.__genes = self.__genes & ~(1 << bit)

    """
    @:param bit Bit to be flipped.
    """
    def __flip_bit(self, bit: int) -> None:
        assert 0 <= bit < Genome.__GENES
        self.__genes = self.__genes ^ (1 << bit)

    """
    @:param num Integer to copy bit from.
    @:param bit Bit to be copied.
    """
    def __copy_bit(self, num: int, bit: int) -> None:
        assert 0 <= bit < Genome.__GENES
        mask = 1 << bit
        self.__genes = (self.__genes & ~mask) | (num & mask)
