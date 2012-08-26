#!/usr/bin/env python
# -*- encoding: utf-8 -*-
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

import math
import os
import random
import sys

def default_accept_lower_quality_sometimes_function(old_quality, new_quality, temperature, K=0.01):

    change_in_quality = new_quality - old_quality
    temperature_normalized = temperature * K

    if temperature_normalized == 0.0:
        raise Exception(str(locals()))

    accept_despite_lower_quality_probability = math.exp(old_quality - new_quality) / temperature_normalized

    return accept_despite_lower_quality_probability > random.random()


def run(generate_new_solution,
        quality_of,
        initial_solution=None,
        temperature=1.0,
        epsilon=0.00001,
        last_change=sys.maxint,
        iterations_before_temperature_change=100,
        alpha=0.85,
        new_temperature=lambda alpha=0.85, old_temperature=1.0: alpha * old_temperature,
        accept_lower_quality_solution_sometimes=None):

    solution = initial_solution
    current_quality = 0.0

    # diagnostics
    run_info = {}
    iterations = 0
    temperature_changes = -1  # lacking do / while we do this weirdly
    quality_improvements = 0
    quality_lowerings_accepted = 0


    if accept_lower_quality_solution_sometimes is None:
        accept_lower_quality_solution_sometimes = default_accept_lower_quality_sometimes_function

    while last_change > epsilon or last_change < 0.0:  # have we made progress?
        temperature_changes += 1

        for i in range(iterations_before_temperature_change):

            new_solution = generate_new_solution(solution)

            new_quality = quality_of(new_solution, old_solution=solution)

            accepted_new_solution = False

            if new_quality >= current_quality:
                accepted_new_solution = True

                if new_quality > current_quality:
                    quality_improvements += 1

            else:
                # don't do elif to catch exceptions in the function
                # more gracefully
                try:
                    accept_lower_quality = \
                        accept_lower_quality_solution_sometimes(current_quality,
                                                                new_quality,
                                                                temperature)
                except Exception, msg:
                    print str(locals())
                    raise

                if accept_lower_quality:
                    accepted_new_solution = True
                    quality_lowerings_accepted += 1
                    print "accepted lower quality solution [%s]," \
                        " going from quality of %s to %s" % (new_solution,
                                                             current_quality,
                                                             new_quality)

            if accepted_new_solution:
                solution = new_solution
                last_change = new_quality - current_quality
                current_quality = new_quality


            iterations += 1

        this_run_was_an_improvement = last_change > epsilon
        if this_run_was_an_improvement:
            temperature = new_temperature(alpha, temperature)

        print "end iteration; ", locals()


    run_info = {"iterations": iterations,
                "quality improvements": quality_improvements,
                "quality lowerings accepted": quality_lowerings_accepted,
                "temperature_changes": temperature_changes,
                "ending quality": current_quality,
                }

    return solution, run_info



def trivial_example():
    def new_solution(old_solution):
        decision = random.random()

        if decision < 0.4:
            new_solution = old_solution[:-1]
        elif decision > 0.9:
            new_solution = old_solution + [1.61]
        else:
            new_solution = old_solution[:]

        return new_solution

    def quality_of(new_solution, old_solution=None):
        if new_solution is None:
            return 0.0
        if len(new_solution) < 1:
            return 1.0
        return 1 / (len(new_solution) + 1.)

    trivial_solution, run_info = run(new_solution,
                                     quality_of,
                                     initial_solution=range(10))

    return trivial_solution, run_info


if __name__ == "__main__":
    print trivial_example()

