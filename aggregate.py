#!/usr/bin/env python

import glob
from os.path import isdir
from ruamel import yaml
import sys


def main(location):
    if isdir(location):
        path = f'{location}/*.yml'
        files = glob.glob(path)
    else:
        files = [location]

    recipes = []
    for name in files:
        with open(name) as stream:
            data = yaml.round_trip_load(stream)
            recipes.append(data)
    yaml.round_trip_dump(recipes, sys.stdout)


if __name__ == "__main__":
   main(sys.argv[1])
