

import sys

import card
import dice


class UserInputException(Exception):
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
        self.need_card_printed = True

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
                    self.need_card_printed = True
        except card.RowAlreadyUsedException:
            raise UserInputException("That row is already used")

    def play_command(self, command):
        if isinstance(command, RerollCommand):
            self.play_reroll(command)
        elif isinstance(command, UseCommand):
            self.play_use(command)
        else:
            raise NotImplementedError(repr(command))

    def play_command_line(self, command_line):
        command = None
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
            command = RerollCommand(*to_reroll)
        for row in self.card.rows:
            if args[0] == row.id:
                command = UseCommand(row.id)
        if command is None:
            raise UserInputException("Invalid Command")
        self.play_command(command)

    def print_state(self, outfile):
        outfile.write("\n")
        for row in self.card.rows:
            #if row.hand is None:
            #    outfile.write("%10s   -\n" % row.id)
            #else:
            #    outfile.write("%10s  %2i\n" % (row.id, row.total()))
            outfile.write("%s\n" % row.printable_line())
        outfile.write("---------------\n")
        outfile.write("    Total: %3i\n" % self.card.total())
        outfile.write("---------------\n")
        #outfile.write("a[%i] b[%i] c[%i] d[%i] e[%i]\n" %
        #    (self.hand.d1, self.hand.d2, self.hand.d3, self.hand.d4, self.hand.d5))
        #outfile.write("You have %i rolls left\n" % self.hand.rerolls_left)
        self.need_card_printed = False

    def play(self):
        outfile = sys.stdout
        while self.card.has_rows_left():
            try:
                if self.need_card_printed:
                    self.print_state(outfile)
                command_line = raw_input("%s Your move? " % self.hand)
                self.play_command_line(command_line)
            except UserInputException as exc:
                outfile.write("Oops! %s\n" % exc)
        self.print_state(outfile)
        outfile.write("Game over! You scored %i\n" % self.card.total())


def main():
    import readline  # magically takes effect
    g = Game()
    g.play()


if __name__ == '__main__':
    main()
