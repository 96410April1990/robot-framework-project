def twoSum(self, nums: List[int], target: int) -> List[int]:
    store = {}

    for i in range(len(nums)):
        if nums[i] in store:
            return [store[nums[i]], i]
        else
            store[target - nums[i]] = i 
    
#In the above program, we are using only one for loop. Hence the complexity will be O(n). If we use a for loop within a for loop,
#then the complexity becomes O(n square) and it is not ideal.

#Logic:
#
# - Input - [2, 7, 11, 15] -> Target - 9

# A simple solution is we loop through the list and deduct each integer element from the target. i.e 9 - 2 = 7 and then we verify
# if 7 is present in the dictionary. If it is not available, then we add the element to the dictionary.
# If the element is available in the dictionary, then we return the number we deducted from the target and the remainder.
#