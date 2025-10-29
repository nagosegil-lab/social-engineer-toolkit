# 🤖 MT5 AI Trading Bot - בוט מסחר אוטומטי עם בינה מלאכותית

בוט מסחר מתקדם לפלטפורמת MT5 (MetaTrader 5) עם אסטרטגיית AI, שניתן לשלוט עליו ישירות מהטלפון הנייד שלך!

## ✨ תכונות עיקריות

- 🤖 **אסטרטגיית AI מתקדמת** - מודל למידת מכונה (Random Forest/Gradient Boosting) שמנתח את השוק
- 📱 **שליטה ניידת** - ממשק ווב מותאם לטלפון נייד
- 📊 **אינדיקטורים טכניים** - RSI, MACD, Bollinger Bands, EMA, SMA ועוד
- ⚡ **ביצוע אוטומטי** - פתיחה וסגירה אוטומטית של עסקאות
- 🛡️ **ניהול סיכונים** - Stop Loss, Take Profit, Trailing Stop
- 📈 **סטטיסטיקות בזמן אמת** - מעקב אחר ביצועים והחזרים
- 🔔 **התראות** - תמיכה באינטגרציה עם Telegram

## 📋 דרישות מקדימות

### 1. חשבון MT5
- פתח חשבון MT5 (דמו או ריאלי) אצל ברוקר כלשהו
- שמור את פרטי ההתחברות: מספר חשבון, סיסמה, שם שרת

### 2. Python
- Python 3.8 או גרסה חדשה יותר
- מותקן על המחשב/שרת שלך

### 3. MetaTrader 5 Terminal
- הורד והתקן את תוכנת MT5 (Windows)
- **חשוב**: הבוט צריך להיות מותקן על אותו מחשב שבו רץ MT5

## 🚀 התקנה מהירה

### שלב 1: התקן את הדרישות

```bash
cd /workspace/trading_bot
pip install -r requirements.txt
```

### שלב 2: הגדר את הקונפיגורציה

ערוך את הקובץ `config.py` והכנס את פרטי החשבון שלך:

```python
MT5_CONFIG = {
    'login': 12345678,  # מספר החשבון שלך ב-MT5
    'password': 'your_password',  # הסיסמה שלך
    'server': 'YourBroker-Demo',  # שם השרת של הברוקר
    'timeout': 60000,
    'portable': False
}

API_CONFIG = {
    'host': '0.0.0.0',
    'port': 5000,
    'secret_key': 'change-this-to-a-random-secret-key',
    'enable_cors': True,
    'auth_token': 'your-secure-token-here'  # שנה את זה!
}
```

**חשוב מאוד**: שנה את `auth_token` למשהו בטוח!

### שלב 3: הרץ את הבוט

```bash
python main.py
```

### שלב 4: גש מהטלפון שלך

1. מצא את כתובת ה-IP של המחשב שלך (Windows: `ipconfig`, Linux/Mac: `ifconfig`)
2. פתח דפדפן בטלפון והקלד: `http://YOUR_IP:5000`
3. הזן את ה-auth token שהגדרת
4. התחל לסחור! 🎉

## 📱 שימוש בממשק הנייד

### מסך הבקרה הראשי

- **Start Bot** ▶️ - מתחיל את הבוט (הבוט יתחיל לנתח ולבצע עסקאות)
- **Stop Bot** ⏸️ - עוצר את הבוט
- **Retrain AI Model** 🧠 - מאמן מחדש את מודל ה-AI עם דאטה עדכני

### מידע על החשבון

הצג:
- יתרה (Balance)
- הון עצמי (Equity)
- רווח/הפסד כולל
- רמת מרג'ין

### פוזיציות פתוחות

- ראה את כל העסקאות הפתוחות
- סגור עסקאות בלחיצה אחת
- מעקב אחר רווח/הפסד בזמן אמת

### סטטיסטיקות

- סה"כ עסקאות
- אחוז הצלחה (Win Rate)
- רווח כולל
- רווח יומי

## ⚙️ הגדרות מתקדמות

### פרמטרי מסחר

