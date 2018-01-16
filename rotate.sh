#!/bin/bash
ROT=$(python parallel.py "$1" 100 | tail -1)
echo "Rotating $1 by $ROT degrees"
sips -r $ROT --out output.jpg $1
