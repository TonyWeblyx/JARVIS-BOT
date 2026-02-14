"""
CLAUDE LIMIT COUNTER pro Masika
Spusť ráno, klikej po každém chatu s Claude.
Ukáže ti kolik zpráv ti zhruba zbývá.

Spuštění: python limit-counter.py
"""

import json
import os
from datetime import datetime, date

SAVE_FILE = "counter.json"
# Claude Pro ~ 45 zpráv Opus / ~100 zpráv Sonnet denně (přibližně)
DAILY_LIMIT_OPUS = 45
DAILY_LIMIT_SONNET = 100


def load_data():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        if data.get("date") != str(date.today()):
            return {"date": str(date.today()), "opus": 0, "sonnet": 0}
        return data
    return {"date": str(date.today()), "opus": 0, "sonnet": 0}


def save_data(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)


def show_status(data):
    opus_left = max(0, DAILY_LIMIT_OPUS - data["opus"])
    sonnet_left = max(0, DAILY_LIMIT_SONNET - data["sonnet"])

    print(f"\n{'='*40}")
    print(f"  CLAUDE LIMIT COUNTER - {data['date']}")
    print(f"{'='*40}")
    print(f"  Opus:   {data['opus']}/{DAILY_LIMIT_OPUS} použito | {opus_left} zbývá")
    print(f"  Sonnet: {data['sonnet']}/{DAILY_LIMIT_SONNET} použito | {sonnet_left} zbývá")
    print(f"{'='*40}")

    if opus_left <= 5:
        print("  ⚠️  POZOR! Opus zprávy dochází! Přepni na Sonnet.")
    if opus_left <= 0:
        print("  🛑 STOP! Opus limit vyčerpán. Pokračuj zítra nebo na Sonnetu.")
    if opus_left > 5:
        print(f"  ✅ V pohodě, ještě máš {opus_left} Opus zpráv.")
    print()


def main():
    data = load_data()
    print("\nClaude Limit Counter")
    print("Počítej si zprávy ať nepřečerpáš denní limit.\n")

    while True:
        show_status(data)
        print("Co chceš zapsat?")
        print("  [1] Poslal jsem zprávu na Opus")
        print("  [2] Poslal jsem zprávu na Sonnet")
        print("  [3] Poslal jsem chat (víc zpráv najednou)")
        print("  [r] Reset na dnešek")
        print("  [q] Konec")

        choice = input("\n> ").strip().lower()

        if choice == "1":
            data["opus"] += 1
            save_data(data)
        elif choice == "2":
            data["sonnet"] += 1
            save_data(data)
        elif choice == "3":
            try:
                n = int(input("Kolik zpráv? "))
                model = input("Model? [o]pus / [s]onnet: ").strip().lower()
                if model in ["o", "opus"]:
                    data["opus"] += n
                else:
                    data["sonnet"] += n
                save_data(data)
            except ValueError:
                print("Zadej číslo!")
        elif choice == "r":
            data = {"date": str(date.today()), "opus": 0, "sonnet": 0}
            save_data(data)
            print("Resetováno!")
        elif choice == "q":
            print("Čau! Šetři limity!")
            break


if __name__ == "__main__":
    main()
