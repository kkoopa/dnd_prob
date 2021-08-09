#!/usr/bin/env python3

#expected value of max or min of kdn
def ex(n, k):
    def ex_min(n, k):
        if k == 1:
            return 0.5 * (n + 1)
        if k == 2:
            return (n + 1) * ((n << 1) + 1) / (6 * n)
        if k == 3:
            m = n + 1
            return m * m / (n << 2)

        return sum(x * ((n - x + 1)**k - (n - x)**k) for x in range(1, n + 1)) * n**-k


    def ex_max(n, k):
        if k == 1:
            return 0.5 * (n + 1)
        if k == 2:
            return ((n << 2) - 1) * (n + 1) / (6 * n)
        if k == 3:
            return (3 * n - 1) * (n + 1) / (n << 2)

        return sum(x * (x**k - (x - 1)**k) for x in range(1, n + 1)) * n**-k

    if k == 0 or n <= 0:
        return 0

    return ex_min(n, -k) if k < 0 else ex_max(n, k)


#variance of max or min of kdn
def var(n, k):
    if k == 0 or n <= 0:
        return 0

    if k == 1:
        return (n * n - 1) / 12
    if k == 2:
        m = n * n
        return (m * ((m << 1) - 1) - 1) / (36 * m)
    if k == 3:
        m = n * n
        return (m * (9 * m - 10) + 1) / (240 * m)

    mu = ex(n, k)
    return sum((x - mu) * (x - mu) * p_eq(n, k, x) for x in range(1, n + 1))


#standard deviation of max or min of kdn
def std(n, k):
    return var(n, k)**.5


#pdf of max or min of kdn
def p_eq(n, k, x):
    def p_eq_min(n_r, k, y):
        return ((y + 1) * n_r)**k - (y * n_r)**k


    def p_eq_max(n_r, k, x):
        return (x * n_r)**k - ((x - 1) * n_r)**k


    if k == 0 or x < 1 or x > n:
        return 0.0

    n_r = 1.0 / n

    return p_eq_min(n_r, -k, n - x) if k < 0 else p_eq_max(n_r, k, x)


#complement of cdf of max or min of kdn
def p_gte(n, k, x, strict=False):
    def p_gte_min(n, k, x):
        return (1.0 - (x - 1) / n)**k


    def p_gte_max(n, k, x):
        return 1.0 - ((x - 1) / n)**k


    if k == 0 or strict and x > n:
        return 0.0

    x = min(max(x, 1), n)

    return p_gte_min(n, -k, x) if k < 0 else p_gte_max(n, k, x)


#complement of cdf of max or min of kdn
def p_gt(n, k, x):
    return p_gte(n, k, x + 1)


#cdf of max or min of kdn
def p_lt(n, k, x):
    return 1.0 - p_gte(n, k, x)


#cdf of max or min of kdn
def p_lte(n, k, x):
    return p_lt(n, k, x + 1)


#success probability of a DC with bonus b
def p_succ(k, dc, b):
    return p_gte(20, k, dc - b, True)


#fail probability of a DC with bonus b
def p_fail(k, dc, b):
    return 1.0 - p_succ(k, dc - b)


#probability of hitting AC with bonus b
def p_hit(k, ac, b):
    return p_gte(20, k, max(ac - b, 2))


#probability of missing AC with bonus b
def p_miss(k, ac, b):
    return 1.0 - p_hit(k, ac, b)


#probability of a critical hit with crit range starting at x
def p_crit(k, x=None):
    return p_gte(20, k, 20) if x is None else p_gte(20, k, x)


if __name__ == '__main__':
    #probability of >= n hits with m ATK rolls using max or min of k d20
    #and ATK bonus b against a target with AC ac
    def p_hitex(ac, b, k=1, m=1, n=1):
        if n > m:
            return 0.0
        return 1.0 - p_miss(k, ac, b)**(m - n + 1)

    #probability of >= n hits with m rays
    #at ATK bonus b against a target with AC ac with Super Advantage max(3d20)
    print(p_hitex(27, 8, 3, 3, 1))

    #probability of >= n hits with m attacks at ATK bonus b against a target
    #with AC ac when the attacker has disadvantage
    print(p_hitex(27, 8, -2, 1, 1))

    #expectation of a d20 as straight roll, advantage and super advantage
    print([ex(20, k) for k in range(1, 4)])

    #expectation of a d20 with disadvantage
    print(ex(20, -2))

    #variance of a d20 as straight roll, advantage and super advantage
    print([var(20, k) for k in range(1, 4)])

    #standard deviation of a d20 as straight roll, advantage and super advantage
    print([std(20, k) for k in range(1, 4)])

    #expected damage for a Figter with 3 attacks at advantage with +1 greatsword
    #and proficiency +4 and STR +5 against a Dire Wolf with AC 14
    print(3 * ((p_hit(2, 14, 5 + 4 + 1) - p_crit(2)) * (2 * ex(6, 1) + 5 + 1) + p_crit(2) * (4 * ex(6, 1) + 5 + 1)))

    #same scenario at disadvantage
    print(3 * ((p_hit(-2, 14, 5 + 4 + 1) - p_crit(-2)) * (2 * ex(6, 1) + 5 + 1) + p_crit(-2) * (4 * ex(6, 1) + 5 + 1)))
