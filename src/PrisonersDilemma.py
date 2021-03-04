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

import argparse
from Simulation import Simulation

parser = argparse.ArgumentParser(description="Attempts to teach a population of prisoners"
                                             " (agents) how to solve the Prisoner's Dilemma",
                                 epilog="https://github.com/KevinTyrrell/PrisonersDilemma-Py",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-p", dest="population", default=2 ** 10, type=int,
                    help="Specifies the population size for the group of prisoners.")
parser.add_argument("-g", dest="generations", default=100, type=int,
                    help="Specifies the number of generations which should be simulated.")
parser.add_argument("-m", dest="mutation_rate", default=0.15, type=float,
                    help="Specifies the rate in which mutations occur in each genome.")
parser.add_argument("-t", dest="tests", default=10, type=int,
                    help="Specifies the number of tests the prisoners are subjected to per generation.")
parser.add_argument("-s", dest="seed", default=(561 * 1105 * 1729), type=int,
                    help="Specifies the random number generator seed to be used.")


def main():
    args = parser.parse_args()
    population = args.population
    generations = args.generations
    mutation_rate = args.mutation_rate
    tests = args.tests
    seed = args.seed

    Simulation.run(population, generations, mutation_rate, tests, seed)


main()
