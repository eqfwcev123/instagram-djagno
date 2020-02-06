# __name__ 이해하기
def myfunction():
    print('The value of __name__ is ' + __name__)


def main():
    myfunction()


if __name__ == '__main__':
    main()
else:
    print('name of the file is ', __name__)