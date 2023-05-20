import time

from rich import print

def print(text, endl=1):
    endline = "\n" * endl

    print(text, end=endline)
