import streamlit as st
import random
from collections import Counter

st.set_page_config(page_title="ZakenChance AI", layout="centered")

st.title("🎲 ZakenChance AI Analyzer")
st.warning("לשימוש בידורי וסטטיסטי בלבד. אין הבטחת זכייה.")

LOTTO_MIN = 1
LOTTO_MAX = 37
STRONG_MIN = 1
STRONG_MAX = 7

all_lotto_numbers = list(range(LOTTO_MIN, LOTTO_MAX + 1))
all_strong_numbers = list(range(STRONG_MIN, STRONG_MAX + 1))


# ---------- Helpers ----------

def parse_lotto_history(text):
    lotto_numbers = []
    strong_numbers = []

    for line in text.splitlines():
        try:
            nums_part, strong_part = line.split("|")
            nums = [int(x.strip()) for x in nums_part.split(",")]
            strong = int(strong_part.strip())

            if len(nums) == 6:
                lotto_numbers.extend(nums)
                strong_numbers.append(strong)
        except:
            continue

    return lotto_numbers, strong_numbers


def score_ticket(ticket):
    evens = len([n for n in ticket if n % 2 == 0])
    lows = len([n for n in ticket if n <= 18])
    total = sum(ticket)
    adjacent = sum(1 for i in range(len(ticket) - 1) if ticket[i + 1] - ticket[i] == 1)

    score = 100

    if evens not in [2, 3, 4]:
        score -= 20

    if lows not in [2, 3, 4]:
        score -= 20

    if total < 90 or total > 150:
        score -= 20

    if adjacent > 1:
        score -= 20

    return score


def is_anti_crowd(ticket):
    common_human_numbers = {1, 2, 3, 4, 5, 7, 10, 11, 13, 18, 21, 22, 26, 30, 31}
    birthday_count = len([n for n in ticket if n <= 31])
    common_count = len([n for n in ticket if n in common_human_numbers])

    return birthday_count <= 4 and common_count <= 2


def generate_balanced_ticket():
    best_ticket = None
    best_score = -1

    for _ in range(500):
        ticket = sorted(random.sample(all_lotto_numbers, 6))
        score = score_ticket(ticket)

        if is_anti_crowd(ticket):
            score += 15

        if score > best_score:
            best_score = score
            best_ticket = ticket

    return best_ticket


def generate_hot_cold_ticket(lotto_numbers):
    if not lotto_numbers:
        return generate_balanced_ticket()

    counts = Counter(lotto_numbers)

    hot_numbers = [n for n, _ in counts.most_common(12)]
    cold_numbers = sorted(all_lotto_numbers, key=lambda x: counts[x])[:12]

    ticket = set()

    ticket.update(random.sample(hot_numbers, min(3, len(hot_numbers))))
    ticket.update(random.sample(cold_numbers, min(2, len(cold_numbers))))

    while len(ticket) < 6:
        ticket.add(random.choice(all_lotto_numbers))

    return sorted(ticket)


def generate_multi_tickets(amount, mode, lotto_numbers):
    tickets = set()
    attempts = 0

    while len(tickets) < amount and attempts < amount * 1000:
        attempts += 1

        if mode == "Balanced Distribution":
            ticket = generate_balanced_ticket()
        elif mode == "Hot + Cold Mix":
            ticket = generate_hot_cold_ticket(lotto_numbers)
        elif mode == "Anti-Crowd Mode":
            ticket = generate_balanced_ticket()
            if not is_anti_crowd(ticket):
                continue
        else:
            ticket = sorted(random.sample(all_lotto_numbers, 6))

        tickets.add(tuple(ticket))

    return [list(t) for t in sorted(tickets)]


def choose_strong(strong_numbers):
    if strong_numbers:
        counts = Counter(strong_numbers)
        return counts.most_common(1)[0][0]
    return random.randint(STRONG_MIN, STRONG_MAX)


# ---------- Input ----------

st.header("📥 תוצאות עבר")

past_lotto = st.text_area(
    "הדבק תוצאות עבר — כל שורה: 6 מספרים + חזק",
    placeholder="1,7,19,22,27,34 | 5\n3,10,16,24,31,37 | 2"
)

lotto_numbers, strong_numbers = parse_lotto_history(past_lotto)


# ---------- Stats ----------

if lotto_numbers:
    st.header("📊 ניתוח תוצאות עבר")

    counts = Counter(lotto_numbers)

    st.subheader("🔥 מספרים חמים")
    st.write(counts.most_common(10))

    st.subheader("❄️ מספרים קרים")
    cold = sorted(all_lotto_numbers, key=lambda x: counts[x])[:10]
    st.write(cold)

    st.subheader("💪 חזק נפוץ")
    st.write(Counter(strong_numbers).most_common())


# ---------- Generator ----------

st.header("🤖 מחולל טפסי AI")

budget = st.number_input("תקציב בש״ח", min_value=1, value=30)

ticket_price = st.number_input("מחיר לטופס בודד", min_value=1, value=3)

max_tickets_by_budget = max(1, budget // ticket_price)

amount = st.slider(
    "כמה טפסים ליצור?",
    min_value=1,
    max_value=50,
    value=min(10, max_tickets_by_budget)
)

mode = st.selectbox(
    "בחר מצב AI",
    [
        "Balanced Distribution",
        "Anti-Crowd Mode",
        "Hot + Cold Mix",
        "Random"
    ]
)

if st.button("צור טפסי AI"):
    tickets = generate_multi_tickets(amount, mode, lotto_numbers)

    st.success(f"נוצרו {len(tickets)} טפסים")

    for i, ticket in enumerate(tickets, start=1):
        strong = choose_strong(strong_numbers)
        score = score_ticket(ticket)

        st.write(
            f"טופס {i}: {ticket} | חזק: {strong} | ציון AI: {score}/100"
        )


# ---------- Chance ----------

st.header("🃏 צ׳אנס AI")

cards = ["7", "8", "9", "10", "J", "Q", "K", "A"]
suits = ["תלתן", "יהלום", "לב", "עלה"]

chance_amount = st.slider("כמה טפסי צ׳אנס ליצור?", 1, 20, 5)

if st.button("צור טפסי צ׳אנס"):
    for i in range(1, chance_amount + 1):
        chance_pick = {
            suit: random.choice(cards)
            for suit in suits
        }

        st.write(f"טופס צ׳אנס {i}:")
        st.write(chance_pick)


st.divider()
st.caption("ZakenChance AI — ניתוח סטטיסטי לכיף בלבד.")
