"""Core helper functions for the ZakenChance Streamlit app."""

from __future__ import annotations

import random
from collections import Counter

LOTTO_MIN = 1
LOTTO_MAX = 37
LOTTO_PICK_COUNT = 6
STRONG_MIN = 1
STRONG_MAX = 7

ALL_LOTTO_NUMBERS = list(range(LOTTO_MIN, LOTTO_MAX + 1))
ALL_STRONG_NUMBERS = list(range(STRONG_MIN, STRONG_MAX + 1))

CHANCE_CARDS = ["7", "8", "9", "10", "J", "Q", "K", "A"]
CHANCE_SUITS = ["תלתן", "יהלום", "לב", "עלה"]
HIGH_CARDS = {"J", "Q", "K", "A"}


def parse_lotto_history(
    text: str,
    lotto_min: int = LOTTO_MIN,
    lotto_max: int = LOTTO_MAX,
    strong_min: int = STRONG_MIN,
    strong_max: int = STRONG_MAX,
    pick_count: int = LOTTO_PICK_COUNT,
):
    """Parse lotto text history and return numbers, strong numbers and row errors."""
    lotto_numbers = []
    strong_numbers = []
    invalid_rows = []

    for index, line in enumerate(text.splitlines(), start=1):
        cleaned = line.strip()
        if not cleaned:
            continue

        parts = cleaned.split("|", 1)
        if len(parts) != 2:
            invalid_rows.append(f"שורה {index}: פורמט לא תקין (נדרש '|').")
            continue

        nums_part, strong_part = parts
        num_tokens = [token.strip() for token in nums_part.split(",")]

        try:
            nums = [int(token) for token in num_tokens]
            strong = int(strong_part.strip())
        except ValueError:
            invalid_rows.append(f"שורה {index}: ערכים חייבים להיות מספרים.")
            continue

        if len(nums) != pick_count:
            invalid_rows.append(
                f"שורה {index}: נדרשים בדיוק {pick_count} מספרים בלוטו."
            )
            continue

        if len(set(nums)) != pick_count:
            invalid_rows.append(f"שורה {index}: המספרים בלוטו חייבים להיות ייחודיים.")
            continue

        if any(number < lotto_min or number > lotto_max for number in nums):
            invalid_rows.append(
                f"שורה {index}: מספרי לוטו חייבים להיות בטווח {lotto_min}-{lotto_max}."
            )
            continue

        if strong < strong_min or strong > strong_max:
            invalid_rows.append(
                f"שורה {index}: מספר חזק חייב להיות בטווח {strong_min}-{strong_max}."
            )
            continue

        lotto_numbers.extend(nums)
        strong_numbers.append(strong)

    return lotto_numbers, strong_numbers, invalid_rows


def parse_chance_history(
    text: str,
    cards: list[str] | None = None,
    suits: list[str] | None = None,
):
    """Parse chance text history and return draws + row errors."""
    cards = cards or CHANCE_CARDS
    suits = suits or CHANCE_SUITS
    valid_cards = {card.upper() for card in cards}

    chance_draws = []
    invalid_rows = []

    for index, line in enumerate(text.splitlines(), start=1):
        cleaned = line.strip()
        if not cleaned:
            continue

        tokens = [token.strip().upper() for token in cleaned.split(",")]
        if len(tokens) != len(suits):
            invalid_rows.append(
                f"שורה {index}: נדרשים בדיוק {len(suits)} קלפים לפי סדר הסמלים."
            )
            continue

        if any(token not in valid_cards for token in tokens):
            invalid_rows.append(
                f"שורה {index}: נמצאו קלפים לא חוקיים. אפשריים: {', '.join(cards)}."
            )
            continue

        chance_draws.append(dict(zip(suits, tokens)))

    return chance_draws, invalid_rows


