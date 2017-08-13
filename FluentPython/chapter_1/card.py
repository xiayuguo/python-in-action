

import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for rank in self.ranks
                                        for suit in self.suits]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]


if __name__ == "__main__":
    deck = FrenchDeck()
    print("total is %d" % len(deck))
    print("first is {}".format(deck[0]))
    print("last is {}".format(deck[-1]))
    from random import choice
    print("choice1 is {}".format(choice(deck)))
    print("choice2 is {}".format(choice(deck)))
    print("choice3 is {}".format(choice(deck)))
