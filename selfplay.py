

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

    def handle_user_input_error(self, exc):
        raise exc

    def finished(self, card):
        pass


    def best_scoring_row(self, card, hand):
        possibilities = [
            (row.scorer.score(hand), row)
            for row in card.available_rows() ]
        possibilities.sort()
        return possibilities[-1][1]


class RandomPlayer(BasePlayer):

    def decide_next_move(self, card, hand):
        possibilities = list(card.available_rows())
        random.shuffle(possibilities)
        return game.UseCommand(possibilities[0].id)


class GrabMaxPlayer(BasePlayer):

    def decide_next_move(self, card, hand):
        return game.UseCommand(self.best_scoring_row(card, hand).id)


class RollThenGrabPlayer(BasePlayer):

    def decide_next_move(self, card, hand):
        if hand.has_rolls_left():
            return game.RerollNotCommand(hand.most_popular_faces()[0], hand)
        else:
            return game.UseCommand(self.best_scoring_row(card, hand).id)


class CheckBeforeRollPlayer(BasePlayer):

    def decide_next_move(self, card, hand):
        for row_id in ("fullhouse", "long", "short"):
            if card.row_by_id(row_id).can_be_used():
                if card.row_by_id(row_id).scorer.score(hand) > 0:
                    return game.UseCommand(row_id)
        if hand.has_rolls_left():
            return game.RerollNotCommand(hand.most_popular_faces()[0], hand)
        return game.UseCommand(self.best_scoring_row(card, hand).id)


class BeatingLastAverages(BasePlayer):

    def decide_next_move(self, card, hand):
        averages = {
            "total1": 2,
            "total2": 4,
            "total3": 6,
            "total4": 7,
            "total5": 8,
            "total6": 9,
            "atleast3": 16,
            "atleast4": 15,
            "fullhouse": 23,
            "short": 27,
            "long": 12,
            "yahtzee": 19,
            "chance": 16,
        }
        for row_id in ("fullhouse", "long", "short"):
            if card.row_by_id(row_id).can_be_used():
                if card.row_by_id(row_id).scorer.score(hand) > 0:
                    return game.UseCommand(row_id)
        if hand.has_rolls_left():
            return game.RerollNotCommand(hand.most_popular_faces()[0], hand)
        possibilities = [
            (row.scorer.score(hand) - averages[row.id], row)
            for row in card.available_rows() ]
        possibilities.sort()
        return game.UseCommand(possibilities[-1][1].id)


def main():
    players_to_try = [
        RandomPlayer,
        GrabMaxPlayer,
        RollThenGrabPlayer,
        CheckBeforeRollPlayer,
        BeatingLastAverages,
    ]
    for player_class in players_to_try:
        runner = Runner(player_class)
        stats = runner.play_a_lot(10000)
        print "%s: The average score was %i" % (player_class.__name__, stats.average())


if __name__ == '__main__':
    main()
