#!/bin/bash
for l1 in a b c d e f g h
do
	for n1 in 1 2 3 4 5 6 7 8
	do
		for l2 in a b c d e f g h
		do
			for n2 in 1 2 3 4 5 6 7 8
			do
				STRING=$l1
				STRING+=$n1
				STRING+="-"
				STRING+=$l2
				STRING+=$n2
				echo $STRING
				echo $STRING | python2 chess.py
			done
		done
	done
done

