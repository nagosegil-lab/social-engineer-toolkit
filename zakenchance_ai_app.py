import random
from collections import Counter

import streamlit as st

LOTTO_MIN = 1
LOTTO_MAX = 37
LOTTO_PICK_COUNT = 6
STRONG_MIN = 1
STRONG_MAX = 7

CHANCE_CARDS = ["7", "8", "9", "10", "J", "Q", "K", "A"]
CHANCE_SUITS = ["תלתן", "יהלום", "לב", "עלה"]


def parse_lotto_history(raw_text):
    lotto_numbers = []
    strong_numbers = []
    invalid_lines = 0

    for line in raw_text.splitlines():
        cleaned = line.strip()
        if not cleaned:
            continue
        try:
            nums_part, strong_part = cleaned.split("|")
            nums = [int(x.strip()) for x in nums_part.split(",")]
            strong = int(strong_part.strip())
        except (ValueError, TypeError):
            invalid_lines += 1
            continue

        if len(nums) != LOTTO_PICK_COUNT:
            invalid_lines += 1
            continue
        if len(set(nums)) != LOTTO_PICK_COUNT:
            invalid_lines += 1
            continue
        if any((n < LOTTO_MIN or n > LOTTO_MAX) for n in nums):
            invalid_lines += 1
            continue
        if strong < STRONG_MIN or strong > STRONG_MAX:
            invalid_lines += 1
            continue

        lotto_numbers.extend(nums)
        strong_numbers.append(strong)

    return lotto_numbers, strong_numbers, invalid_lines


def pick_weighted_unique_lotto_numbers(counts):
    all_nums = list(range(LOTTO_MIN, LOTTO_MAX + 1))
    picks = set()
    while len(picks) < LOTTO_PICK_COUNT:
        weights = [counts[n] + 1 for n in all_nums]
        candidate = random.choices(all_nums, weights=weights, k=1)[0]
        picks.add(candidate)
    return sorted(picks)


st.set_page_config(page_title="ZakenChance AI", layout="centered")

st.title("🎲 ZakenChance AI Analyzer")
st.write("ניתוח סטטיסטי לכיף בלבד — אין הבטחת זכייה.")

st.warning("הגרלות לוטו וצ׳אנס הן אקראיות. הכלי הזה מנתח דפוסים ותדירויות בלבד.")

# ---------- Lotto ----------
st.header("🔢 לוטו ישראלי")

past_lotto = st.text_area(
    "הדבק תוצאות עבר — כל שורה: 6 מספרים + חזק",
    placeholder="1,7,19,22,27,34 | 5\n3,10,16,24,31,37 | 2",
)

lotto_numbers = []
strong_numbers = []

if past_lotto:
    lotto_numbers, strong_numbers, invalid_lines = parse_lotto_history(past_lotto)
    if invalid_lines:
        st.info(f"דילגתי על {invalid_lines} שורות לא תקינות.")

    st.subheader("📊 מספרים חמים")
    hot = Counter(lotto_numbers).most_common(10)
    st.write(hot)

    st.subheader("❄️ מספרים קרים")
    all_nums = list(range(LOTTO_MIN, LOTTO_MAX + 1))
    counts = Counter(lotto_numbers)
    cold = sorted(all_nums, key=lambda x: counts[x])[:10]
    st.write(cold)

if st.button("צור טופס לוטו AI"):
    all_nums = list(range(LOTTO_MIN, LOTTO_MAX + 1))

    if lotto_numbers:
        counts = Counter(lotto_numbers)
        pick = pick_weighted_unique_lotto_numbers(counts)

        if strong_numbers:
            strong_counts = Counter(strong_numbers)
            strong = strong_counts.most_common(1)[0][0]
        else:
            strong = random.randint(STRONG_MIN, STRONG_MAX)
    else:
        pick = sorted(random.sample(all_nums, LOTTO_PICK_COUNT))
        strong = random.randint(STRONG_MIN, STRONG_MAX)

    st.success(f"🎯 טופס AI: {pick} | חזק: {strong}")

# ---------- Chance ----------
st.header("🃏 צ׳אנס ישראלי")

if st.button("צור טופס צ׳אנס AI"):
    chance_pick = {suit: random.choice(CHANCE_CARDS) for suit in CHANCE_SUITS}

    st.success("🎯 טופס צ׳אנס AI:")
    for suit, card in chance_pick.items():
        st.write(f"{suit}: {card}")

st.divider()
st.caption("ZakenChance AI — לשימוש בידורי וסטטיסטי בלבד.")
