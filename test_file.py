#
#
#
lst = [1, 1, 10, 1, 3, 2, 5, 10, 10, 11, 12, 11]

new_list = []
for i in lst:
    if i not in new_list:
        new_list.append(i)


print(lst)
print(new_list)
