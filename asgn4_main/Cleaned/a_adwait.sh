#!/bin/bash

bin/Parser.py ${1}

python /home/adwait/Documents/Acads/2017-18-II/CS335/Scala_Git/Scala-Compiler/asgn4_main/Cleaned/src/ass.py /home/adwait/Documents/Acads/2017-18-II/CS335/Scala_Git/Scala-Compiler/asgn4_main/Cleaned/test/result.ir > /home/adwait/Documents/Acads/2017-18-II/CS335/Scala_Git/Scala-Compiler/asgn4_main/Cleaned/test/result.asm

spim -file /home/adwait/Documents/Acads/2017-18-II/CS335/Scala_Git/Scala-Compiler/asgn4_main/Cleaned/test/result.asm

rm /home/adwait/Documents/Acads/2017-18-II/CS335/Scala_Git/Scala-Compiler/asgn4_main/Cleaned/bin/*.pyc /home/adwait/Documents/Acads/2017-18-II/CS335/Scala_Git/Scala-Compiler/asgn4_main/Cleaned/bin/parsetab.py

