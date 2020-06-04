password_range = range(197487, 673251)


def password_check_2(pw):
    prev = ""
    ascending = True
    double_check = False
    repeats = 0

    for c in str(pw):
        if c == prev:
            repeats += 1
        else:
            if repeats == 1:
                double_check = True
            repeats = 0

        if prev:
            if int(c) < int(prev):
                ascending = False

        prev = c

    # handle numbers that end on duplicate
    if repeats == 1:
        double_check = True

    return ascending and double_check


if __name__ == '__main__':
    print(sum(1 for x in password_range if password_check_2(x)))
