#!/bin/bash
ROT=$(python parallel.py "$1" 100 | tail -1)
echo $ROT
sips -r $ROT --out output.jpg $1