```python
TRADING_CONFIG = {
    'symbol': 'EURUSD',  # הזוג המטבעות לסחור בו
    'lot_size': 0.01,  # גודל הפוזיציה
    'max_positions': 3,  # מספר מקסימלי של פוזיציות פתוחות
    'stop_loss_pips': 50,  # Stop Loss בפיפסים
    'take_profit_pips': 100,  # Take Profit בפיפסים
    'trailing_stop': True,  # הפעל Trailing Stop
    'trailing_stop_pips': 30,  # מרחק ה-Trailing Stop
}
```

### ניהול סיכונים

```python
RISK_CONFIG = {
    'max_daily_loss': 0.05,  # מקסימום הפסד יומי (5%)
    'max_drawdown': 0.15,  # מקסימום ירידה (15%)
    'daily_profit_target': 0.03,  # יעד רווח יומי (3%)
    'enable_trading_hours': True,  # הגבל שעות מסחר
    'trading_hours': {
        'start': '08:00',  # התחלת מסחר
        'end': '22:00',  # סיום מסחר
        'timezone': 'UTC'
    }
}
```

### הגדרות AI

```python
AI_CONFIG = {
    'model_type': 'random_forest',  # או 'gradient_boosting'
    'lookback_period': 60,  # מספר נרות לניתוח
    'prediction_threshold': 0.6,  # רמת ביטחון מינימלית לעסקה
    'retrain_interval': 24,  # שעות בין אימונים מחדש
}
```

## 🔐 אבטחה

### הגדרת HTTPS (מומלץ מאוד!)

לשימוש אמיתי, מומלץ להגדיר HTTPS:

1. צור תעודת SSL:
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

2. ערוך את `api.py` להוסיף:
```python
app.run(host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))
```

### טיפים לאבטחה

- ✅ השתמש ב-auth token חזק ואקראי
- ✅ שנה את ה-token לעיתים קרובות
- ✅ אל תשתף את ה-token
- ✅ השתמש ב-HTTPS בייצור
- ✅ הגבל גישה ל-API לכתובות IP ספציפיות אם אפשר

## 🌐 גישה מרחוק (מחוץ לרשת הביתית)

### אפשרות 1: Port Forwarding

1. היכנס לראוטר שלך
2. הגדר Port Forwarding לפורט 5000
3. מצא את ה-IP החיצוני שלך: https://whatismyipaddress.com/
4. גש מהטלפון: `http://YOUR_PUBLIC_IP:5000`

### אפשרות 2: Ngrok (קל ומהיר!)

```bash
# התקן ngrok
npm install -g ngrok

# הרץ ngrok
ngrok http 5000
```

Ngrok ייתן לך URL ציבורי שתוכל לגשת אליו מכל מקום!

### אפשרות 3: VPS/Cloud Server

העלה את הבוט לשרת בענן (AWS, DigitalOcean, Vultr) כדי שירוץ 24/7.

## 📊 איך זה עובד?

### תהליך קבלת החלטות של הבוט

