
def rowproxy_to_dictlist(row):
    d, l = {}, []
    for rowproxy in row:
        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for tup in rowproxy.items():
            # build up the dictionary
            d = {**d, **{tup[0]: tup[1]}}
        l.append(d)
    return l