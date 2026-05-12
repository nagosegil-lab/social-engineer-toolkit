# ZakenChance AI Android App

This folder contains a standalone Android app (Kotlin + Jetpack Compose) for the ZakenChance AI generator.

## Features

- Material 3 UI with dedicated tabs for Lotto and Chance
- Persistent local settings/input using DataStore (survives app restarts)
- Lotto history parsing with strict validation:
  - exactly 6 numbers
  - unique numbers
  - lotto range 1-37
  - strong range 1-7
- Lotto analysis:
  - hot numbers
  - cold numbers
  - common strong numbers
- Lotto generation modes:
  - Balanced Distribution
  - Anti-Crowd Mode
  - Hot + Cold Mix
  - Random
- Budget-aware ticket limits (`budget / ticket_price`)
- AI score transparency for each lotto ticket
- Chance history parsing and per-suit hot/cold analysis
- Chance generation modes:
  - Balanced Distribution
  - History Weighted
  - Hot + Cold Mix
  - Random
- CSV export via clipboard copy buttons (lotto/chance)
- Release signing support via Gradle properties

## Open and run

1. Open Android Studio.
2. Select **Open** and choose this folder: `android-zakenchance/`.
3. Let Gradle sync complete.
4. Run the `app` module on an Android device/emulator.

## Generate a signed APK

### 1) Create a keystore (one-time)

```bash
keytool -genkeypair \
  -v \
  -keystore zakenchance-release-key.jks \
  -alias zakenchance \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000
```

### 2) Configure signing secrets

Copy `signing.properties.example` values into your `~/.gradle/gradle.properties`
and replace with your real keystore path/passwords.

### 3) Build release APK

From Android Studio:
- **Build > Generate Signed Bundle / APK** and select APK.

Or via command line (inside `android-zakenchance/`):

```bash
./gradlew assembleRelease
```

Then pick up the artifact at:
`app/build/outputs/apk/release/app-release.apk`

If `gradlew` is missing in your local checkout, run the build from Android Studio
or generate a Gradle wrapper once (`gradle wrapper`) and rerun the command.
