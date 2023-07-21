def new_format(x):
    result = ""
    for i in range(len(x)-1, -1, -1):
        result = x[i] + result
        if (len(x) - i) % 3 == 0 and i != 0:
            result = '.' + result
    return result


assert (new_format("1000000") == "1.000.000")
assert (new_format("100") == "100")
assert (new_format("1000") == "1.000")
assert (new_format("100000") == "100.000")
assert (new_format("10000") == "10.000")
assert (new_format("0") == "0")
