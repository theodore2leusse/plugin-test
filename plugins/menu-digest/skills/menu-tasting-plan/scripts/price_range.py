#!/usr/bin/env python3
"""Fourchette de budget d'un menu degustation.

Lit sur stdin un JSON de la forme :

    {"courses": [{"name": "Poireaux vinaigrette", "price": 12}, ...],
     "guests": 4,          # optionnel, defaut 1
     "currency": "EUR"}    # optionnel, defaut "EUR"

Ecrit sur stdout total, minimum, maximum, mediane et budget par personne.
Un service sans cle "price" est exclu du calcul et signale. Bibliotheque
standard uniquement.
"""

import json
import statistics
import sys

SYMBOLS = {"EUR": "€", "USD": "$", "GBP": "£", "CHF": "CHF", "JPY": "¥"}


def fail(message):
    print(message, file=sys.stderr)
    raise SystemExit(1)


def amount(value, symbol):
    rounded = round(float(value), 2)
    text = str(int(rounded)) if rounded == int(rounded) else "{:.2f}".format(rounded)
    return "{} {}".format(text, symbol)


def load():
    raw = sys.stdin.read().strip()
    if not raw:
        fail("Aucune donnee sur stdin. Attendu : {\"courses\": [{\"name\": ..., \"price\": ...}]}")
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as error:
        fail("JSON invalide : {}. Attendu : {{\"courses\": [...]}}".format(error.msg))
    if not isinstance(payload, dict) or not isinstance(payload.get("courses"), list):
        fail("Structure inattendue. Attendu un objet avec une liste \"courses\".")
    if not payload["courses"]:
        fail("La liste \"courses\" est vide : aucun service a chiffrer.")
    return payload


def split_courses(courses):
    priced, unpriced = [], []
    for index, course in enumerate(courses, start=1):
        if not isinstance(course, dict):
            unpriced.append("service {} (format inattendu)".format(index))
            continue
        name = str(course.get("name") or "service {}".format(index))
        price = course.get("price")
        if isinstance(price, bool) or not isinstance(price, (int, float)):
            unpriced.append(name)
        else:
            priced.append((name, float(price)))
    return priced, unpriced


def guest_count(payload):
    guests = payload.get("guests", 1)
    if isinstance(guests, bool) or not isinstance(guests, int) or guests < 1:
        return 1, guests if guests != 1 else None
    return guests, None


def main():
    payload = load()
    courses = payload["courses"]
    symbol = SYMBOLS.get(str(payload.get("currency", "EUR")).upper(), str(payload.get("currency", "EUR")))
    priced, unpriced = split_courses(courses)
    guests, bad_guests = guest_count(payload)

    lines = ["{} service(s), {} prix affiche(s).".format(len(courses), len(priced)), ""]

    if not priced:
        lines.append("Aucun prix affiche : budget non calculable.")
        lines.append("Ne pas estimer les prix, l'annoncer a l'utilisateur.")
    else:
        prices = [price for _, price in priced]
        cheapest = min(priced, key=lambda item: item[1])
        dearest = max(priced, key=lambda item: item[1])
        lines.append("Total (budget par personne) : {}".format(amount(sum(prices), symbol)))
        lines.append("Service le moins cher       : {} ({})".format(amount(cheapest[1], symbol), cheapest[0]))
        lines.append("Service le plus cher        : {} ({})".format(amount(dearest[1], symbol), dearest[0]))
        lines.append("Prix median                 : {}".format(amount(statistics.median(prices), symbol)))
        if guests > 1:
            lines.append("")
            lines.append("Budget pour {} personnes : {}".format(guests, amount(sum(prices) * guests, symbol)))

    if unpriced:
        lines.append("")
        lines.append("Sans prix affiche, exclu(s) du calcul : {}".format(", ".join(unpriced)))
        if priced:
            lines.append("Le total ci-dessus est donc un plancher, pas le prix final.")

    if bad_guests is not None:
        lines.append("")
        lines.append("Valeur \"guests\" ignoree ({!r}) : calcul fait pour 1 personne.".format(bad_guests))

    print("\n".join(lines))


if __name__ == "__main__":
    main()
