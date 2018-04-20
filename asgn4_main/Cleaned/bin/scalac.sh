#!/bin/bash

Parser.py {1}

python ../src/ass.py ../test/result.ir > ../test/result.asm

spim -file ../test/result.asm

rm ./*.pyc ./parsetab.py

