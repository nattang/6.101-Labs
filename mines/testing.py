

def cube_root(value):
    n = 1
    min = value
    while n < value:
        cube = n**3
        if cube< value:
            if value - cube < min:
                min = value - cube
                res = n
        elif value < cube:
            if cube - value < min:
                min = cube - value
                res = n
            else:
                return res
                break
        n += 1
    return res

print(cube_root(14123123120))