1. **איסוף נתונים** 📈
   - הבוט מושך נתוני מחירים היסטוריים מ-MT5
   - מחשב אינדיקטורים טכניים (RSI, MACD, וכו')

2. **ניתוח AI** 🧠
   - מודל למידת מכונה מנתח את הנתונים
   - מחזיר אות: BUY, SELL, או HOLD
   - כולל רמת ביטחון (0-100%)

3. **החלטת מסחר** 💡
   - אם רמת הביטחון מעל הסף (60% כברירת מחדל)
   - והתנאים מתאימים (שעות מסחר, מרג'ין, וכו')
   - הבוט פותח עסקה

4. **ניהול פוזיציה** 🎯
   - מגדיר Stop Loss ו-Take Profit אוטומטית
   - מעדכן Trailing Stop
   - סוגר עסקאות לפי תנאים

5. **למידה מתמשכת** 🔄
   - הבוט מאמן מחדש את המודל מדי 24 שעות
   - משתפר עם הזמן ומסתגל לשוק

## 🎯 אסטרטגיית המסחר

הבוט משתמש באסטרטגיה היברידית:

### אינדיקטורים טכניים
- **RSI** - זיהוי תנאים של oversold/overbought
- **MACD** - זיהוי מגמות וחצייה
- **Bollinger Bands** - זיהוי תנודתיות וברייקאאוטים
- **EMA/SMA** - זיהוי כיוון מגמה
- **ATR** - מדידת תנודתיות

### למידת מכונה
- מודל Random Forest או Gradient Boosting
- מאומן על 5,000 נרות היסטוריות
- לומד דפוסים מורכבים שקשה לזהות ידנית

## ⚠️ אזהרות חשובות

1. **התחל עם חשבון דמו!** 
   - נסה את הבוט עם חשבון דמו לפני כסף אמיתי
   - הבן איך הוא עובד ומה האסטרטגיה שלו

2. **למידת מכונה אינה קסם**
   - אין ערובה לרווחיות
   - ביצועי העבר אינם מבטיחים ביצועים עתידיים

3. **ניהול סיכונים**
   - אל תסחר יותר ממה שאתה יכול להרשות לעצמך להפסיד
   - השתמש תמיד ב-Stop Loss
   - התחל עם גדלים קטנים

4. **מעקב שוטף**
   - עקוב אחר הבוט באופן קבוע
   - בדוק את הביצועים
   - התאם פרמטרים לפי הצורך

## 🐛 פתרון בעיות

### הבוט לא מתחבר ל-MT5

1. וודא ש-MT5 פתוח ומחובר
2. בדוק שפרטי ההתחברות נכונים
3. וודא שהבוט רץ על אותו מחשב של MT5

### הבוט לא פותח עסקאות

1. בדוק שהוא במצב "Running"
2. וודא שאתה בשעות המסחר המוגדרות
3. בדוק שיש מרג'ין פנוי
4. הגדר `prediction_threshold` נמוך יותר

### שגיאות Python

```bash
# התקן מחדש את הדרישות
pip install -r requirements.txt --upgrade

# אם יש בעיה עם MT5
pip uninstall MetaTrader5
pip install MetaTrader5==5.0.45
```

### לא מצליח להתחבר מהטלפון

1. וודא שהמחשב והטלפון באותה רשת Wi-Fi
2. בדוק את החומת האש (Firewall) - ייתכן שצריך לאפשר את פורט 5000
3. נסה את כתובת ה-IP השנייה של המחשב אם יש יותר מאחת

## 📞 תמיכה והרחבות

### הוסף אינדיקטור חדש

ערוך את `ai_strategy.py` והוסף לקלאס `TechnicalIndicators`:

```python
@staticmethod
def calculate_custom_indicator(data: pd.Series) -> pd.Series:
    # הוסף את הלוגיקה שלך כאן
    return result
```

### שנה את האסטרטגיה

ערוך את `bot.py`, פונקציה `_execute_trade()` כדי להוסיף לוגיקה מותאמת אישית.

### הוסף התראות Telegram

1. צור בוט ב-Telegram דרך @BotFather
2. קבל את ה-token וה-chat_id
3. הזן אותם ב-`config.py`:

```python
NOTIFICATION_CONFIG = {
    'enable_notifications': True,
    'telegram_bot_token': 'YOUR_BOT_TOKEN',
    'telegram_chat_id': 'YOUR_CHAT_ID',
}
```

## 📈 טיפים לשיפור ביצועים

1. **אמן מחדש בתדירות גבוהה** - במשק תנודתי, אמן כל 12 שעות
2. **התאם פרמטרים** - נסה ערכים שונים של stop loss/take profit
3. **בחר זמנים טובים** - הגבל מסחר לשעות בהן השוק פעיל
4. **diversification** - הרץ על מספר זוגות מטבע
5. **בדיקה עקבית** - עקוב אחר ה-win rate והתאם

## 📝 רישיון

פרויקט זה הוא לשימוש אישי ולמידה. השתמש בו באחריותך בלבד.

## 🎓 למידה נוספת

- [תיעוד MT5 Python](https://www.mql5.com/en/docs/python_metatrader5)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [אסטרטגיות מסחר עם AI](https://www.investopedia.com/terms/a/algorithmic-trading.asp)

---

**בהצלחה במסחר! 🚀📈💰**

*זכור: מסחר כרוך בסיכון. אל תסחר בכסף שאתה לא יכול להפסיד.*
