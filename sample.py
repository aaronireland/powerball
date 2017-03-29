import powerball

contest = powerball.Contest()


def process_ticket(ticket):
    while(not ticket.is_complete()):
        if len(ticket.balls) < powerball.BALLS_TO_PLAY:
            base_message = "1 thru {}".format(powerball.MAX_BALL)
            if len(ticket.balls) == 0:
                ordinal = "1st"
                message = base_message
            elif len(ticket.balls) == 1:
                ordinal = "2nd"
                message = "{} excluding {}".format(base_message, str(ticket))
            else:
                ordinal = "{}th".format(len(ticket.balls) + 1)
                message = "{} excluding {}".format(base_message, str(ticket))
        else:
            message = "1 thru {}".format(powerball.MAX_POWERBALL)
            ordinal = "Power Ball"
        try:
            prompt = "select {} # ({}): ".format(ordinal, message)
            selection = input(prompt)
            if selection == "":
                break
            ticket.add(selection)
        except:
            continue
    return ticket


def main():
    while(True):
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        if first_name == "" or last_name == "":
            break

        entrant = powerball.Entrant(first_name, last_name)
        ticket = process_ticket(powerball.Ticket(entrant))
        contest.enter(ticket)
    contest.results()

if __name__ == "__main__":
    main()
