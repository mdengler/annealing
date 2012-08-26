#!/usr/bin/env python
"""

Toy simulated annealing implemention from Skiena's "Algorithm Design Manual"

Simulated-Annealing()
    Create initial solution S
    Initialize temperature t
    repeat
        for i = 1 to iteration-length do
            Generate a random transition from S to Si
            If (C(S) ≥ C(Si )) then S = Si
            else if (e(C(S)−C(Si ))/(k·t) > random[0, 1)) then S = Si
        Reduce temperature t
    until (no change in C(S))
    Return S


Copyright (c) 2012 Martin Dengler <martin@martindengler.com>
License: GPL v3+
"""

import os
import sys



def run(solution=None,
        temperature=0.5,
        epsilon=0.00001,
        last_change=sys.maxint,
        iterations_before_temperature_change=100,
        alpha=0.85,
        new_temperature=lambda alpha=0.85, old_temperature=1.0: alpha * old_temperature):

    while last_change > epsilon:

        for i in range(iterations_before_temperature_change):

            new_transition = generate_transition(solution)
            new_solution   = generate_solution(solution, new_transition)
            new_quality    = quality_of(new_solution, old_solution=solution, transition=new_transition)

            if (new_quality > current_quality
                or
                accept_lower_quality_solution_sometimes(old_quality, new_quality, temperature)):
                solution = new_solution

        temperature = new_temperature(alpha, temperature)

    return solution



def test():
    print "stub"


if __name__ == "__main__":
    test()

