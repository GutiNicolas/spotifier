

class StringUtils:

    def none_empty(string):
        print("String is none empty: {}".format(StringUtils.is_empty(string)))
        return not StringUtils.is_empty(string)

    def is_empty(string):
        print("String is None: {}".format(string) is None)
        print("String len is 0: {}".format(len(string) == 0))
        print("String is whitespace only: {}".format(string.isspace()))
        return string is None or len(string) == 0 or string.isspace()