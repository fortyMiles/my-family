import random


def generate_token(string):
    number = int(string)
    length = random.randint(2, 5)
    low = 10 ** (length - 1)
    high = 10 ** length - 1
    random_number = random.randint(low, high)
    print length
    print random_number
    number *= random_number
    result = str(number) + str(random_number) + str(length)
    return result


def check(account, code):
    length = int(code[-1])
    random_number = code[- (1 + length):-1]
    code_phone = code[: -(1 + length)]
    print int(code_phone)/int(random_number) == int(account)


if __name__ == '__main__':
    account = '18857453091'
    code = generate_token(account)
    check(account, code)
