

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


class RandomPlayer:

    def decide_next_move(self, card, hand):
        possibilities = list(card.available_rows())
        random.shuffle(possibilities)
        return game.UseCommand(possibilities[0].id)

    def finished(self, card):
        pass


def main():
    runner = Runner(RandomPlayer)
    stats = runner.play_a_lot(10000)
    print "The average score was %i" % stats.average()


if __name__ == '__main__':
    main()
