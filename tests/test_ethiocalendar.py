
import importlib
import datetime as _dt
import pytest

# Try to import the package
ec = importlib.import_module("ethiocalendar")

# --- Helpers: attempt multiple likely API shapes --------------------------------
def _to_gregorian(y, m, d):
    # Function names (in order of likelihood)
    for fname in [
        "to_gregorian",
        "ethiopian_to_gregorian",
        "convert_to_gregorian",
        "toGregorian",
        "eth_to_greg",
    ]:
        f = getattr(ec, fname, None)
        if callable(f):
            res = f(y, m, d)
            # normalize result into (Y,M,D) tuple
            if isinstance(res, tuple) and len(res) == 3:
                return tuple(int(x) for x in res)
            if hasattr(res, "year") and hasattr(res, "month") and hasattr(res, "day"):
                return (int(res.year), int(res.month), int(res.day))
    # Class shapes
    for cname, method in [
        ("EthiopianDate", "to_gregorian"),
        ("EthiopicDate", "to_gregorian"),
        ("EthDate", "to_gregorian"),
    ]:
        C = getattr(ec, cname, None)
        if C is not None:
            obj = C(y, m, d)
            meth = getattr(obj, method, None)
            if callable(meth):
                res = meth()
                if isinstance(res, tuple) and len(res) == 3:
                    return tuple(int(x) for x in res)
                if hasattr(res, "year") and hasattr(res, "month") and hasattr(res, "day"):
                    return (int(res.year), int(res.month), int(res.day))
    raise AttributeError("Could not find a usable API to convert Ethiopian→Gregorian")

def _to_ethiopian(y, m, d):
    for fname in [
        "from_gregorian",
        "gregorian_to_ethiopian",
        "convert_to_ethiopian",
        "toEthiopian",
        "greg_to_eth",
    ]:
        f = getattr(ec, fname, None)
        if callable(f):
            res = f(y, m, d)
            if isinstance(res, tuple) and len(res) == 3:
                return tuple(int(x) for x in res)
            if hasattr(res, "year") and hasattr(res, "month") and hasattr(res, "day"):
                return (int(res.year), int(res.month), int(res.day))
    for cname, method in [
        ("GregorianDate", "to_ethiopian"),
        ("GregDate", "to_ethiopian"),
    ]:
        C = getattr(ec, cname, None)
        if C is not None:
            obj = C(y, m, d)
            meth = getattr(obj, method, None)
            if callable(meth):
                res = meth()
                if isinstance(res, tuple) and len(res) == 3:
                    return tuple(int(x) for x in res)
                if hasattr(res, "year") and hasattr(res, "month") and hasattr(res, "day"):
                    return (int(res.year), int(res.month), int(res.day))
    raise AttributeError("Could not find a usable API to convert Gregorian→Ethiopian")

# --- Canonical anchors (widely-agreed facts) ------------------------------------
# 1) Ethiopian New Year (Meskerem 1) is Sep 11 Gregorian, except it shifts to Sep 12
#    when the following Gregorian year is a leap year.
#    Example: 2012 EC began on 2019-09-12 (since 2020 was Gregorian leap).
# 2) Ethiopian leap years occur every 4 years; Pagume has 6 days in leap years.
#    A common rule of thumb: EC year Y is leap if Y % 4 == 3.

@pytest.mark.parametrize("ec_date, greg_date", [
    # Meskerem 1, 2011 EC → 2018‑09‑11 G
    ((2011, 1, 1), (2018, 9, 11)),
    # Meskerem 1, 2012 EC → 2019‑09‑12 G (shift due to 2020 leap)
    ((2012, 1, 1), (2019, 9, 12)),
    # Pagume 6, 2011 EC (leap year) → 2019‑09‑11 G (last day of the EC year)
    ((2011, 13, 6), (2019, 9, 11)),
    # Pagume 5, 2015 EC (non‑leap year) → 2023‑09‑10 G
    ((2015, 13, 5), (2023, 9, 10)),
])
def test_eth_to_greg_anchors(ec_date, greg_date):
    y, m, d = ec_date
    assert _to_gregorian(y, m, d) == greg_date

@pytest.mark.parametrize("greg_date, ec_date", [
    # 2025‑11‑12 G → 2018‑Hidar‑3 EC
    ((2025, 11, 12), (2018, 3, 3)),
    # 2019‑09‑12 G → 2012‑Meskerem‑1 EC
    ((2019, 9, 12), (2012, 1, 1)),
    # 2019‑09‑11 G → 2011‑Pagume‑6 EC
    ((2019, 9, 11), (2011, 13, 6)),
    # 2023‑09‑10 G → 2015‑Pagume‑5 EC
    ((2023, 9, 10), (2015, 13, 5)),
])
def test_greg_to_eth_anchors(greg_date, ec_date):
    y, m, d = greg_date
    assert _to_ethiopian(y, m, d) == ec_date

@pytest.mark.parametrize("ec_date", [
    (2011, 1, 1),
    (2012, 1, 1),
    (2015, 13, 5),
    (2011, 13, 6),
    (2018, 3, 3),
])
def test_round_trip(ec_date):
    y, m, d = ec_date
    gy, gm, gd = _to_gregorian(y, m, d)
    y2, m2, d2 = _to_ethiopian(gy, gm, gd)
    assert (y, m, d) == (y2, m2, d2)
