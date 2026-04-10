# Historical Number Scorer

כלי פשוט בפייתון לשקלול ערכים (מספרים/קלפים/סמלים) לפי היסטוריית הגרלות.

## מה הכלי עושה

הכלי קורא קובץ CSV של תוצאות היסטוריות ומחשב לכל ערך ציון משוקלל לפי:

1. **שכיחות** – כמה פעמים הערך הופיע.
2. **עדכניות** – כמה לאחרונה הערך הופיע.
3. **מגמה** – האם הערך מופיע יותר בחלון הזמן האחרון יחסית לעבר.

> חשוב: זה כלי אנליטי/סטטיסטי בלבד, לא הבטחת זכייה.

## פורמט קלט מומלץ

CSV עם כותרת, כאשר בכל שורה יש "הגרלה" אחת.

דוגמה:

```csv
spade,heart,diamond,club,datetime,draw_id
K,10,K,K,30/03/26 17:00,52673
J,8,8,K,30/03/26 15:00,52672
9,K,10,K,30/03/26 13:00,52671
```

אפשר לכלול גם עמודות נוספות (תאריך/מזהה), ופשוט להחריג אותן בהרצה.

## הרצה בסיסית

```bash
python3 tools/historical_number_scorer.py \
  --input /path/to/history.csv \
  --exclude-columns datetime draw_id \
  --top 10
```

## בחירת עמודות ספציפיות

אם רוצים לקבע עמודות:

```bash
python3 tools/historical_number_scorer.py \
  --input /path/to/history.csv \
  --columns spade heart diamond club
```

## כיוונון משקלים

```bash
python3 tools/historical_number_scorer.py \
  --input /path/to/history.csv \
  --exclude-columns datetime draw_id \
  --weights 0.6 0.25 0.15
```

הסדר הוא: `frequency recency trend`.

## חלון "אחרון" למגמה

- כמספר הגרלות: `--recent-window 20`
- כחלק יחסי מההיסטוריה: `--recent-window 0.3` (כלומר 30%)

## שמירת תוצאות לקובץ

```bash
python3 tools/historical_number_scorer.py \
  --input /path/to/history.csv \
  --exclude-columns datetime draw_id \
  --output-csv /path/to/scored.csv
```

## המלצת קומבינציות (זוגות/שלשות/רביעיות)

אפשר להפעיל גם דירוג לקומבינציות ולא רק לערכים בודדים:

```bash
python3 tools/historical_number_scorer.py \
  --input /path/to/history.csv \
  --exclude-columns datetime draw_id \
  --combo-size 4 \
  --top-combos 15 \
  --combos-output-csv /path/to/combos_scored.csv
```

- `--combo-size 2` עבור זוגות
- `--combo-size 3` עבור שלשות
- `--combo-size 4` עבור רביעיות

## ממשק גרפי (GUI)

לשימוש נוח ללא פקודות:

```bash
python3 tools/historical_number_scorer_gui.py
```

בחלון:
1. בוחרים קובץ CSV
2. מגדירים עמודות/Exclude (אם צריך)
3. מגדירים משקלים וחלון recent
4. (אופציונלי) מגדירים `Combination size`
5. לוחצים `Run analysis`

