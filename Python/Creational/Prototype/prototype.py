# TODO: Explanation
# TODO: Write tests

final_list = []
temp_list = [1, 2, 3]
final_list.append(temp_list)
temp_list.append(4)
print(final_list) #output: [[1, 2, 3, 4]]


my_list = [[1, 2, 3], [4, 5, 6], 7, 8]
new_list = my_list.copy()
my_list[3] = 9
my_list[1][1] = 2
print(my_list)    #output: [[1, 2, 3], [4, 2, 6], 7, 9]
print(new_list)  #output: [[1, 2, 3], [4, 2, 6], 7, 8]


import copy
my_list = [[1, 2, 3], [4, 5, 6], 7, 8]
new_list = copy.deepcopy(my_list)
my_list[3] = 9
my_list[1][1] = 2
print(my_list)    #output: [[1, 2, 3], [4, 2, 6], 7, 9]
print(new_list)  #output: [[1, 2, 3], [4, 5, 6], 7, 8] (without any changes)
