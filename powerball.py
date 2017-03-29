import random
from collections import Counter

BALLS_TO_PLAY = 5
POWERBALL = BALLS_TO_PLAY + 1
MAX_BALL = 69
MAX_POWERBALL = 26


class Entrant(object):
    def __init__(self, first, last):
        self.first_name = first
        self.last_name = last

    def __str__(self):
        return "{} {}".format(
            self.first_name.capitalize(),
            self.last_name.capitalize())


class Ticket(object):
    def __init__(self, entrant):
        self.entrant = entrant
        self.balls = []
        self.powerball = None

    def add(self, number):
        try:
            number = int(number)
        except:
            return
        if len(self.balls) < BALLS_TO_PLAY:
            if number <= MAX_BALL and number not in self.balls:
                self.balls.append(number)
        elif number <= MAX_POWERBALL:
            self.powerball = number

    def is_complete(self):
        return len(self.balls) == BALLS_TO_PLAY and \
            len(set(self.balls)) == BALLS_TO_PLAY and \
            self.powerball is not None

    def __str__(self):
        if self.balls:
            ticket = ", ".join(str(ball) for ball in self.balls)

            # inject 'and' after last comma
            if "," in ticket:
                last_comma = ticket.rfind(", ") + 2
                ticket = "{}and {}".format(
                    ticket[:last_comma],
                    ticket[last_comma:])

            if self.powerball:
                ticket = "{:<22} Powerball: {}".format(ticket, self.powerball)
            return ticket
        else:
            return "Empty Ticket"


class Contest(object):
    def __init__(self):
        self.entries = []
        self.winning_ticket = Ticket(Entrant('Winning', 'Number'))

    def winning_number(self, ix):
        if ix < BALLS_TO_PLAY:
            selected = [ticket.balls[ix] for ticket in self.entries]
            random_selection = random.randint(1, MAX_BALL)
        else:
            selected = [ticket.powerball for ticket in self.entries]
            random_selection = random.randint(1, MAX_POWERBALL)

        if len(selected) == 1:
            return selected[0]  # Only one entry was rec'd
        else:
            mode, freq = Counter(selected).most_common(1)[0]
            if freq == 1:
                return random_selection  # No duplicate numbers
            else:
                try:
                    # Select the frequency of the 2nd element from 2 most common
                    next_freq = Counter(selected).most_common(2)[1][1]
                    # if there was a tie return a random selection.
                    if freq > next_freq:
                        return mode
                    else:
                        return random_selection
                except IndexError:
                    # If everyone selected the same number:
                    return mode

    def enter(self, entry):
        if isinstance(entry, Ticket):
            if entry.is_complete():
                self.entries.append(entry)
                # reset winning_ticket
                self.winning_ticket = Ticket(Entrant('Winning', 'Number'))

    def results(self):
        if self.entries and not self.winning_ticket.is_complete():
            for ball in range(0, BALLS_TO_PLAY):
                number = self.winning_number(ball)
                # If the most common selection is a previously selected winning ball?
                while(number in [ball for ball in self.winning_ticket.balls]):
                    number = random.randint(1, MAX_BALL)
                self.winning_ticket.add(number)
            self.winning_ticket.add(self.winning_number(POWERBALL))
        print(self)

    def __str__(self):
        msg = ["Powerball Contest"]
        if self.entries:
            msg.append("-" * 30 + "|" + "-" * 36)
            for ticket in self.entries:
                msg.append("{:<30}| {}".format(str(ticket.entrant), ticket))
            if self.winning_ticket.is_complete():
                msg.append("\n~~~ POWERBALL WINNING NUMBER ~~~")
                msg.append(self.winning_ticket)
        return "\n".join(str(line) for line in msg)
