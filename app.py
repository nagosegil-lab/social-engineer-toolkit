import csv
import io
from collections import Counter

import streamlit as st

from zakenchance_core import (
    ALL_LOTTO_NUMBERS,
    CHANCE_CARDS,
    CHANCE_SUITS,
    chance_suit_counters,
    choose_strong,
    generate_multi_chance_tickets,
    generate_multi_tickets,
    parse_chance_history,
    parse_lotto_history,
    ticket_score_details,
)

st.set_page_config(page_title="ZakenChance AI", layout="centered")

st.title("🎲 ZakenChance AI Analyzer")
st.warning("לשימוש בידורי וסטטיסטי בלבד. אין הבטחת זכייה.")


def reset_app_state():
    st.session_state["past_lotto_input"] = ""
    st.session_state["past_chance_input"] = ""
    st.session_state["generated_lotto_tickets"] = []
    st.session_state["generated_chance_tickets"] = []


if "generated_lotto_tickets" not in st.session_state:
    st.session_state["generated_lotto_tickets"] = []
if "generated_chance_tickets" not in st.session_state:
    st.session_state["generated_chance_tickets"] = []
if "past_lotto_input" not in st.session_state:
    st.session_state["past_lotto_input"] = ""
if "past_chance_input" not in st.session_state:
    st.session_state["past_chance_input"] = ""


st.header("📥 תוצאות עבר")
st.button("נקה קלט ותוצאות", on_click=reset_app_state)

past_lotto = st.text_area(
    "הדבק תוצאות עבר — כל שורה: 6 מספרים + חזק",
    placeholder="1,7,19,22,27,34 | 5\n3,10,16,24,31,37 | 2",
    key="past_lotto_input",
)
lotto_numbers, strong_numbers, lotto_invalid_rows = parse_lotto_history(past_lotto)

if lotto_invalid_rows:
    st.warning(f"זוהו {len(lotto_invalid_rows)} שורות לוטו לא תקינות.")
    with st.expander("פירוט שורות שנפסלו (לוטו)"):
        for row_error in lotto_invalid_rows:
            st.write(f"- {row_error}")

past_chance = st.text_area(
    "הדבק תוצאות צ׳אנס עבר — כל שורה: 4 קלפים לפי סדר תלתן,יהלום,לב,עלה",
    placeholder="10,K,8,J\n7,10,Q,A",
    key="past_chance_input",
)
chance_draws, chance_invalid_rows = parse_chance_history(past_chance)

if chance_invalid_rows:
    st.warning(f"זוהו {len(chance_invalid_rows)} שורות צ׳אנס לא תקינות.")
    with st.expander("פירוט שורות שנפסלו (צ׳אנס)"):
        for row_error in chance_invalid_rows:
            st.write(f"- {row_error}")


if lotto_numbers:
    st.header("📊 ניתוח תוצאות עבר - לוטו")
    counts = Counter(lotto_numbers)

    st.subheader("🔥 מספרים חמים")
    st.write(counts.most_common(10))

    st.subheader("❄️ מספרים קרים")
    cold_numbers = sorted(ALL_LOTTO_NUMBERS, key=lambda value: counts[value])[:10]
    st.write(cold_numbers)

    st.subheader("💪 חזק נפוץ")
    st.write(Counter(strong_numbers).most_common())

if chance_draws:
    st.header("📊 ניתוח תוצאות עבר - צ׳אנס")
    suit_counters = chance_suit_counters(chance_draws)
    for suit in CHANCE_SUITS:
        counter = suit_counters[suit]
        hot_cards = counter.most_common(3)
        cold_cards = sorted(CHANCE_CARDS, key=lambda card: counter[card])[:3]
        st.write(f"{suit} | חמים: {hot_cards} | קרים: {cold_cards}")


st.header("🤖 מחולל טפסי AI - לוטו")

budget = st.number_input("תקציב בש״ח", min_value=1, value=30, step=1)
ticket_price = st.number_input("מחיר לטופס בודד", min_value=1, value=3, step=1)

