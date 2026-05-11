# ZakenChance AI Android App

This folder contains a standalone Android app (Kotlin + Jetpack Compose) for the ZakenChance AI generator.

## Features

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

## Open and run

1. Open Android Studio.
2. Select **Open** and choose this folder: `android-zakenchance/`.
3. Let Gradle sync complete.
4. Run the `app` module on an Android device/emulator.