def ticket_score_details(ticket: list[int]):
    """Return ticket metrics, penalties and final score."""
    sorted_ticket = sorted(ticket)
    evens = sum(1 for number in sorted_ticket if number % 2 == 0)
    lows = sum(1 for number in sorted_ticket if number <= 18)
    total = sum(sorted_ticket)
    adjacent = sum(
        1
        for idx in range(len(sorted_ticket) - 1)
        if sorted_ticket[idx + 1] - sorted_ticket[idx] == 1
    )

    penalties = []
    score = 100

    if evens not in {2, 3, 4}:
        penalties.append(("איזון זוגי/אי-זוגי חלש", 20))
        score -= 20
    if lows not in {2, 3, 4}:
        penalties.append(("יותר מדי נמוכים/גבוהים", 20))
        score -= 20
    if total < 90 or total > 150:
        penalties.append(("סכום מחוץ לטווח 90-150", 20))
        score -= 20
    if adjacent > 1:
        penalties.append(("יותר מרצף אחד של מספרים עוקבים", 20))
        score -= 20

    return {
        "score": max(0, score),
        "evens": evens,
        "lows": lows,
        "total": total,
        "adjacent_pairs": adjacent,
        "penalties": penalties,
    }


def is_anti_crowd(ticket: list[int]):
    common_human_numbers = {1, 2, 3, 4, 5, 7, 10, 11, 13, 18, 21, 22, 26, 30, 31}
    birthday_count = sum(1 for number in ticket if number <= 31)
    common_count = sum(1 for number in ticket if number in common_human_numbers)
    return birthday_count <= 4 and common_count <= 2


def generate_balanced_ticket(
    all_numbers: list[int] | None = None,
    iterations: int = 500,
    rng: random.Random | None = None,
):
    all_numbers = all_numbers or ALL_LOTTO_NUMBERS
    rng = rng or random.Random()

    best_ticket = sorted(rng.sample(all_numbers, LOTTO_PICK_COUNT))
    best_score = -1

    for _ in range(iterations):
        candidate = sorted(rng.sample(all_numbers, LOTTO_PICK_COUNT))
        details = ticket_score_details(candidate)
        candidate_score = details["score"] + (15 if is_anti_crowd(candidate) else 0)

        if candidate_score > best_score:
            best_score = candidate_score
            best_ticket = candidate

    return best_ticket


def generate_hot_cold_ticket(
    lotto_numbers: list[int],
    all_numbers: list[int] | None = None,
    rng: random.Random | None = None,
):
    all_numbers = all_numbers or ALL_LOTTO_NUMBERS
    rng = rng or random.Random()

    if not lotto_numbers:
        return generate_balanced_ticket(all_numbers=all_numbers, rng=rng)

    counts = Counter(lotto_numbers)
    hot_numbers = [number for number, _ in counts.most_common(12)]
    cold_numbers = sorted(all_numbers, key=lambda value: counts[value])[:12]

    ticket = set()
    ticket.update(rng.sample(hot_numbers, min(3, len(hot_numbers))))
    ticket.update(rng.sample(cold_numbers, min(2, len(cold_numbers))))

    while len(ticket) < LOTTO_PICK_COUNT:
        ticket.add(rng.choice(all_numbers))

    return sorted(ticket)


def generate_multi_tickets(
    amount: int,
    mode: str,
    lotto_numbers: list[int],
    all_numbers: list[int] | None = None,
    rng: random.Random | None = None,
):
    all_numbers = all_numbers or ALL_LOTTO_NUMBERS
    rng = rng or random.Random()
    tickets = set()
    attempts = 0

    while len(tickets) < amount and attempts < amount * 1000:
        attempts += 1

        if mode == "Balanced Distribution":
            ticket = generate_balanced_ticket(all_numbers=all_numbers, rng=rng)
        elif mode == "Hot + Cold Mix":
            ticket = generate_hot_cold_ticket(
                lotto_numbers=lotto_numbers,
                all_numbers=all_numbers,
                rng=rng,
            )
        elif mode == "Anti-Crowd Mode":
            ticket = generate_balanced_ticket(all_numbers=all_numbers, rng=rng)
            if not is_anti_crowd(ticket):
                continue
        else:
            ticket = sorted(rng.sample(all_numbers, LOTTO_PICK_COUNT))

        tickets.add(tuple(ticket))

    return [list(ticket) for ticket in sorted(tickets)]


def choose_strong(
    strong_numbers: list[int],
    strong_min: int = STRONG_MIN,
    strong_max: int = STRONG_MAX,
    rng: random.Random | None = None,
):
    rng = rng or random.Random()
    if strong_numbers:
        counts = Counter(strong_numbers)
        return counts.most_common(1)[0][0]
    return rng.randint(strong_min, strong_max)


