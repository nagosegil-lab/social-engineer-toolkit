# 📋 מדריך התקנה מפורט - בוט מסחר נייד

## 🎯 דרישות מערכת

### מערכת הפעלה נתמכות
- **Windows 10/11** (64-bit)
- **macOS 10.15+** (Intel/M1/M2)
- **Linux Ubuntu 18.04+** או הפצות דומות
- **Android/iOS** (לגישה לממשק בלבד)

### תוכנות נדרשות
- **Python 3.8+** - שפת התכנות
- **MetaTrader 5** - פלטפורמת המסחר
- **Git** (אופציונלי) - לשכפול הפרויקט
- **Docker** (אופציונלי) - להרצה בקונטיינר

## 🔧 התקנה שלב אחר שלב

### שלב 1: התקנת Python

#### Windows:
1. גש ל-[python.org](https://python.org/downloads/)
2. הורד Python 3.8 או גרסה חדשה יותר
3. הרץ את הקובץ והקפד לסמן "Add Python to PATH"
4. בדוק התקנה:
```cmd
python --version
pip --version
```

#### macOS:
```bash
# עם Homebrew (מומלץ)
brew install python3

# או הורד מ-python.org
# בדיקה:
python3 --version
pip3 --version
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
pip3 --version
```

### שלב 2: התקנת MetaTrader 5

#### Windows:
1. הורד MT5 מאתר הברוקר שלך
2. התקן והגדר חשבון (דמו או אמיתי)
3. ודא שהחשבון פעיל ומחובר

#### macOS:
```bash
# דרך Wine (מורכב יותר)
# או השתמש ב-VPS עם Windows
# או חיבור לשרת MT5 מרחוק
```

#### Linux:
```bash
# דרך Wine
sudo apt install wine
# הורד MT5 Windows version והרץ דרך Wine
# או השתמש ב-VPS
```

### שלב 3: הורדת הבוט

#### דרך Git:
```bash
git clone https://github.com/your-repo/mobile-trading-bot.git
cd mobile-trading-bot
```

#### הורדה ידנית:
1. הורד ZIP מ-GitHub
2. חלץ לתיקייה
3. פתח terminal/cmd בתיקייה

### שלב 4: הגדרת סביבת Python

```bash
# יצירת סביבה וירטואלית (מומלץ)
python3 -m venv trading_env

# הפעלת הסביבה
# Windows:
trading_env\Scripts\activate
# macOS/Linux:
source trading_env/bin/activate

# התקנת חבילות
pip install -r requirements_trading.txt
```

### שלב 5: הרצת סקריפט ההתקנה

```bash
python3 setup_bot.py
```

הסקריפט יצור:
- תיקיות נדרשות
- קבצי הגדרות
- סקריפטי הפעלה
- קבצי Docker

### שלב 6: הגדרת קובץ הסביבה

```bash
# העתק את קובץ הדוגמה
cp .env.example .env

# ערוך את הקובץ
nano .env  # Linux/Mac
notepad .env  # Windows
```

#### הגדרות MT5 חובה:
```bash
MT5_SERVER=your-broker-server
MT5_LOGIN=your_account_number
MT5_PASSWORD=your_password
```

#### הגדרות Telegram (אופציונלי):
```bash
TELEGRAM_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

#### הגדרות Email (אופציונלי):
```bash
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_TO=alerts@yourdomain.com
```

## 🤖 הגדרת בוט Telegram

### יצירת בוט:
1. פתח Telegram ושלח הודעה ל-@BotFather
2. שלח `/newbot`
3. בחר שם לבוט
4. בחר username (חייב להסתיים ב-bot)
5. שמור את ה-Token

### קבלת Chat ID:
1. שלח הודעה לבוט שלך
2. גש ל-`https://api.telegram.org/bot<TOKEN>/getUpdates`
3. חפש את ה-chat.id בתגובה

## 📧 הגדרת Email

### Gmail:
1. הפעל 2-Factor Authentication
2. צור App Password:
   - הגדרות → אבטחה → App passwords
   - בחר Mail ו-Other
   - השתמש בסיסמה שנוצרה

### הגדרות SMTP נפוצות:
```bash
# Gmail
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_PORT=587

# Outlook
EMAIL_SMTP_SERVER=smtp-mail.outlook.com
EMAIL_PORT=587

# Yahoo
EMAIL_SMTP_SERVER=smtp.mail.yahoo.com
EMAIL_PORT=587
```

## 🚀 הפעלה ראשונה

### בדיקת הגדרות:
```bash
# בדוק שכל הקבצים במקום
ls -la

# בדוק שהסביבה פעילה
which python  # צריך להראות את הסביבה הוירטואלית
```

### הפעלה:
```bash
# Linux/Mac
chmod +x start_bot.sh
./start_bot.sh

# Windows
start_bot.bat

# או ישירות
python3 main.py
```

### בדיקת הפעלה:
1. פתח דפדפן
2. גש ל-`http://localhost:8080`
3. התחבר עם סיסמה: `trading123`
4. בדוק שהדשבורד נטען

## 🐳 התקנה עם Docker

### התקנת Docker:
```bash
# Ubuntu
sudo apt install docker.io docker-compose
sudo usermod -aG docker $USER

# macOS
# הורד Docker Desktop מ-docker.com

# Windows
# הורד Docker Desktop מ-docker.com
```

### הרצה עם Docker:
```bash
# בנייה והרצה
docker-compose up --build

# הרצה ברקע
docker-compose up -d

# עצירה
docker-compose down
```

## 🌐 גישה מהטלפון

### הגדרת רשת:
1. ודא שהמחשב והטלפון באותה רשת WiFi
2. מצא את IP של המחשב:
```bash
# Windows
ipconfig

# macOS/Linux
ifconfig
# או
ip addr show
```

### גישה מהטלפון:
1. פתח דפדפן בטלפון
2. גש ל-`http://YOUR_COMPUTER_IP:8080`
3. התחבר עם הסיסמה

### גישה מהאינטרנט (מתקדם):
```bash
# עם ngrok (לבדיקות בלבד)
ngrok http 8080

# עם port forwarding בנתב
# פתח port 8080 ופנה אותו למחשב
```

## 🔧 פתרון בעיות התקנה

### Python לא מותקן:
```bash
# בדוק גרסה
python3 --version

# אם לא עובד, התקן מחדש מ-python.org
```

### חבילות לא מותקנות:
```bash
# עדכן pip
pip install --upgrade pip

# התקן מחדש
pip install -r requirements_trading.txt --force-reinstall
```

### MT5 לא מתחבר:
1. בדוק שMT5 רץ ומחובר
2. ודא שהחשבון פעיל
3. בדוק הגדרות חומת אש
4. נסה חשבון דמו קודם

### Port תפוס:
```bash
# שנה port בקובץ .env
WEB_PORT=8081

# או מצא מי משתמש בport
# Windows
netstat -ano | findstr :8080

# Linux/Mac
lsof -i :8080
```

### בעיות הרשאות:
```bash
# Linux/Mac
chmod +x start_bot.sh
sudo chown -R $USER:$USER .

# Windows - הרץ כמנהל
```

## 📱 אופטימיזציה לנייד

### הגדרות דפדפן:
1. הוסף לmain screen (Add to Home Screen)
2. הפעל notifications
3. השבת auto-lock בזמן שימוש

### חיסכון בסוללה:
1. השתמש ב-WiFi במקום נתונים סלולריים
2. הקטן brightness
3. סגור אפליקציות אחרות

## 🔒 אבטחה והגנה

### שינוי סיסמה:
```python
# בקובץ trading_bot/web/app.py
# שנה את השורה:
if password == 'trading123':  # שנה כאן!
```

### הגדרת HTTPS:
```bash
# צור תעודות SSL
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# עדכן הגדרות Flask
```

### חומת אש:
```bash
# Ubuntu
sudo ufw allow 8080
sudo ufw enable

# Windows
# הגדר דרך Windows Defender Firewall
```

## 📊 ניטור והתחזוקה

### לוגים:
```bash
# צפייה בלוגים
tail -f trading_bot.log

# לוגים של Docker
docker-compose logs -f
```

### עדכונים:
```bash
# עדכון קוד
git pull origin main

# עדכון חבילות
pip install -r requirements_trading.txt --upgrade
```

### גיבויים:
```bash
# גבה הגדרות
cp .env .env.backup

# גבה מודלי AI
tar -czf models_backup.tar.gz trading_bot/ai/saved_models/

# גבה לוגים
cp trading_bot.log logs_backup/
```

## 🆘 קבלת עזרה

### משאבים:
- [תיעוד MetaTrader 5](https://www.mql5.com/en/docs)
- [תיעוד Python](https://docs.python.org/)
- [קהילת Telegram](https://t.me/your_bot_community)

### דיווח על בעיות:
1. פתח Issue ב-GitHub
2. צרף לוגים רלוונטיים
3. תאר את הבעיה בפירוט
4. ציין מערכת הפעלה וגרסאות

---

**✅ אחרי השלמת כל השלבים, הבוט שלך אמור לרוץ ולהיות נגיש מהטלפון!**

**🎉 בהצלחה במסחר! זכור - תמיד התחל עם חשבון דמו!**