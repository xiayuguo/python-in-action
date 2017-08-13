from collections import namedtuple


def game():
    # 元组拆包
    a, b, *rest = range(5)
    print(a, b, rest)

    a, b, *rest = range(2)
    print(a, b, rest)

    a, *body, c, d = range(5)
    print(a, body, c, d)

    *head, b, c, d = range(5)
    print(head, b, c, d)

    # 具名元组 page_26
    City = namedtuple('City', 'name country population coordinates')
    tokyo = City('Tokyo', 'JP', '36.933', (35.689722, 139.691667))
    print(tokyo)
    print("population is %s" % tokyo.population)
    print("coordinates is {}".format(tokyo.coordinates))
    print("index one in tokyo is %s" % tokyo[1])
    print("all fields is {}".format(City._fields))
    LatLong = namedtuple('LatLong', 'lat long')
    delhi_data = ('Delhi NCR', 'IN', 21.935, LatLong(28.613889, 77.208889))
    delhi = City._make(delhi_data)
    print(delhi._asdict())  # collections.OrderedDict


if __name__ == "__main__":
    game()
