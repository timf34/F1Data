def iterable_practicing():
    for i in range(5):
        yield i


def use_iterable():
    for i in iterable_practicing():
        print(i)


def main():
    use_iterable()


if __name__ == '__main__':
    main()
