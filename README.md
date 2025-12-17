````markdown
# 🗓️ ethiocalendar

**ethiocalendar** is a lightweight and easy-to-use Python library for handling the **Ethiopian calendar system**.  
It supports converting between **Ethiopian** and **Gregorian** dates, determining leap years, and getting today’s date in both calendars.

---

## 🚀 Installation

Install directly from PyPI:

```bash
pip install ethiocalendar
```
````

---

## ✨ Features

- Convert **Ethiopian → Gregorian** and **Gregorian → Ethiopian**
- Get **today’s date** in both calendars
- Detect **Ethiopian leap years**
- Handle **Pagume** (13th month) and its 5/6-day rule
- Support for **round-trip conversions**
- Fully tested and easy to integrate in projects

---

## 📘 Quick Examples

### 1️⃣ Ethiopian → Gregorian

```python
import ethiocalendar as ec

# Meskerem 1, 2012 EC → September 12, 2019 GC
print(ec.to_gregorian(2012, 1, 1))
# Output: (2019, 9, 12)
```

---

### 2️⃣ Gregorian → Ethiopian

```python
import ethiocalendar as ec

# November 12, 2025 GC → Hidar 3, 2018 EC
print(ec.from_gregorian(2025, 11, 12))
# Output: (2018, 3, 3)
```

---

### 3️⃣ Get Today’s Ethiopian Date

```python
import ethiocalendar as ec

today_ec = ec.today()  # returns (year, month, day)
print("Today (Ethiopian):", today_ec)
```

Output example:

```
Today (Ethiopian): (2018, 3, 3)
```

---

### 4️⃣ Get Today’s Gregorian Date from Ethiopian Calendar

```python
import ethiocalendar as ec

# Get current Ethiopian date and convert it back to Gregorian
y, m, d = ec.today()
print(ec.to_gregorian(y, m, d))
```

---

### 5️⃣ Check if a Year Is Leap Year (Ethiopian Rule)

```python
import ethiocalendar as ec

print(ec.is_leap_year(2011))  # True
print(ec.is_leap_year(2012))  # False
```

---

### 6️⃣ Round-Trip Conversion Check

```python
import ethiocalendar as ec

date_ec = (2012, 1, 1)
to_gc = ec.to_gregorian(*date_ec)
back_ec = ec.from_gregorian(*to_gc)

assert date_ec == back_ec
print("Round-trip successful:", back_ec)
```

---

## 📅 Calendar Notes

- The Ethiopian year has **13 months**:

  - **12 months × 30 days**
  - **Pagume** (13th month) has **5 days**, or **6** in a leap year.

- Leap years occur every 4 years when `year % 4 == 3`.
- **New Year’s Day (መስከረም 1)** falls on:

  - **September 11** (Gregorian)
  - or **September 12** before a Gregorian leap year.

---

## 🧪 Tests

Tests are included under `tests/` and can be run with:

```bash
pytest -q
```

The test suite verifies:

- Known anchor dates (Meskerem 1 ↔ Sept 11/12)
- Pagume leap-year boundaries
- Round-trip conversions
- Randomized correctness checks

---

## 🧑‍💻 Author

**Mukerem Ali Nur**
[GitHub ↗](https://github.com/mukerem) | [PyPI ↗](https://pypi.org/project/ethiocalendar)
