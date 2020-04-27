import re
from fuzzywuzzy import fuzz

not_deseable_words = ["Lyrics", "Lyric", "Live at", "Official Video", "Official audio", "/", "()"]

class StringUtils:

    def none_empty(string):
        print("String is none empty: {}".format(not StringUtils.is_empty(string)))
        return not StringUtils.is_empty(string)

    def is_empty(string):
        print("String is None: {}".format(string) is None)
        return string is None or len(string) == 0 or string.isspace()

    def clean_queriable(string):
        print("String before Clean is {}".format(string))
        if(StringUtils.is_empty(string)):
            return None

        not_needed = re.findall(r'\((.*?)\)', string)
        print("Not deseable words found! {}".format(not_needed))

        not_needed = list(map(lambda x: "({})".format(x), not_needed))
        not_deseable_words.extend(not_needed)

        print("Removing {} from {}".format(not_deseable_words, string))
        for word in not_deseable_words:
            string = string.replace(word, "")

        print("Final result is {}".format(string))
        return string

    def similarity_bigger_than_given(string_a, string_b, at_least):
        if StringUtils.is_empty(string_a) and StringUtils.is_empty(string_b):
            return True

        ratio = fuzz.ratio(string_a, string_b)
        return ratio >= at_least
