def create_one(length: int) -> list:
    one = [1]
    while len(one) < length:
        one = [0] + one
    return one


def binary_inc(bin_num_list: list) -> list:
    one = create_one(len(bin_num_list))
    for j in range(len(one)-1, -1, -1):
        bin_num_list[j] += one[j]
        if bin_num_list[j] == 2:
            bin_num_list[j] = 0
            if j == 0:
                bin_num_list.insert(0, 1)
                return bin_num_list
            else:
                one[j-1] = 1
    return bin_num_list


def points(s: str) -> list:
    if s == '':
        return ['']
    num = 2**(len(s) - 1)
    ans = []
    ibin = [0 for _ in range(len(s)-1)]
    for i in range(num):
        print(ibin)
        s1 = ''
        for j in range(len(s)-1):
            s1 += s[j]
            if ibin[j] == 1:
                s1 += '.'
        s1 += s[-1]
        ans.append(s1)
        ibin = binary_inc(ibin)
    return ans


s = input('')
print(points(s))
