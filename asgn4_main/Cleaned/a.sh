#!/bin/bash

bin/Parser.py test/custom.scala

python /home/mppiyush/project/Scala-Compiler/asgn4_main/Cleaned/src/ass.py /home/mppiyush/project/Scala-Compiler/asgn4_main/Cleaned/test/result.ir > /home/mppiyush/project/Scala-Compiler/asgn4_main/Cleaned/test/result.asm

spim -file /home/mppiyush/project/Scala-Compiler/asgn4_main/Cleaned/test/result.asm

rm /home/mppiyush/project/Scala-Compiler/asgn4_main/Cleaned/bin/*.pyc /home/mppiyush/project/Scala-Compiler/asgn4_main/Cleaned/bin/parsetab.py

