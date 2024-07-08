#!/usr/bin/env python3

def sing_99_bottles_of_beer(start):
    if start > 100:
        print("Please enter a number 100 or less.")
        return

    for i in range(start, 0, -1):
        print(f"{i} bottles of beer on the wall!")
        print(f"{i} bottles of beer on the wall! {i} bottles of beer! You take one down, pass it around!")
        print(f"{i-1 if i-1 > 0 else 'no more'} bottles of beer on the wall!\n")

# Ask the user for the starting number of bottles
start_bottles = int(input("How many bottles of beer are you counting down from (100 or less)? "))
sing_99_bottles_of_beer(start_bottles)