max_tickets_by_budget = int(budget // ticket_price)
if max_tickets_by_budget == 0:
    st.error("התקציב הנוכחי לא מספיק אפילו לטופס לוטו אחד.")
    amount = 0
else:
    allowed_ticket_max = min(50, max_tickets_by_budget)
    if max_tickets_by_budget > 50:
        st.info("הבחירה מוגבלת ל-50 טפסים לכל יצירה.")
    amount = st.slider(
        "כמה טפסים ליצור?",
        min_value=1,
        max_value=allowed_ticket_max,
        value=min(10, allowed_ticket_max),
    )

mode = st.selectbox(
    "בחר מצב AI ללוטו",
    [
        "Balanced Distribution",
        "Anti-Crowd Mode",
        "Hot + Cold Mix",
        "Random",
    ],
)

if st.button("צור טפסי לוטו AI"):
    if amount == 0:
        st.error("לא ניתן ליצור טפסים עם התקציב והמחיר הנוכחיים.")
    else:
        tickets = generate_multi_tickets(
            amount=amount,
            mode=mode,
            lotto_numbers=lotto_numbers,
            all_numbers=ALL_LOTTO_NUMBERS,
        )
        generated_rows = []
        for index, ticket in enumerate(tickets, start=1):
            strong = choose_strong(strong_numbers)
            details = ticket_score_details(ticket)
            generated_rows.append(
                {
                    "index": index,
                    "ticket": ticket,
                    "strong": strong,
                    "details": details,
                }
            )
        st.session_state["generated_lotto_tickets"] = generated_rows
        st.success(f"נוצרו {len(generated_rows)} טפסים.")

generated_lotto = st.session_state["generated_lotto_tickets"]
if generated_lotto:
    for row in generated_lotto:
        details = row["details"]
        penalties = ", ".join(reason for reason, _ in details["penalties"]) or "ללא הורדות"
        st.write(
            f"טופס {row['index']}: {row['ticket']} | חזק: {row['strong']} "
            f"| ציון AI: {details['score']}/100"
        )
        st.caption(
            f"זוגיים: {details['evens']}, נמוכים (<=18): {details['lows']}, "
            f"סכום: {details['total']}, רצפים: {details['adjacent_pairs']}"
        )
        st.caption(f"הורדות ציון: {penalties}")

    lotto_csv_buffer = io.StringIO()
    lotto_writer = csv.writer(lotto_csv_buffer)
    lotto_writer.writerow(
        [
            "ticket_index",
            "numbers",
            "strong",
            "ai_score",
            "evens",
            "low_numbers",
            "sum",
            "adjacent_pairs",
            "penalties",
        ]
    )
    for row in generated_lotto:
        details = row["details"]
        penalty_text = "; ".join(reason for reason, _ in details["penalties"])
        lotto_writer.writerow(
            [
                row["index"],
                "-".join(str(number) for number in row["ticket"]),
                row["strong"],
                details["score"],
                details["evens"],
                details["lows"],
                details["total"],
                details["adjacent_pairs"],
                penalty_text,
            ]
        )
    st.download_button(
        "ייצוא טפסי לוטו ל-CSV",
        data=lotto_csv_buffer.getvalue().encode("utf-8-sig"),
        file_name="zakenchance_lotto_tickets.csv",
        mime="text/csv",
    )


st.header("🃏 מחולל טפסי AI - צ׳אנס")

chance_amount = st.slider("כמה טפסי צ׳אנס ליצור?", min_value=1, max_value=20, value=5)
chance_mode = st.selectbox(
    "בחר מצב AI לצ׳אנס",
    [
        "Balanced Distribution",
        "History Weighted",
        "Hot + Cold Mix",
        "Random",
    ],
)

if st.button("צור טפסי צ׳אנס AI"):
    chance_tickets = generate_multi_chance_tickets(
        amount=chance_amount,
        mode=chance_mode,
        chance_draws=chance_draws,
        cards=CHANCE_CARDS,
        suits=CHANCE_SUITS,
    )
    st.session_state["generated_chance_tickets"] = chance_tickets
    st.success(f"נוצרו {len(chance_tickets)} טפסי צ׳אנס.")

generated_chance = st.session_state["generated_chance_tickets"]
if generated_chance:
    chance_csv_buffer = io.StringIO()
    chance_writer = csv.writer(chance_csv_buffer)
    chance_writer.writerow(["ticket_index"] + CHANCE_SUITS)
    for index, ticket in enumerate(generated_chance, start=1):
        st.write(f"טופס צ׳אנס {index}: {ticket}")
        chance_writer.writerow([index] + [ticket[suit] for suit in CHANCE_SUITS])
    st.download_button(
        "ייצוא טפסי צ׳אנס ל-CSV",
        data=chance_csv_buffer.getvalue().encode("utf-8-sig"),
        file_name="zakenchance_chance_tickets.csv",
        mime="text/csv",
    )

st.divider()
st.caption("ZakenChance AI — ניתוח סטטיסטי לכיף בלבד.")
