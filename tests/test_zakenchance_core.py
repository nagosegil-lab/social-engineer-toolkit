import random
import unittest

from zakenchance_core import (
    ALL_LOTTO_NUMBERS,
    CHANCE_CARDS,
    CHANCE_SUITS,
    generate_multi_chance_tickets,
    generate_multi_tickets,
    parse_chance_history,
    parse_lotto_history,
    ticket_score_details,
)


class ZakenChanceCoreTests(unittest.TestCase):
    def test_parse_lotto_history_valid_and_invalid_rows(self):
        raw = "\n".join(
            [
                "1,7,19,22,27,34 | 5",
                "1,1,2,3,4,5 | 2",
                "3,10,16,24,31,37 | 9",
                "a,10,11,12,13,14 | 3",
                "3,10,16,24,31,37 | 2",
            ]
        )

        lotto_numbers, strong_numbers, invalid_rows = parse_lotto_history(raw)

        self.assertEqual(len(lotto_numbers), 12)
        self.assertEqual(strong_numbers, [5, 2])
        self.assertEqual(len(invalid_rows), 3)

    def test_ticket_score_details_reports_penalties(self):
        details = ticket_score_details([1, 2, 3, 4, 5, 6])

        self.assertEqual(details["evens"], 3)
        self.assertEqual(details["lows"], 6)
        self.assertEqual(details["total"], 21)
        self.assertEqual(details["adjacent_pairs"], 5)
        self.assertEqual(details["score"], 40)
        self.assertEqual(len(details["penalties"]), 3)

    def test_generate_multi_tickets_returns_unique_sized_tickets(self):
        rng = random.Random(123)

        tickets = generate_multi_tickets(
            amount=5,
            mode="Random",
            lotto_numbers=[],
            all_numbers=ALL_LOTTO_NUMBERS,
            rng=rng,
        )

        self.assertEqual(len(tickets), 5)
        self.assertEqual(len({tuple(ticket) for ticket in tickets}), 5)
        for ticket in tickets:
            self.assertEqual(len(ticket), 6)
            self.assertEqual(ticket, sorted(ticket))

    def test_parse_chance_history_validates_rows(self):
        raw = "\n".join(
            [
                "10,K,8,J",
                "7,10,Q,A",
                "1,2,3,4",
                "7,8,9",
            ]
        )

        draws, invalid_rows = parse_chance_history(raw, cards=CHANCE_CARDS, suits=CHANCE_SUITS)

        self.assertEqual(len(draws), 2)
        self.assertEqual(draws[0]["תלתן"], "10")
        self.assertEqual(len(invalid_rows), 2)

    def test_generate_multi_chance_tickets_returns_expected_amount(self):
        rng = random.Random(321)
        chance_draws, _ = parse_chance_history(
            "10,K,8,J\n7,10,Q,A",
            cards=CHANCE_CARDS,
            suits=CHANCE_SUITS,
        )

        tickets = generate_multi_chance_tickets(
            amount=6,
            mode="History Weighted",
            chance_draws=chance_draws,
            cards=CHANCE_CARDS,
            suits=CHANCE_SUITS,
            rng=rng,
        )

        self.assertEqual(len(tickets), 6)
        for ticket in tickets:
            self.assertEqual(set(ticket.keys()), set(CHANCE_SUITS))
            for card in ticket.values():
                self.assertIn(card, CHANCE_CARDS)


if __name__ == "__main__":
    unittest.main()
