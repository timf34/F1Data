def iterable_practicing():
    for i in range(10):
        yield i

        # This will still work
        if i == 3:
            break


def use_iterable():
    for i in iterable_practicing():
        print(i)


def main():
    use_iterable()


if __name__ == '__main__':
    main()
