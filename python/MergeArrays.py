def merge_sorted_arrays(arrOne, arrTwo):

    i, j = 0, 0
    merged_arrays = []

    while i < len(arrOne) and j < len(arrTwo):
        if arrOne[i] < arrTwo[j]:
            merged_arrays.append(arrOne[i])
            i += 1
        else:
            merged_arrays.append(arrTwo[j])
            j += 1

    while i < len(arrOne):
        merged_arrays.append(arrOne[i])
        i += 1
    
    while j < len(arrTwo):
        merged_arrays.append(arrTwo[j])
        j += 1

    return merged_arrays

arr1 = [1, 3, 5]
arr2 = [2, 4, 6]

merged_array = merge_sorted_arrays(arr1, arr2)
print(merged_array)
            