import sys


def get_max_dig(num):
    res, digval = -1, 0
    for d in num:
        digval = int(d) if d.isdigit() else ord(d.upper()) - ord('A') + 10
        if res < digval:
            res = digval

    return res


def in_numsys_10(num, base):
    res, p = 0, 0
    for c in num[::-1]:
        if c.isdigit():
            dig = int(c)
        else:
            dig = 10 + ord(c.upper()) - ord('A')
        res += dig * (base ** p)
        p += 1
    return res


def from_numsys_10(num, base):
    out = ''
    b = num
    while b > 0:
        a = b % base
        b //= base
        if a > 9:
            out += chr(ord('A') + a - 10)
        else:
            out += str(a)
    return out[::-1]


def check_inp_num_and_sys(s_num, s_sys):
    outs = f'Input data error: {s_num} is not in {s_sys} system'
    if not all([a.isdigit() for a in s_sys]):
        print(f'{s_sys} is incorrect system')
        return False
    for dig in s_num:
        if dig.isdigit():
            if int(dig) >= int(s_sys):
                print(outs)
                return False
        else:
            if ord(dig.upper()) >= ord('A') + int(s_sys) - 10:
                print(outs)
                return False
    return True


def show_help():
    print('На входе: 1) число для преобразования. 2) Система счисления входного числа. 3) В какую систему переводить')


def transform(s_inp, s_ins, s_outs):
    # if not all([c.isdigit for c in s_outs]):
    #     return 'Output system must be a number'
    # if check_inp_num_and_sys(s_inp, s_ins):
        res10 = in_numsys_10(s_inp, int(s_ins))
        res = from_numsys_10(res10, int(s_outs))
        return res
    # return False


if __name__ == '__main__':
    res = ''

    inp_list = sys.argv
    if len(inp_list) != 4:
        show_help()
    else:
        res = transform(inp_list[1], inp_list[2], inp_list[3])
    if res:
        print(res)
    input('Enter to exit')



