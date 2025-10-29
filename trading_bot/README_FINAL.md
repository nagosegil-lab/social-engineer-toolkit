# 🤖 בוט מסחר MT5 + AI 📱

**בוט מסחר מתקדם המשלב MetaTrader 5 עם בינה מלאכותית לניתוח שוק וקבלת החלטות מסחר אוטומטיות**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![MT5](https://img.shields.io/badge/MetaTrader-5-green.svg)](https://www.metatrader5.com)
[![AI](https://img.shields.io/badge/AI-Machine%20Learning-orange.svg)](https://scikit-learn.org)
[![Mobile](https://img.shields.io/badge/Mobile-Responsive-purple.svg)](https://flask.palletsprojects.com)

---

## 🚀 הפעלה מהירה (5 דקות)

### אופציה 1: התקנה אוטומטית (מומלץ)
```bash
# הורד והפעל
git clone <repository-url>
cd trading_bot
chmod +x install_and_run.sh
./install_and_run.sh
```

### אופציה 2: התקנה ידנית
```bash
# 1. הכנת הסביבה
python -m venv trading_bot_env
source trading_bot_env/bin/activate  # Linux/Mac
# או
trading_bot_env\\Scripts\\activate  # Windows

# 2. התקנת חבילות
pip install -r requirements.txt

# 3. הפעלה
python start_bot.py
```

### אופציה 3: עם Docker
```bash
# הפעלה עם Docker
docker-compose up -d
```

### 📋 הגדרה ראשונית
1. **ערוך .env** - הוסף פרטי MT5 שלך
2. **פתח דפדפן** - נווט ל: `http://localhost:5000`
3. **התחל מסחר** - לחץ על "התחל בוט"

---

## ✨ תכונות עיקריות

- 🤖 **בינה מלאכותית מתקדמת** - ניתוח שוק עם Machine Learning
- 📱 **ממשק מובייל ידידותי** - שליטה מלאה מהטלפון
- 📊 **ניתוח טכני מקיף** - RSI, MACD, Bollinger Bands ועוד
- 🛡️ **ניהול סיכונים חכם** - הגנה על ההון
- 📈 **גרפים אינטראקטיביים** - מעקב אחר המחירים בזמן אמת
- ⚡ **ביצועים מהירים** - תגובה מהירה לשינויים בשוק

---

## 📱 ממשק מובייל

הממשק המובייל כולל:

- **לוח בקרה** - מידע על יתרה, רווח/הפסד, פוזיציות פתוחות
- **גרף מחירים** - גרף קנדליסטיק אינטראקטיבי
- **ניתוח AI** - חיזויים וניתוח מצב השוק
- **ניהול פוזיציות** - סגירה מהירה של פוזיציות
- **הגדרות** - התאמת פרמטרי המסחר

---

## 🧠 איך הבינה המלאכותית עובדת

הבוט משתמש בטכנולוגיות מתקדמות:

1. **איסוף נתונים** - איסוף נתוני מחיר, נפח ואינדיקטורים טכניים
2. **ניתוח טכני** - חישוב RSI, MACD, Bollinger Bands, Stochastic ועוד
3. **למידת מכונה** - אימון מודל Random Forest על נתונים היסטוריים
4. **חיזוי** - קבלת החלטות מסחר על בסיס הניתוח
5. **ניהול סיכונים** - הגבלת הפסדים ומקסום רווחים

---

## ⚙️ הגדרות מתקדמות

### פרמטרי מסחר
```python
SYMBOL=EURUSD          # זוג מטבע
TIMEFRAME=M15          # מסגרת זמן
LOT_SIZE=0.01          # גודל פוזיציה
MAX_POSITIONS=3        # מקסימום פוזיציות
STOP_LOSS_PIPS=50      # הפסד מקסימלי
TAKE_PROFIT_PIPS=100   # רווח יעד
```

### ניהול סיכונים
```python
MAX_DAILY_LOSS=100.0   # הפסד יומי מקסימלי
MAX_DAILY_PROFIT=500.0 # רווח יומי מקסימלי
```

---

## 📊 אינדיקטורים טכניים

הבוט משתמש באינדיקטורים הבאים:

- **Moving Averages** - SMA 20/50, EMA 12/26
- **MACD** - Moving Average Convergence Divergence
- **RSI** - Relative Strength Index
- **Bollinger Bands** - פסי בולינגר
- **Stochastic** - אוסצילטור סטוכסטי
- **ATR** - Average True Range
- **Volume Analysis** - ניתוח נפח

---

## 🛡️ ניהול סיכונים

הבוט כולל מערכת ניהול סיכונים מתקדמת:

- **הגבלת הפסדים יומיים** - עצירה אוטומטית במקרה של הפסדים גדולים
- **הגבלת רווחים יומיים** - שמירה על רווחים
- **גבלת פוזיציות** - מניעת חשיפה מוגזמת
- **Stop Loss דינמי** - חישוב Stop Loss על בסיס ATR
- **Risk-Reward Ratio** - יחס סיכון-תשואה של 1:2

---

## 📈 ביצועים

הבוט מתאים למסחר ב:

- **זוגות מטבע** (Forex) - EUR/USD, GBP/USD, USD/JPY
- **מטאלים** - זהב, כסף
- **מניות** - מניות עיקריות
- **קריפטו** - ביטקוין, אתריום

---

## 🔧 פתרון בעיות

### בעיות חיבור ל-MT5
1. ודא ש-MetaTrader 5 פתוח
2. בדוק את פרטי ההתחברות
3. ודא שהחשבון פעיל

### בעיות ביצועים
1. בדוק את חיבור האינטרנט
2. ודא שיש מספיק זיכרון RAM
3. סגור תוכנות מיותרות

---

## 📚 קבצים חשובים

- `main.py` - נקודת כניסה ראשית
- `start_bot.py` - הפעלה קלה עם ממשק
- `quick_start.py` - התקנה מהירה
- `run_demo.py` - הדגמה ללא MT5
- `mobile_app.py` - ממשק מובייל
- `trading_bot.py` - לוגיקת הבוט הראשית
- `ai_analyzer.py` - ניתוח AI
- `mt5_connector.py` - חיבור ל-MT5
- `risk_manager.py` - ניהול סיכונים

---

## 🎯 דוגמאות שימוש

### הפעלה בסיסית
```python
from trading_bot import TradingBot

bot = TradingBot()
bot.start()  # הפעלה במצב קונסולה
```

### הפעלה עם ממשק מובייל
```python
python start_bot.py
```

### הרצת דמו
```python
python run_demo.py
```

---

## ⚠️ אזהרה

**המסחר במט"ח כרוך בסיכון גבוה ואינו מתאים לכל המשקיעים.**
**השתמש רק בהון שאתה יכול להרשות לעצמך להפסיד.**
**הבוט מיועד למטרות חינוכיות ומחקריות בלבד.**

---

## 📞 תמיכה

לשאלות ותמיכה:
- פתח Issue ב-GitHub
- בדוק את הלוגים בקובץ `trading_bot.log`
- ראה `QUICK_START.md` להדרכה מהירה

---

## 📄 רישיון

MIT License - ראה קובץ LICENSE לפרטים.

---

**בהצלחה במסחר! 🚀📈**