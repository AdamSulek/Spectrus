def str_checker(inscription):
    '''
        The function recognize the float and integer value and than
            return True

        otherwise
            return False
    '''
    if inscription:
        try:
            float(inscription)
            return True
        except ValueError:
            return False
    else:
        return False

if __name__ == "__main__":
    print(str_checker("adam"))
    print(str_checker('a'))
    print(str_checker("-13.2"))
    print(str_checker(-13.2))
    print(str_checker("5"))
    print(str_checker(0.22))
    print(str_checker(-5))
    print(str_checker(""))
