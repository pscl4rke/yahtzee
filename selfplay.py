

import random

import game


class Stats:

    def __init__(self):
        self._count = 0
        self._total = 0

    def add_datapoint(self, datapoint):
        self._count += 1
        self._total += datapoint

    def average(self):
        return self._total / self._count


class Runner:

    def __init__(self, player_class):
        self.player_class = player_class

    def play_a_lot(self, count):
        stats = Stats()
        for i in range(count):
            player = self.player_class()
            this_game = game.Game()
            this_game.play(player)
            stats.add_datapoint(this_game.card.total())
        return stats


class BasePlayer:

    def finished(self, card):
        pass


class RandomPlayer(BasePlayer):

    def decide_next_move(self, card, hand):
        possibilities = list(card.available_rows())
        random.shuffle(possibilities)
        return game.UseCommand(possibilities[0].id)


class GrabMaxPlayer(BasePlayer):

    def decide_next_move(self, card, hand):
        possibilities = [
            (row.scorer.score(hand), row)
            for row in card.available_rows() ]
        possibilities.sort()
        best_scoring_row = possibilities[-1][1]
        return game.UseCommand(best_scoring_row.id)


class RollThenGrab(BasePlayer):

    def decide_next_move(self, card, hand):
        if hand.has_rolls_left():
            return game.RerollNotCommand(hand.most_popular_faces()[0], hand)
        else:
            possibilities = [
                (row.scorer.score(hand), row)
                for row in card.available_rows() ]
            possibilities.sort()
            best_scoring_row = possibilities[-1][1]
            return game.UseCommand(best_scoring_row.id)


def main():
    players_to_try = [
        RandomPlayer,
        GrabMaxPlayer,
        RollThenGrab,
    ]
    for player_class in players_to_try:
        runner = Runner(player_class)
        stats = runner.play_a_lot(10000)
        print "%s: The average score was %i" % (player_class.__name__, stats.average())


if __name__ == '__main__':
    main()
