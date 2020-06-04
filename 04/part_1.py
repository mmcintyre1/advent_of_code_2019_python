password_range = range(197487, 673252)


def password_check(pw):
    prev = ""
    double_check = False
    ascending = True

    for c in str(pw):
        if c == prev:
            double_check = True

        if prev:
            if int(c) < int(prev):
                ascending = False
        prev = c

    return double_check and ascending


if __name__ == '__main__':
    print(sum(1 for x in password_range if password_check(x)))
