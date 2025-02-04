def sum_of_divisors(n):
    total = 1
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            total += i
            if i != n // i:
                total += n // i
    return total

def find_amicable_numbers(limit):
    amicable_numbers = set()
    for a in range(2, limit):
        b = sum_of_divisors(a)
        if b != a and sum_of_divisors(b) == a:
            amicable_numbers.add(a)
            amicable_numbers.add(b)
    return sum(amicable_numbers)

result = find_amicable_numbers(10000)
print(result)
