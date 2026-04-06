from functools import reduce

nums = [1, 2, 3, 4, 5]

# map → square numbers
squared = list(map(lambda x: x**2, nums))
print(squared)

# filter → even numbers
even = list(filter(lambda x: x % 2 == 0, nums))
print(even)

# reduce → sum
total = reduce(lambda x, y: x + y, nums)
print(total)