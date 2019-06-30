from random import seed, randrange, getrandbits, random, shuffle
from sys import maxsize

# How many prisoners in the simulation.
PRISONER_POP = 100
# How often mutations occur while copying each gene-bit.
MUTATION_RATE = 0.15
# Amount of times two prisoners are subjugated to the dilemma per generation.
TESTS_PER_GENERATION = 5
# Number of generations to be performed.
MAX_GENERATIONS = 10
# Seed for this particular simulation.
SEED = 15486277

# Name of the program.
PROGRAM_NAME = "GeneticAlgorithm"
# 10 raised to the significant digits of the prisoner's alignment float.
ALIGNMENT_MAX = 100000000

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
    
# Defines a prisoner, who must decide whether to defect or to cooperate.
class Prisoner:
    """
    If no alignment is specified, the prisoner is assigned a random alignment.
    @param [alignment] Likelihood to defect, ranging from [0, ALIGNMENT_MAX).
    @field __alignment
    @field __age Number of generations of offspring of the prisoner.
    """
    def __init__(self, alignment = None):
        if alignment == None:
            self.__alignment = randrange(ALIGNMENT_MAX)
        elif isinstance(alignment, int):
            if alignment >= ALIGNMENT_MAX or alignment < 0:
                raise ValueError("Alignment of {} was out of bounds [0, ALIGNMENT_MAX)".format(str(alignment)))
            self.__alignment = alignment
        else:
            raise TypeError("Alignment must be an integer")
        self.__age = 0
    """
    A prisoner decision to defect is by chance, but is influenced
    by his alignment (whether he favors defecting or not).
    @return True if the prisoner decides to defect.
    """
    def defect(self):
        return randrange(ALIGNMENT_MAX) < self.__alignment
    """
    Performs a crossover with another Prisoner.
    @param other_prisoner Prisoner to perform the crossover reproduction with.
    @return Tuple of two prisoners, with alignments similar to their parents.
    """
    def crossover(self, other_prisoner):
        if not isinstance(other_prisoner, Prisoner):
            raise TypeError("Expected Prisoner instance, received: {}".format(type(other_prisoner)))
        if self == other_prisoner:
            raise ValueError("Prisoner cannot crossover with itself")
        
        bf1 = bitfield(self.__alignment)
        bf2 = bitfield(other_prisoner.__alignment)
        bf1_len, bf2_len = len(bf1), len(bf2)
        bf_cross_len = min(bf1_len, bf2_len)
        
        c1_align, c2_align, decimal, bit = 0, 0, 1, 0
        
        # Helper function for random mutations.
        def mutator(bit):
            return 1 - bit if random() < MUTATION_RATE else bit
        # Helper function for fast conversion from binary.
        def adder(bit_1, bit_2):
            bit_1 = mutator(bit_1)
            bit_2 = mutator(bit_2)
            if bit_1:
                nonlocal c1_align
                c1_align += decimal
            if bit_2:
                nonlocal c2_align
                c2_align += decimal
        # Helper function for fast swapping of bits.
        def crosser(bit_1, bit_2):
            if bool(getrandbits(1)):
                adder(bit_2, bit_1)
            else:
                adder(bit_1, bit_2)
        
        # Iterate over all bits, crossing them or mutating them at random.
        # Afterwards, return two new Prisoner children with those alignments.
        while bit < bf_cross_len:
            crosser(bf1[-bit - 1], bf2[-bit - 1])
            bit += 1
            decimal += decimal
        while bit < bf1_len:
            crosser(bf1[-bit - 1], 0)
            bit += 1
            decimal += decimal
        while bit < bf2_len:
            crosser(0, bf2[-bit - 1])
            bit += 1
            decimal += decimal
        self.__age += 1
        other_prisoner.__age += 1
        return (Prisoner(c1_align), Prisoner(c2_align))
    """
    @return Likelihood to defect, ranging from [0, ALIGNMENT_MAX).
    """
    def get_alignment(self):
        return self.__alignment
    """
    @return Number of generations of offspring of the prisoner.
    """
    def get_age(self):
        return self.__age
    """
    @return String representation of the prisoner.
    """
    def __str__(self):
        return "Prisoner{{age={}, alignment={}}}".format(str(self.__age), str(self.__alignment))

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

def main():
    print("Starting up.")
    if MUTATION_RATE < 0 or MUTATION_RATE > 1:
        raise ValueError("Mutation rate of {} is not within acceptable bounds of [0.0, 1.0]".format(str(MUTATION_RATE)))
    if PRISONER_POP <= 0 or PRISONER_POP % 4 != 0:
        raise ValueError("Initial population of {} must a positive number and a multiple of four".format(str(PRISONER_POP)))
    seed(SEED)
    
    def assess_pop(pop_list):
        rolling_avg = None
        for i in range(PRISONER_POP):
            p = pop_list[i]
            a = p.get_alignment()
            if rolling_avg != None:
                rolling_avg = rolling_avg + (a - rolling_avg) / (i + 1.0)
            else:
                rolling_avg = a
        print("Average defection rate: {}%".format(str(rolling_avg / ALIGNMENT_MAX)))
    
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



