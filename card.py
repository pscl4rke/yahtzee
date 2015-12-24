

class RowAlreadyUsedException(Exception):
    pass


class TotalOf:

    def __init__(self, face):
        self.face = face

    def score(self, hand):
        score = 0
        for die in hand:
            if int(die) == self.face:
                score += self.face
        return score


class AtLeast:

    def __init__(self, required):
        self.required = required

    def score(self, hand):
        for face, count in hand.counts().items():
            if count >= self.required:
                return sum(int(die) for die in hand)
        return 0


class FullHouse:

    def score(self, hand):
        groups = hand.grouped_by_count()
        if (len(groups[2]) == 1) and (len(groups[3]) == 1):
            return 25
        else:
            return 0


def straights_in(ordered_set):
    for i in range(len(ordered_set)):
        yield straight_prefix_of(ordered_set[i:])


def straight_prefix_of(ordered_set):
    prefix = [ordered_set[0]]
    suffix = ordered_set[1:]
    for element in suffix:
        if element != (prefix[-1] + 1):
            break
        else:
            prefix.append(element)
    return prefix


class StraightOf:

    def __init__(self, size, succ):
        self.succ = succ
        self.size = size

    def score(self, hand):
        in_a_row = list(sorted(set(int(die) for die in hand)))
        biggest = max(len(s) for s in straights_in(in_a_row))
        return self.succ if (biggest >= self.size) else 0


class Yahtzee:

    def score(self, hand):
        for die in (hand.d2, hand.d3, hand.d4, hand.d5):
            if int(die) != int(hand.d1):
                return 0
        return 50


class Chance:

    def score(self, hand):
        return sum(int(die) for die in hand)


class Row:

    def __init__(self, id, scorer):
        self.id = id
        self.scorer = scorer
        self.hand = None

    def can_be_used(self):
        return self.hand is None

    def use(self, hand):
        if self.hand is not None:
            raise RowAlreadyUsedException()
        self.hand = hand

    def total(self):
        if self.hand is None:
            return 0
        return self.scorer.score(self.hand)

    def printable_line(self):
        if self.hand is None:
            return "%10s   -" % self.id
        else:
            return "%10s  %2i" % (self.id, self.total())


class Bonus:

    def __init__(self, rows):
        self.id = None
        self.rows = list(rows)

    def can_be_used(self):
        return False

    def use(self, hand):
        raise Exception("Bonus is automatic")

    def total(self):
        subtotal = sum(row.total() for row in self.rows)
        return 0 if (subtotal < 63) else 35

    def printable_line(self):
        if self.total() == 0:
            return "   (bonus)"
        else:
            return "   (bonus)  %2i" % self.total()


class Card:

    def __init__(self):
        self.rows = []
        self.rows.append(Row("total1", TotalOf(1)))
        self.rows.append(Row("total2", TotalOf(2)))
        self.rows.append(Row("total3", TotalOf(3)))
        self.rows.append(Row("total4", TotalOf(4)))
        self.rows.append(Row("total5", TotalOf(5)))
        self.rows.append(Row("total6", TotalOf(6)))
        self.rows.append(Bonus(self.rows))
        self.rows.append(Row("atleast3", AtLeast(3)))
        self.rows.append(Row("atleast4", AtLeast(4)))
        self.rows.append(Row("fullhouse", FullHouse()))
        self.rows.append(Row("short", StraightOf(4, 30)))
        self.rows.append(Row("long", StraightOf(5, 40)))
        self.rows.append(Row("yahtzee", Yahtzee()))
        self.rows.append(Row("chance", Chance()))

    def total(self):
        return sum(row.total() for row in self.rows)

    def has_rows_left(self):
        return any(row.can_be_used() for row in self.rows)

    def available_rows(self):
        return [row for row in self.rows if row.can_be_used()]


