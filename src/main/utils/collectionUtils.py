from collections.abc import Sequence
from src.main.utils.stringUtils import StringUtils

class CollectionUtils:

    def none_empty(coll):
        print("Collection is none empty: {}".format(not CollectionUtils.is_empty(coll)))
        return not CollectionUtils.is_empty(coll)

    def is_empty(coll):
        print("Collection is None: {}".format(coll is None))
        return coll is None or len(coll) == 0 or not isinstance(coll, Sequence) or isinstance(coll,
                                                                                              (str, bytes, bytearray))

    def element_to_tuple_by_separator(coll, separator):
        if (CollectionUtils.is_empty(coll)):
            return []

        res = list(map(lambda x: CollectionUtils.split_and_trim(x, separator), coll))
        print("TOUPLES are {}".format(res))
        return list(filter(lambda x: x is not None , res))


    def split_and_trim(s, sep):
        splitted = str(s).split(str(sep))
        print(splitted)
        if (CollectionUtils.is_empty(splitted)):
            return None
        artist = splitted[0]
        song = splitted[1]
        if (StringUtils.is_empty(artist) or StringUtils.is_empty(song)):
            return None
        return str(artist).strip(), str(song).strip()
