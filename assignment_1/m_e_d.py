# Student Number: 5767 661 5
# Author: Jan van Rooyen
#
# Purpose: Contains functions use in the natural language processing assignments.
#

# Simple function used to iterate over all values in given matrix and output index and value to console.
# Parameter: matrix - A dictionary data type
# Parameter: x_length - The maximum number of items on the x-axis
# Parameter: y_length - The maximum number of items on the y-axis.
#
def printout_matrix(matrix, x_length, y_length):
    print('-----------------')
    for x_index in range(0, x_length):
        for y_index in range(0, y_length):
            if (x_index, y_index) in matrix.keys():
                print('({%d,%d}=%d)' %(x_index, y_index, matrix[x_index, y_index]) , end=' ')
        print()
# end def printout_matrix


# Function used to find the minimum editing distance between a source and target string.
#
# Parameter: source - Source string to be compared with
# Parameter: target - Target string to be compared with
# Parameter: cost_of_insertion - Weight of the cost of inserting a character - Default=1
# Parameter: cost_of_deletion -  Weight of the cost of deleting a character - Default=1
# Parameter: cost_of_substitution -  Weight of the cost of substituting a character - Default=2
# Parameter: print_matrix - Provides and option to output the final matrix to console - Default=False
# Returns: Integer - The final minimum edit distance between the given source and target strings.
#
def find_minimum_editing_distance(source, target, cost_of_insertion=1, cost_of_deletion=1, cost_of_substitution=2, print_matrix=False):
    # Instantiate an empty dictionary that will store the matrix.
    distance_matrix = {}

    # Store the length of the source string
    # with x_length being used for all x-axis operations
    source_length = len(source)
    x_length = source_length + 1

    # Store the length of the target string.
    # with y_length being used for all y-axis operations
    target_length = len(target)
    y_length = target_length + 1

    # Set the insertion values for the source against an empty target.
    y_index = 0
    for x_index in range(x_length):
        distance_matrix[x_index, y_index] = x_index

    # Set the insertion values for the target against an empty source.
    x_index = 0
    for y_index in range(y_length):
        distance_matrix[x_index, y_index] = y_index

    for x_index in range(1, x_length):
        for y_index in range(1, y_length):
            # Calculate the Deletion cost
            deletion_cost = distance_matrix[x_index - 1, y_index] + cost_of_deletion

            # Calculate the insertion cost
            insertion_cost = distance_matrix[x_index, y_index - 1] + cost_of_insertion

            # Calculate the substitution cost
            substitution_cost = distance_matrix[x_index - 1, y_index - 1]

            if source[x_index - 1] != target[y_index - 1]:
                substitution_cost = substitution_cost + cost_of_substitution

            # Set the matrix position [i][j] to the smallest value worked out above.
            smallest_cost = min(substitution_cost, deletion_cost, insertion_cost)
            distance_matrix[x_index, y_index] = smallest_cost

    if print_matrix:
        printout_matrix(distance_matrix, x_length, y_length)
    print("Minimum Edit Distance between '%s' and '%s' is %d" % (source, target, distance_matrix[x_length-1, y_length-1]))
# end def printout_matrix


#
#
#
if __name__ == '__main__':
    find_minimum_editing_distance('connect', 'commute',print_matrix=False)
    find_minimum_editing_distance(source='connect', target='contact',print_matrix=False)

