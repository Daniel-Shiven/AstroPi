# If animal is within 5% range of humidity
# If animal is within 15 range of celsius 
# 
# SUDO CODE (SECOND DRAFT)
# 
# 1. Make a list of animals that fit the temperature and humidity requirements
# 
# 2. For every list of combinations of these animals with a min of 3 animals in each combination
# 
# 3. Test for each if the combination to see if it hits all the pyschological benefits.
#
# 4. If it does, then record its weight and compare the weight to the previous lowest weight.
#
# 5. If it is lower, then set the topchoice list to the weight and corresponding combination to that
# 
# 6. Once all combinations have been explored, the one that is stored in the topchoice variable remains
#
# 
#
#  
#  
# Understanding power sets:
#
# A power set is the set of all possible subsets of a given set. For example,
# if we have a set {1, 2, 3}, its power set is {{}, {1}, {2}, {3}, {1, 2}, {1, 3}, {2, 3}, {1, 2, 3}}.
# 
#
# 
#   
# Understanding Binary:
# For example, the binary number 1010 represents the number 10 in decimal form. Here, the rightmost
# digit (the "ones" digit) is 0, which means that there are no 1s in the 2^0 place. The second digit
# from the right (the "twos" digit) is 1, which means that there is a 1 in the 2^1 place, or 2. The
# third digit from the right (the "fours" digit) is 0, which means that there are no 1s in the 2^2 place.
# And the fourth digit from the right (the "eights" digit) is 1, which means that there is a 1 in the 2^3
# place, or 8. So the binary number 1010 represents the decimal number 8 + 2 = 10.



#============================================================================#
#============================ FINAL PROGRAM CODE ============================#
#============================================================================#


# Establishing every animal's key variables (13 animals)
# First establishes animal name
# Second establishes the animals benefits with 0 or 1 (10 benefits)
# Third establishes temperature, humidity, and weight

animal_identity = [ ["golden", [1,1,1,1,1,1,0,0,0,0],[20,55,27.5]],
["pug", [0,1,0,1,0,0,0,0,0,0],[21,55,7.25]],
["labradoodle", [1,1,0,1,0,0,1,0,0,0],[21,55,22.5]],
["greyhound", [0,0,0,1,1,1,1,0,0,0],[19.5,55,27.5]],
["labradore", [1,1,1,1,1,1,1,0,0,0],[19.5,55,27.5]],
["poodle", [1,0,1,1,1,1,1,1,0,0],[19.5,55,22.5]],
["collie", [1, 1, 0, 1, 1, 1, 1, 1, 0, 0],[19.5,55,17]],
["terrier", [0, 1, 0, 1, 1, 1, 1, 1, 0, 0],[19.5,55,7]],
["sphynx", [0,1,1,0,0,0,0,0,1,1],[25,55,4]],
["persian", [0, 1, 1, 0, 0, 0, 0, 0, 1, 1],[19.5,55,4]],
["rabbit", [1, 1, 0, 1, 0, 1, 1, 0, 0, 0],[18,55,3.9]],
["hamster", [1, 1, 0, 1, 0, 0, 1, 0, 0, 0],[21,45,.095]],
["easternBox", [1, 1, 0, 1, 0, 0, 1, 0, 0, 0],[25,60,4]],
["greekTortoise", [1, 1, 0, 1, 0, 0, 1, 0, 0, 0],[26.5,60,10.5]]]


# This is the function that will produce our ideal combination of animals to send to the ISS,
# based on temp and humidity, then pyschological benefits, and finally lowest weight
def W_Rizz_Match(temp, humidity, animal_identity):
    # Initialize a list to store eligible animals
    eligible_animals = []
   
    # Loop through each animal and check if it's temperature and humidity are within the desired range
    for i in range(len(animal_identity)):
        if abs(temp - animal_identity[i][2][0]) <= 6 and abs(humidity - animal_identity[i][2][1]) <= 10 * humidity:
            eligible_animals.append(animal_identity[i])
   
    #Print a list of the eligible animals for bug fixing purposes (Remove in final draft)
    print("The eligible animals are:",)
    for i in range(len(eligible_animals)):
        print(eligible_animals[i][0])


    #This variable will store the weight and animals in the best list. Weight is set to 1k as the program
    #below needs a predefined weight for topchoice when it is first chosen
    topchoice = (1000,[])
    currentBest = 1
    isBest = False

    # Loop through each combination of eligible animals with a power set: all the possible subsets in a set
    # 2^ of the set length will yield the # of all possible sets.
    for i in range(1, 2**len(eligible_animals)):

        combination = [] #Initializes the list for a combination

        #This will run once for every eligible animal - checks to see if the eligible animal's index corresponds
        #With the number in the for i function. << is a bitwise shift operator
        for j in range(len(eligible_animals)):
            if i & (1 << j): # Compares binary i to binary 1 shifted to the left by j bits (10,100,1000 - only one 1 in the #)
                             # The & compares the corresponding bits of two binary numbers and sees if they are both 1
                             # for example i = 3 (110) and j=1 (10), the 2nd bits are both 1 so it evaluates to true
                combination.append(eligible_animals[j]) #then add it to the list

        total = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #Each 0 represents a pro

        #Merging the lists - if animal's pros are not in total then add them
        for i in range(len(combination)):
            for j in range(len(total)):
                if combination[i][1][j] == 1 and total[j] == 0: #For each index
                    total[j] = 1

        print(sum(total), ">=", currentBest)
        isBest = False
        if sum(total) > currentBest:
            isBest = True

        if sum(total) >= currentBest:
            currentBest = sum(total)
            weight = 0
            final_list = []
            for i in range(len(combination)):
                weight += combination[i][2][2]
                final_list.append(combination[i][0])

            print(f"Another list is: {final_list}\nIt's weight is: {weight}")

            print(isBest)
            if weight < topchoice[0]:
                topchoice = []
                topchoice.append(weight)
                topchoice.append(final_list)
            if isBest:
                topchoice = []
                topchoice.append(weight)
                topchoice.append(final_list)

    return topchoice


bestList = W_Rizz_Match(27,36,animal_identity)

print(bestList)