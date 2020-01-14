#!/bin/bash

# Change to directory
cd ~/selfie2anime-tutorial

# Check for updates
git fetch --all
git checkout master
git reset --hard origin/master

# Run
source ~/tensorflow-1.15.0/bin/activate
python main.py --dataset faceart --phase video --light True
