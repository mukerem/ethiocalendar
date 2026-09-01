# ethiocalendar

[![PyPI version](https://img.shields.io/pypi/v/ethiocalendar.svg)](https://pypi.org/project/ethiocalendar/)
[![Downloads](https://static.pepy.tech/badge/ethiocalendar)](https://pepy.tech/projects/ethiocalendar)
[![Python](https://img.shields.io/pypi/pyversions/ethiocalendar.svg)](https://pypi.org/project/ethiocalendar/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.txt)

**ethiocalendar** is a Python date and time library for the **Ethiopian calendar**.
It converts between **Ethiopian** and **Gregorian** dates, detects leap years, and
exposes `date` / `datetime` objects that mirror the standard library.

Conversion uses the same Ethiopic Amete Mihret epoch as Unicode ICU
(`JD_EPOCH_OFFSET_AMETE_MIHRET = 1723856`, Beyene–Kudlek).

Current release: **1.2.0** (Python 3.6+).

---

## Installation

```bash
pip install -U ethiocalendar
```

---

## What's new in 1.2.0

- More accurate Ethiopian ↔ Gregorian conversion (ICU / Beyene–Kudlek epoch)
- Gregorian → Ethiopian no longer fails on Pagume 5 of non-leap years
- `datetime.togregorian()` and Pagume `strftime` work correctly
- Documented tuple helpers: `to_gregorian`, `from_gregorian`, `today`, `is_leap_year`
- Existing methods such as `date.togregorian()` and `fromgretoethio()` are unchanged

---

## Features

- Convert **Ethiopian → Gregorian** and **Gregorian → Ethiopian**
- `date` and `datetime` objects with the familiar standard-library methods
- Today's date in both calendars
- Ethiopian leap years (Pagume 6 when `year % 4 == 3`)
- Round-trip conversions, including Pagume

---

## Quick examples

### Object API (existing, unchanged)

```python
import datetime
import ethiocalendar as ec

# Meskerem 1, 2012 EC → September 12, 2019 GC
print(ec.date(2012, 1, 1).togregorian())
# datetime.date(2019, 9, 12)

print(ec.fromgretoethio(datetime.date(2025, 11, 12)))
# ethiocalendar.date(2018, 3, 3)

print(ec.date.today())
print(ec.is_puagume6(2011))  # True
```

### Convenience functions

```python
import ethiocalendar as ec

print(ec.to_gregorian(2012, 1, 1))
# (2019, 9, 12)

print(ec.from_gregorian(2025, 11, 12))
# (2018, 3, 3)

print(ec.today())
# (year, month, day) in the Ethiopian calendar

print(ec.is_leap_year(2011))  # True
print(ec.is_leap_year(2012))  # False
```

### Round-trip

```python
import ethiocalendar as ec

date_ec = (2012, 1, 1)
to_gc = ec.to_gregorian(*date_ec)
back_ec = ec.from_gregorian(*to_gc)
assert date_ec == back_ec
```

---

## Calendar notes

- The Ethiopian year has **13 months**: 12 × 30 days, plus **Pagume** (5 days, or 6 in a leap year).
- Leap years occur every 4 years when `year % 4 == 3`.
- **Meskerem 1** falls on **11 September** in the Gregorian calendar, or **12 September** when the following Gregorian year is a leap year. That shortcut holds for Ethiopian years 1900–2091. Because the Ethiopian calendar does not skip century leap days, New Year drifts by one Gregorian day after 2100 (which is not a Gregorian leap year).

---

## Tests

```bash
pytest -q
```

---

## Links

- PyPI: https://pypi.org/project/ethiocalendar/
- Downloads: https://pepy.tech/projects/ethiocalendar
- Source: https://github.com/mukerem/ethiocalendar

---

## Author

**Mukerem Ali Nur**
[GitHub](https://github.com/mukerem/ethiocalendar) · [PyPI](https://pypi.org/project/ethiocalendar) · [Downloads](https://pepy.tech/projects/ethiocalendar)