def chance_suit_counters(chance_draws: list[dict[str, str]], suits: list[str] | None = None):
    suits = suits or CHANCE_SUITS
    return {
        suit: Counter(draw[suit] for draw in chance_draws if suit in draw)
        for suit in suits
    }


def generate_balanced_chance_ticket(
    cards: list[str] | None = None,
    suits: list[str] | None = None,
    rng: random.Random | None = None,
):
    cards = cards or CHANCE_CARDS
    suits = suits or CHANCE_SUITS
    rng = rng or random.Random()

    for _ in range(200):
        pick = {suit: rng.choice(cards) for suit in suits}
        values = list(pick.values())
        has_high = any(value in HIGH_CARDS for value in values)
        has_low = any(value not in HIGH_CARDS for value in values)
        if len(set(values)) >= 3 and has_high and has_low:
            return pick

    return {suit: rng.choice(cards) for suit in suits}


def generate_hot_cold_chance_ticket(
    chance_draws: list[dict[str, str]],
    cards: list[str] | None = None,
    suits: list[str] | None = None,
    rng: random.Random | None = None,
):
    cards = cards or CHANCE_CARDS
    suits = suits or CHANCE_SUITS
    rng = rng or random.Random()

    if not chance_draws:
        return generate_balanced_chance_ticket(cards=cards, suits=suits, rng=rng)

    counters = chance_suit_counters(chance_draws, suits=suits)
    ticket = {}

    for suit in suits:
        suit_counter = counters[suit]
        hot_cards = [card for card, _ in suit_counter.most_common(3)]
        cold_cards = sorted(cards, key=lambda card: suit_counter[card])[:3]
        strategy = rng.choices(
            ["hot", "cold", "random"],
            weights=[4, 3, 2],
            k=1,
        )[0]

        if strategy == "hot" and hot_cards:
            ticket[suit] = rng.choice(hot_cards)
        elif strategy == "cold" and cold_cards:
            ticket[suit] = rng.choice(cold_cards)
        else:
            ticket[suit] = rng.choice(cards)

    return ticket


def generate_history_weighted_chance_ticket(
    chance_draws: list[dict[str, str]],
    cards: list[str] | None = None,
    suits: list[str] | None = None,
    rng: random.Random | None = None,
):
    cards = cards or CHANCE_CARDS
    suits = suits or CHANCE_SUITS
    rng = rng or random.Random()

    if not chance_draws:
        return generate_balanced_chance_ticket(cards=cards, suits=suits, rng=rng)

    counters = chance_suit_counters(chance_draws, suits=suits)
    ticket = {}
    for suit in suits:
        weights = [counters[suit][card] + 1 for card in cards]
        ticket[suit] = rng.choices(cards, weights=weights, k=1)[0]
    return ticket


def generate_multi_chance_tickets(
    amount: int,
    mode: str,
    chance_draws: list[dict[str, str]],
    cards: list[str] | None = None,
    suits: list[str] | None = None,
    rng: random.Random | None = None,
):
    cards = cards or CHANCE_CARDS
    suits = suits or CHANCE_SUITS
    rng = rng or random.Random()

    tickets = set()
    attempts = 0
    max_attempts = amount * 1000

    while len(tickets) < amount and attempts < max_attempts:
        attempts += 1

        if mode == "Balanced Distribution":
            ticket = generate_balanced_chance_ticket(cards=cards, suits=suits, rng=rng)
        elif mode == "Hot + Cold Mix":
            ticket = generate_hot_cold_chance_ticket(
                chance_draws=chance_draws,
                cards=cards,
                suits=suits,
                rng=rng,
            )
        elif mode == "History Weighted":
            ticket = generate_history_weighted_chance_ticket(
                chance_draws=chance_draws,
                cards=cards,
                suits=suits,
                rng=rng,
            )
        else:
            ticket = {suit: rng.choice(cards) for suit in suits}

        encoded = tuple(ticket[suit] for suit in suits)
        tickets.add(encoded)

    return [{suit: values[idx] for idx, suit in enumerate(suits)} for values in sorted(tickets)]
