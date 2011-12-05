#!/bin/bash

#date="20060202"
date=$1

for i in {0..19}; do
    echo time python upload.py output.$date.$i.json
    time python upload.py output.$date.$i.json
    sleep 1
done
