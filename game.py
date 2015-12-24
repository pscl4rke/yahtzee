

import card
import dice


class UserInputException(Exception):
    pass


class NoopCommand:
    pass


class RerollCommand:

    def __init__(self, d1, d2, d3, d4, d5):
        self.d1 = d1
        self.d2 = d2
        self.d3 = d3
        self.d4 = d4
        self.d5 = d5


class UseCommand:

    def __init__(self, row_id):
        self.row_id = row_id


class Game:

    def __init__(self):
        self.card = card.Card()
        self.hand = dice.Hand()

    def play_reroll(self, cmd):
        try:
            self.hand.reroll(cmd.d1, cmd.d2, cmd.d3, cmd.d4, cmd.d5)
        except dice.NoMoreRollsException:
            raise UserInputException("No more rolls left")

    def play_use(self, command):
        try:
            for row in self.card.rows:
                if row.id == command.row_id:
                    row.use(self.hand)
                    self.hand = dice.Hand()
        except card.RowAlreadyUsedException:
            raise UserInputException("That row is already used")

    def play_command(self, command):
        if isinstance(command, RerollCommand):
            self.play_reroll(command)
        elif isinstance(command, UseCommand):
            self.play_use(command)
        elif isinstance(command, NoopCommand):
            pass
        else:
            raise NotImplementedError(repr(command))

    def play(self, player):
        while self.card.has_rows_left():
            command = player.decide_next_move(self.card, self.hand)
            self.play_command(command)
        player.finished(self.card)


class InteractivePlayer:

    def __init__(self):
        self.need_card_printed = True

    def print_card(self, card):
        print
        for row in card.rows:
            print "%s" % row.printable_line()
        print "---------------"
        print "    Total: %3i" % card.total()
        print "---------------"
        self.need_card_printed = False

    def parse_command_line(self, command_line, card):
        args = command_line.split()
        if len(args) < 1:
            raise UserInputException("Invalid Command")
        if args[0] == "roll":
            requested = args[1:]
            to_reroll = [False, False, False, False, False]
            if 'a' in requested:
                to_reroll[0] = True
            if 'b' in requested:
                to_reroll[1] = True
            if 'c' in requested:
                to_reroll[2] = True
            if 'd' in requested:
                to_reroll[3] = True
            if 'e' in requested:
                to_reroll[4] = True
            if True not in to_reroll:
                raise UserInputException("Must reroll something")
            return RerollCommand(*to_reroll)
        for row in card.rows:
            if args[0] == row.id:
                return UseCommand(row.id)
        raise UserInputException("Invalid Command: %s" % args[0])

    def decide_next_move(self, card, hand):
        try:
            if self.need_card_printed:
                self.print_card(card)
            command_line = raw_input("%s Your move? " % hand)
            command = self.parse_command_line(command_line, card)
            if isinstance(command, UseCommand):
                self.need_card_printed = True
            return command
        except UserInputException as exc:
            print "Oops! %s" % exc
            return NoopCommand()

    def finished(self, card):
        self.print_card(card)
        print "Game over! You scored %i" % card.total()


def main():
    import readline  # magically takes effect
    g = Game()
    p = InteractivePlayer()
    g.play(p)


if __name__ == '__main__':
    main()
