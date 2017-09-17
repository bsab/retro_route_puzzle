# Retro Route Puzzle #

[![Test Build Status](https://travis-ci.org/edsonlb/maze-puzzle.svg?branch=master)](https://travis-ci.org/bsab/retro_route_puzzle/builds#)

Write a program that will output a valid route one could follow to collect all specified items within a map. The map is a json description of set of rooms with allowed path and contained object.
exercize starts with an input of:
json reppresentation of map starting room
list of object to collect

### Example ###
Input Start Room ID: 4

Input Objects To Collect: Knife, Potted Plant, Pillow
```
python retro_route_puzzle.py data.json 4 "knife" "Potted Plant" "Pillow"
```