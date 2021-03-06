
# Thanks to Amir Ziai
# https://towardsdatascience.com/flattening-json-objects-in-python-f5343c794b10


def flatten_json(y, delim='.'):
    """Flatten a nested JSON document using delimited key names
    """
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + delim)
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + delim)
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out
