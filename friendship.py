#!/usr/bin/env python3

from collections import namedtuple
from functools import partial
from itertools import islice
from math import exp, sqrt
from math import pi as π
from random import random

DistributionParameters = namedtuple('DistributionParameters', ('μ', 'σ'))
CrossValleyFriendship = namedtuple('CrossValleyFriendship', ('W', 'E'))

def normal(μ, σ):
    def density(x):
        return (1/(σ*2*π))*exp(-(x-μ)**2/(2*σ**2))
    return density

standard_normal = partial(normal, σ=1)

def rejection_sampler(distribution, domain):
    lower, upper = domain
    while True:
        reading = random() * (upper - lower) + lower
        roll_to_exist = random()
        if roll_to_exist < distribution(reading):
            yield reading

def normal_population(μ, σ, n):
    distribution = normal(μ, σ)
    inferred_domain = [μ + bound for bound in (-4*σ, +4*σ)]
    return sorted(islice(rejection_sampler(distribution, inferred_domain), n))

def summon_populations(
        west_distribution_parameters, east_distribution_parameters, n):
    return [normal_population(*params, n=n)
            for params in (west_distribution_parameters,
                           east_distribution_parameters)]

def match(west_distribution_parameters, east_distribution_parameters, n):
    westerners, easterners = summon_populations(
        west_distribution_parameters, east_distribution_parameters, n)
    matches = set()
    while westerners and easterners:
        to_match = westerners.pop()  # without loss of generality
        best_diff = float('inf')
        for i, potential_match in enumerate(reversed(easterners)):
            match_diff = abs(to_match - potential_match)
            if match_diff < best_diff:
                best_diff = match_diff
                best_index = len(easterners) - i - 1
                continue
            if potential_match < to_match and match_diff > best_diff:
                break
        match = easterners.pop(best_index)
        matches |= CrossValleyFriendship(W=to_match, E=match)
    return matches

def squirrel_ratio_in_neighborhood(
        west_distribution_parameters, east_distribution_parameters, μ, ɛ, n):
    westerners, easterners = summon_populations(
        west_distribution_parameters, east_distribution_parameters, n)
    west_census, east_census = [len([s for s in population if abs(s - μ) < ɛ])
                                for population in (westerners, easterners)]
    return west_census/east_census


if __name__ == "__main__":
    central_neighborhood_ambiance = squirrel_ratio_in_neighborhood(
        DistributionParameters(0, 1), DistributionParameters(0, 1),
        0, 0.5, n=1000
    )
    print(central_neighborhood_ambiance)
    assert abs(1 - central_neighborhood_ambiance) < 0.1  # usually, anyway
