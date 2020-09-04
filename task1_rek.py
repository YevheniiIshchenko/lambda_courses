import time


def points(s: str) -> list:
    if s == '':
        return ['']

    num = 2**(len(s) - 1)
    ans = []

    for i in range(num):
        s1 = ''

        for j in range(len(s)):
            s1 += s[j]
            if (i >> j) & 1 == 1:
                s1 += '.'
        ans.append(s1)
    return ans


def points_rek(s: str) -> list:
    if s == '':
        return ['']
    n = len(s)-1
    ans = []

    def rek1(i, s1):
        if i < n:
            s1 += s[i]
            i += 1
        if i == n:
            s1 += s[n]
            ans.append(s1)
            return

        rek1(i, s1)
        rek2(i, s1)

    def rek2(i, s1):
        if i < n:
            s1 += s[i] + '.'
            i += 1
        if i == n:
            s1 += s[n]
            ans.append(s1)
            return

        rek1(i, s1)
        rek2(i, s1)

    rek1(0, '')
    rek2(0, '')

    return ans


n = 10
s = input('')
print(points(s))
print(points_rek(s))

full = 0

for _ in range(n):
    start = time.time()
    points_rek(s)
    end = time.time()
    full += (end - start)
print('Average ex. time (recursion) = ', full/n)
for _ in range(n):
    start = time.time()
    points(s)
    end = time.time()
    full += (end - start)
print('Average ex. time (w/ recursion) = ', full/n)
