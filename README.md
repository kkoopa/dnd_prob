# DnD Probability Calculator

Computes probabilities for combinations of n-sided dice.

## Example

```python
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
```
