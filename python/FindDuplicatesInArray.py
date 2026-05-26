def find_duplicates(array):
    seen = set()
    duplicates = set()

    for num in array:
        if num in seen:
            duplicates.add(num)
        else:
            seen.add(num)
    return duplicates

array = [1, 2, 3, 4, 5, 3, 2, 6, 7, 8, 1]
duplicates = find_duplicates(array)
print("Duplicates in the array:", duplicates)