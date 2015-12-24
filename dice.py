

import random


class NoMoreRollsException(Exception):
    pass


class Die:

    def __init__(self):
        self.roll()

    def roll(self):
        self.face = random.choice((1, 2, 3, 4, 5, 6))

    def __repr__(self):
        return "<Die: %i>" % self.face

    def __int__(self):
        return self.face


class Hand:

    def __init__(self):
        self.d1 = Die()
        self.d2 = Die()
        self.d3 = Die()
        self.d4 = Die()
        self.d5 = Die()
        self.rerolls_left = 2

    def reroll(self, roll_d1, roll_d2, roll_d3, roll_d4, roll_d5):
        if self.rerolls_left == 0:
            raise NoMoreRollsException()
        if roll_d1:
            self.d1.roll()
        if roll_d2:
            self.d2.roll()
        if roll_d3:
            self.d3.roll()
        if roll_d4:
            self.d4.roll()
        if roll_d5:
            self.d5.roll()
        self.rerolls_left -= 1

    def __repr__(self):
        return "<Hand %i %i %i %i %i>" % (self.d1, self.d2, self.d3, self.d4, self.d5)

    def __str__(self):
        return "a[%i] b[%i] c[%i] d[%i] e[%i] (Rerolls left: %i)" % (
            self.d1, self.d2, self.d3, self.d4, self.d5, self.rerolls_left,
        )

    def __iter__(self):
        yield self.d1
        yield self.d2
        yield self.d3
        yield self.d4
        yield self.d5

    def counts(self):
        counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        for die in (self.d1, self.d2, self.d3, self.d4, self.d5):
            counts[int(die)] += 1
        return counts

    def grouped_by_count(self):
        groups = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}
        for face, count in self.counts().items():
            groups[count].append(face)
        return groups

    def has_rolls_left(self):
        return self.rerolls_left > 0

    def most_popular_faces(self):
        groups = self.grouped_by_count()
        for count in reversed(sorted(groups.keys())):
            if groups[count] != []:
                return groups[count]


