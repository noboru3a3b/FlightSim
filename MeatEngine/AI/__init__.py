"""Meat Engine AI Package

A set of tools designed for evaluating board state and selecting a move.

Currently supports (in a limited fashion, see below):
 - Human player
 - Random selection
 - MTD(f)

TODO Should support:
 - Alpha-Beta
 - Minimax
 - Betamax (just kidding, nobody supports Betamax)


the current code is hardcoded for analyzing Tic Tac Toe. Some minor
adaptation of the code should be all that's necessary to get it to
work for chess, checkers, mancala, nim, or just about any
deterministic, turn based, two player adversarial game of full
information.
"""
