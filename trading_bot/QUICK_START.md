# 🚀 התחלה מהירה - בוט מסחר MT5

## התקנה בדקה אחת!

### 1️⃣ התקן Python Packages
```bash
cd /workspace/trading_bot
pip install -r requirements.txt
```

### 2️⃣ הגדר את פרטי ה-MT5 שלך
פתח את `config.py` ושנה:

```python
MT5_CONFIG = {
    'login': 12345678,        # ← שנה למספר החשבון שלך
    'password': 'password',    # ← שנה לסיסמה שלך
    'server': 'Broker-Demo',   # ← שנה לשרת שלך
}

API_CONFIG = {
    'auth_token': 'my-secret-token-12345'  # ← שנה לטוקן אישי!
}
```

### 3️⃣ הרץ את הבוט
```bash
python main.py
```

### 4️⃣ התחבר מהטלפון
1. מצא את ה-IP של המחשב:
   - Windows: פתח CMD והקלד `ipconfig`
   - Mac/Linux: פתח Terminal והקלד `ifconfig`
   
2. פתח דפדפן בטלפון וגש ל:
   ```
   http://YOUR_IP_ADDRESS:5000
   ```
   
3. הזן את ה-auth token שהגדרת

4. לחץ על "▶ Start Bot" והבוט יתחיל לעבוד!

---

## 📱 גישה מחוץ לבית? השתמש ב-Ngrok!

```bash
# התקן ngrok
npm install -g ngrok

# במסוף נפרד, הרץ:
ngrok http 5000
```

Ngrok ייתן לך URL כמו: `https://abc123.ngrok.io`

עכשיו תוכל לגשת לבוט מכל מקום בעולם! 🌍

---

## ⚡ פקודות מהירות

### הרץ בוט ישירות
```bash
python main.py
```

### אמן מודל AI ידנית
```python
python -c "
from bot import TradingBot
bot = TradingBot()
if bot.initialize():
    print('Training model...')
    df = bot.mt5.get_historical_data('EURUSD', 'H1', 5000)
    bot.ai_strategy.train_model(df)
    print('Done!')
"
```

### בדוק סטטוס
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:5000/api/status
```

---

## 🎯 טיפ מהיר: התחל עם דמו!

1. פתח חשבון דמו ב-MT5 (חינם!)
2. הרץ את הבוט על חשבון הדמו למשך שבוע
3. עקוב אחר הביצועים
4. רק אז עבור לחשבון אמיתי (אם אתה מרגיש בטוח)

---

## ❓ בעיות נפוצות

**"Failed to connect to MT5"**
- ✅ MT5 פתוח?
- ✅ MT5 מחובר לאינטרנט?
- ✅ פרטי החשבון נכונים?

**"Bot not trading"**
- ✅ לחצת על "Start Bot"?
- ✅ יש מרג'ין פנוי?
- ✅ אתה בשעות המסחר?

**"Can't access from phone"**
- ✅ טלפון ומחשב באותו WiFi?
- ✅ Firewall מאפשר את פורט 5000?
- ✅ ה-IP נכון?

---

**זהו! בהצלחה! 🎉**
