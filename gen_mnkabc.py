import itertools

# m starts from 4320 and increments by 80 until it reaches 87440.
# n is a power of 2 starting from 4096 and ending at 65536.
# k is a power of 2 starting from 4096 and ending at 65536.
# a, b, and c are equal and are calculated as k + 32 and k + 64.


def powers_of_two(start, end):
    powers = []
    power = start
    while power <= end:
        powers.append(power)
        power *= 2
    return powers

# Generate possible values for n and k
n_values = powers_of_two(4096, 65536)
k_values = powers_of_two(4096, 65536)

# Generate possible values for m
m_values = list(range(4320, 87441, 80))

# Generate combinations of m, n, and k
combinations = itertools.product(m_values, n_values, k_values)

# Print combinations with calculated a, b, and c values
for m, n, k in combinations:
    a = b = c = k + 32
    print(f"{m},{n},{k},{a},{b},{c}")
    a = b = c = k + 64
    print(f"{m},{n},{k},{a},{b},{c}")
