
<br /><h3 align="center">Prisoner\'s Dilemma - Python</h3>

  <p align="center">
  Attempts to teach a group of prisoners how to solve the <a href="https://en.wikipedia.org/wiki/Prisoner%27s_dilemma">Prisoner's Dilemma</a> problem using genetic algorithms.
    <br />
	<br />
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#usage">Usage</a></li>
	<li><a href="#training">Training</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This program was my first attempt at implementing the core concepts of genetic algorithms (fitness -> mutation/crossover -> pruning -> ↵). I would improve my understanding of these concepts when approaching a harder genetic algorithm problem: [GitHub: Blackjack-Genetic](https://github.com/KevinTyrrell/Blackjack-Genetic) (teaching agents how to play well at Blackjack using genetic algorithms).


<!-- USAGE EXAMPLES -->
## Usage

### Prerequisites

* Python 3

> Auto generated by [Argparse](https://docs.python.org/3/library/argparse.html) via commit [3871564](https://github.com/KevinTyrrell/PrisonersDilemma-Py/commit/387156477fcaa9ac088c418d6190f755d8bb371e).

```
usage: PrisonersDilemma.py [-h] [-p POPULATION] [-g GENERATIONS]
                           [-m MUTATION_RATE] [-t TESTS] [-s SEED]

optional arguments:
  -h, --help        show this help message and exit
  -p POPULATION     Specifies the population size for the group of prisoners.
                    (default: 1024)
  -g GENERATIONS    Specifies the number of generations which should be
                    simulated. (default: 100)
  -m MUTATION_RATE  Specifies the rate in which mutations occur in each
                    genome. (default: 0.15)
  -t TESTS          Specifies the number of tests the prisoners are subjected
                    to per generation. (default: 10)
  -s SEED           Specifies the random number generator seed to be used.
                    (default: 1071815745)
```

<!-- TRAINING EXAMPLE -->
## Training

**Example Training Parameters**
> `python PrisonersDilemma.py -g 50 -m 0.05 -t 20 -s 23915871`
* **Population**: *default* (number of prisoners)
* **Generations**: 50 (number of iterations)
* **Mutation Rate**: 0.05 (chance [0.0, 1.0] for a gene to be mutated)
* **Tests**: 20 (number of trials to subject prisoners to the Prisoner\'s Dilemma)
* **Seed**: 23915871


    ~~~~~~ Generation #0 ~~~~~~
    Average Defection (%)29.83
    Average Prisoner Age 0.000
    ~~~~~~ Generation #1 ~~~~~~
    Average Defection (%)30.87
    Average Prisoner Age 0.500
    ~~~~~~ Generation #2 ~~~~~~
    Average Defection (%)33.41
    Average Prisoner Age 0.753
    ~~~~~~ Generation #3 ~~~~~~
    Average Defection (%)37.82
    Average Prisoner Age 0.864
    ~~~~~~ Generation #4 ~~~~~~
    Average Defection (%)44.04
    Average Prisoner Age 0.922
	
	
*Generations #5 -> #45 Omitted ([see-below](#Takeaways))*


    ~~~~~~ Generation #45 ~~~~~~
    Average Defection (%)96.38
    Average Prisoner Age 1.183
    ~~~~~~ Generation #46 ~~~~~~
    Average Defection (%)96.55
    Average Prisoner Age 1.144
    ~~~~~~ Generation #47 ~~~~~~
    Average Defection (%)96.75
    Average Prisoner Age 1.143
    ~~~~~~ Generation #48 ~~~~~~
    Average Defection (%)95.98
    Average Prisoner Age 1.101
    ~~~~~~ Generation #49 ~~~~~~
    Average Defection (%)95.69
    Average Prisoner Age 1.168


#### Takeaways

*Full Output (Generations #0 -> #49) -> [Git Gist](https://gist.github.com/KevinTyrrell/a86f81f24ae49fd0de8c21fa090fc012)*

* Defection rate is approaching `100%`, but cannot reach it due to negative mutations.
* Average age should remain low due to half of the population being culled each generation, however it seems like very few prisoner live past the age of 3. Perhaps with more generatios, this number would increase.
* Increasing the number of tests per generation seems to dramatically speed up the learning process, as it makes the cost function much more accurate.
* By generation `15`, over `90%` of the population choses to defect. Over the next `35` generations, this is only refined by ~`5%`.


<!-- LICENSE -->
## License

Distributed under the GPL-3.0 License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Kevin Tyrrell - KevinTearUl@gmail.com

Project Link: [https://github.com/KevinTyrrell/PrisonersDilemma-Py](https://github.com/KevinTyrrell/PrisonersDilemma-Py)


