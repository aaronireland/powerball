import unittest
import powerball


class TestEntrant(unittest.TestCase):

    def test_create_entrant_success(self):
        entrant = powerball.Entrant('foo', 'bar')
        self.assertEqual(str(entrant), 'Foo Bar')
        self.assertIsInstance(entrant, powerball.Entrant)

    def test_create_entrant_failure(self):
        with self.assertRaises(TypeError):
            entrant = powerball.Entrant()


class TestTicket(unittest.TestCase):

    def test_create_ticket_success(self):
        entrant = powerball.Entrant('foo', 'bar')
        ticket = powerball.Ticket(entrant)
        self.assertIsInstance(ticket, powerball.Ticket)
        self.assertEqual(ticket.entrant, entrant)
        self.assertEqual(ticket.balls, [])
        self.assertIsNone(ticket.powerball)

    def test_create_ticket_failure(self):
        with self.assertRaises(TypeError):
            ticket = powerball.Ticket()

    def test_complete_ticket(self):
        entrant = powerball.Entrant('foo', 'bar')
        ticket = powerball.Ticket(entrant)
        ticket.add(3)
        ticket.add(69)
        ticket.add(68)
        ticket.add(5)
        ticket.add(15)
        self.assertIsNone(ticket.powerball)
        ticket.add(15)
        self.assertTrue(ticket.is_complete())
        ticket_string = "3, 69, 68, 5, and 15   Powerball: 15"
        self.assertEqual(str(ticket), ticket_string)

    def test_ticket_duplicate_attempt(self):
        entrant = powerball.Entrant('foo', 'bar')
        ticket = powerball.Ticket(entrant)
        ticket.add(3)
        ticket.add(3)
        self.assertIsNone(ticket.powerball)
        self.assertFalse(ticket.is_complete())
        self.assertEqual(len(ticket.balls), 1)

    def test_ticket_out_of_range_attempt(self):
        entrant = powerball.Entrant('foo', 'bar')
        ticket = powerball.Ticket(entrant)
        ticket.add(powerball.MAX_BALL + 1)
        self.assertEqual([], ticket.balls)
        ticket.add(3)
        ticket.add(69)
        ticket.add(68)
        ticket.add(5)
        ticket.add(15)
        ticket.add(powerball.MAX_POWERBALL + 1)
        self.assertIsNone(ticket.powerball)
        self.assertFalse(ticket.is_complete())
        ticket.add(15)
        self.assertTrue(ticket.is_complete())


class TestContest(unittest.TestCase):

    def test_contest_create(self):
        contest = powerball.Contest()
        self.assertIsInstance(contest, powerball.Contest)

    def test_contest_rules(self):
        contest = powerball.Contest()

        employees = [
            ('Aaron', 'Ireland',),
            ('John', 'Smith',),
            ('Sweet', 'Baboo',),
            ('Monty', 'Python',),
            ('Foo', 'Bar')]

        selections = [
            [4, 6, 17, 68, 32, 14],
            [4, 2, 17, 67, 33, 14],
            [4, 8, 17, 66, 34, 1],
            [2, 4, 17, 65, 35, 1],
            [2, 4, 17, 64, 36, 19]]

        for i in range(0, len(employees)):
            first, last = employees[i]
            picks = selections[i]
            ticket = powerball.Ticket(powerball.Entrant(first, last))
            for pick in picks:
                ticket.add(pick)

            self.assertTrue(ticket.is_complete())
            contest.enter(ticket)

        self.assertFalse(contest.winning_ticket.is_complete())
        contest.results()
        self.assertTrue(contest.winning_ticket.is_complete())
        self.assertEqual(contest.winning_ticket.balls[0], 4)
        self.assertFalse(contest.winning_ticket.balls[1] == 4)
        self.assertEqual(contest.winning_ticket.balls[2], 17)
