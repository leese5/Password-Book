import random


def create_database():

    num_list, low_alphabet, up_alphabet = [], list(), list()

    # build 1~10 numbers
    for i in range(1, 10):
        num_list.append(str(i))
    # build a~z chars
    for ascii_val in range(ord('a'), ord('z')+1):
        low_alphabet.append(chr(ascii_val))
    # build A~Z chars
    for char in low_alphabet:
        up_alphabet.append(char.capitalize())

    return num_list + low_alphabet + up_alphabet


def random_60():
    # generate a random int num between 0 to 60
    # 26 low + 26 up + 9 num = 61 total char
    # index is between 0 to 60

    return random.randint(0, 60)


def random_15():
    # generate a number between 10 to 15 for password length

    return random.randint(10, 15)


def build_password():
    database, pw = create_database(), ""

    for i in range(random_15()):
        rand_char = database[random_60()]
        pw += rand_char

    return pw


def send_pw():
    pw = build_password()
    f = open('com.txt', 'w')
    f.write(f"{pw}")
    f.close()


def receive_pw():
    f = open('com.txt', 'r')
    line = f.readline()
    f.close()

    return line


if __name__ == "__main__":
    send_pw()
    print(receive_pw())
