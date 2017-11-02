def isprime(n):
    if n < 2: return False
    if n % 2 == 0: return n == 2
    k = 3
    while k*k <= n:
         if n % k == 0: return False
         k += 2
    return True

rulers = []
ruler = []
d = set()
n = 0
while len(ruler) <= 10:
    order = len(ruler) + 1
    if order > 2 and isprime(order):
        ruler = [2*order*k + k*k%order for k in range(order)]
        d = {a-b for a in ruler for b in ruler if a > b}
        n = max(ruler) + 1
        rulers.append(tuple(ruler))
        continue

    nd = set(n-e for e in ruler)
    if not d & nd:
        ruler.append(n)
        d |= nd
        rulers.append(tuple(ruler))
    n += 1

print ruler

isuniq = lambda l: len(l) == len(set(l))
isruler = lambda l: isuniq([a-b for a in l for b in l if a > b])

assert all(isruler(r) for r in rulers)

rulers = list(sorted([r for r in rulers if 50 <= len(r) <= 100], key=len))
print(sum(max(r) for r in rulers))
