## Author Chirag Dhawan
# Markov snakes and ladders
# It finds the expected moves of dice required to finish the game
# The dice is biased and total of 5000 simulations of each board configuration is run

#Input
def inputs():
    tests=[]
    no_of_test_cases = int(input()) #input no of test cases
    for i in range(0, no_of_test_cases):
        dice_probs = input() #input bias comma seperated
        probs=[]
        for i in range(0,6):
            probs.append(float(dice_probs.split(',')[i])) #Dice bias probabilities are split and converted to float

        no_of_ladders_snakes = input() #input no of ladders and snakes comma seperated
        no_of_ladders = int(no_of_ladders_snakes.split(',')[0]) # split to get ladders
        no_of_snakes = int(no_of_ladders_snakes.split(',')[1]) # split to get snakes
        ladders_raw = input() # input ladder start and end comma seperated and different ladders space seperated
        ladders = []
        for j in range(0, no_of_ladders):
            ladders.append(ladders_raw.split(" ")[j]) #split to get distinct start end pair

        snakes_raw = input()# input snakes start and end, comma seperated and different snakes space seperated
        snakes = []
        for k in range(0, no_of_snakes):
            snakes.append(snakes_raw.split(" ")[k]) #split to get distinct start end pair

        tests.append(Board(probs,ladders,snakes,no_of_ladders,no_of_snakes)) #appending the different board ojects to the test list
    return tests

##########################################################################################
########################################################################################

# Board class

class Board(object):

    def __init__(self, dice_probs,ladders, snakes,no_of_ladders,no_of_snakes, total_sqaures=100): # total squares can be changed
        self.up_or_down= {} #dictionary containing the key value pair where start number is key and end number is the value
        self.dice_probs=dice_probs
        self.total_squares=total_sqaures
        self.jump_in_ladders(no_of_ladders,ladders) # this function is defined later and it adds the ladder start end pair to the dictionary self.up_or_down
        self.jump_in_snakes(no_of_snakes,snakes) # this function is defined later and it adds the snakes start end pair to the dictionary self.up_or_down

    def jump_in_ladders(self,no_of_ladders,ladders):
        for i in range(0,no_of_ladders):
            start=int(ladders[i].split(',')[0]) #start of the ladder
            end = int(ladders[i].split(',')[1]) #ending of the ladder
            if start >= end:
                raise ValueError("A Ladder cannot take down")
            if start in self.up_or_down:
                raise ValueError("Cannot have mulitple snakes and/or ladders on a single number")
            self.up_or_down[start] = end

    def jump_in_snakes(self,no_of_snakes,snakes):
        for i in range(0,no_of_snakes):
            start = int(snakes[i].split(',')[0]) #start of the snake
            end = int(snakes[i].split(',')[1]) #ending of the snake
            if start <= end:
                raise ValueError("A Snake is not a ladder and cannot take you up")
            if start in self.up_or_down:
                raise ValueError("Cannot have mulitple snakes and/or ladders on a single number")
            self.up_or_down[start] = end



    def game(self):                 #This function plays the game and returns the expected moves after 5000 games
        total_moves = 0
        for t in range(0,5000):     # Simulating 5000 games
            current_number = 1
            while(current_number!=self.total_squares):
                simulated_roll=simulation(self.dice_probs)   #calls the function simulation which is defined later, returns a dice number
                new_number = current_number + int(simulated_roll)
                total_moves=total_moves+1                    #update the total moves
                if new_number in self.up_or_down.keys():     # if the new number after a roll is in the up_or_down dictionary keys
                    current_number=int(self.up_or_down[new_number])    # then get the number which is the value of the key and update current
                elif new_number<=self.total_squares:                        #else if the number is less than 100
                    current_number=new_number                           # update the current number to new number
        return(total_moves/5000)                                # return the expectation of total moves

#################################################################################################################

import random   #import random to get random values

# This function is used to get a roll of dice using the bias probabilities
def simulation(bias_probs):
    roll=random.random()   # this will output random values between 0 and 1
    prob_sum=0
    dice=1
    for probs in bias_probs:
        prob_sum=prob_sum+probs
        if roll<=prob_sum:  # For e.g if bias probs are 0.32,0.32,0.12,0.04,0.07,0.13
            return dice     # then this function will output 1 if the roll is less than or equal to 0.32
        else:               # and 2 if roll>0.32 and <=0.64 and so on.
            dice=dice+1


#### Main calls the inputs and prints the result using the Board's game function
if __name__ == "__main__":
    tests = inputs()
    for t in tests:
        print(t.game())





