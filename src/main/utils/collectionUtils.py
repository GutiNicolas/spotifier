from collections.abc import Sequence
from src.main.utils.stringUtils import StringUtils


class CollectionUtils:

    def none_empty(coll):
        print("Collection is none empty: {}".format(CollectionUtils.is_empty(coll)))
        return not CollectionUtils.is_empty(coll)

    def is_empty(coll):
        print("Collection is None: {}".format(coll) is None)
        print("Collection len is 0: {}".format(len(coll) == 0))
        return coll is None or len(coll) == 0 or not isinstance(coll, Sequence) or isinstance(coll,
                                                                                              (str, bytes, bytearray))

    def element_to_tuple_by_separator( coll, separator):
        if (CollectionUtils.is_empty(coll)):
            return []

        touples = map(CollectionUtils.split_and_trim, coll, separator)
        return list(filter(None, touples))

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
