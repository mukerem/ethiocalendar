import datetime as gregorian
import pickle

import pytest

import ethiocalendar as ec


def _iter_eth_dates(year0, year1):
    for year in range(year0, year1 + 1):
        for month in range(1, 14):
            dim = 6 if (month == 13 and year % 4 == 3) else (5 if month == 13 else 30)
            for day in range(1, dim + 1):
                yield year, month, day


# --- Canonical anchors -------------------------------------------------------

@pytest.mark.parametrize("ec_date, greg_date", [
    ((2011, 1, 1), (2018, 9, 11)),
    ((2012, 1, 1), (2019, 9, 12)),
    ((2011, 13, 6), (2019, 9, 11)),
    ((2015, 13, 5), (2023, 9, 10)),
    ((2018, 3, 3), (2025, 11, 12)),
    ((1, 1, 1), (8, 8, 27)),
])
def test_eth_to_greg_anchors_object_api(ec_date, greg_date):
    got = ec.date(*ec_date).togregorian()
    assert (got.year, got.month, got.day) == greg_date


@pytest.mark.parametrize("ec_date, greg_date", [
    ((2011, 1, 1), (2018, 9, 11)),
    ((2012, 1, 1), (2019, 9, 12)),
    ((2011, 13, 6), (2019, 9, 11)),
    ((2015, 13, 5), (2023, 9, 10)),
    ((2018, 3, 3), (2025, 11, 12)),
])
def test_eth_to_greg_anchors_tuple_api(ec_date, greg_date):
    assert ec.to_gregorian(*ec_date) == greg_date


@pytest.mark.parametrize("greg_date, ec_date", [
    ((2025, 11, 12), (2018, 3, 3)),
    ((2019, 9, 12), (2012, 1, 1)),
    ((2019, 9, 11), (2011, 13, 6)),
    ((2023, 9, 10), (2015, 13, 5)),
    ((2024, 9, 10), (2016, 13, 5)),  # previously crashed
    ((8, 8, 27), (1, 1, 1)),
])
def test_greg_to_eth_anchors(greg_date, ec_date):
    obj = ec.fromgretoethio(gregorian.date(*greg_date))
    assert (obj.year, obj.month, obj.day) == ec_date
    assert ec.from_gregorian(*greg_date) == ec_date


def test_round_trip_object_and_tuple_api():
    for ec_date in [(2011, 1, 1), (2012, 1, 1), (2015, 13, 5), (2011, 13, 6), (2018, 3, 3), (2016, 13, 5)]:
        gy, gm, gd = ec.to_gregorian(*ec_date)
        assert ec.from_gregorian(gy, gm, gd) == ec_date
        g = ec.date(*ec_date).togregorian()
        back = ec.fromgretoethio(g)
        assert (back.year, back.month, back.day) == ec_date


def test_pagume5_of_non_leap_year_converts_both_ways():
    # year % 4 == 0, Pagume 5 used to make _ord2ymd return month 0
    for year in (4, 8, 1992, 2012, 2016, 2020):
        eth = ec.date(year, 13, 5)
        g = eth.togregorian()
        back = ec.fromgretoethio(g)
        assert (back.year, back.month, back.day) == (year, 13, 5)


def test_date_arithmetic_across_pagume5():
    start = ec.date(2016, 13, 4)
    nxt = start + ec.timedelta(days=1)
    assert (nxt.year, nxt.month, nxt.day) == (2016, 13, 5)
    nxt2 = nxt + ec.timedelta(days=1)
    assert (nxt2.year, nxt2.month, nxt2.day) == (2017, 1, 1)


def test_ordinal_inverse_exhaustive_early_years():
    for y, m, d in _iter_eth_dates(1, 40):
        n = ec.date(y, m, d).toordinal()
        y2, m2, d2 = ec.date.fromordinal(n).year, ec.date.fromordinal(n).month, ec.date.fromordinal(n).day
        assert (y2, m2, d2) == (y, m, d)


def test_round_trip_modern_range():
    for y, m, d in _iter_eth_dates(1890, 2030):
        g = ec.date(y, m, d).togregorian()
        back = ec.fromgretoethio(g)
        assert (back.year, back.month, back.day) == (y, m, d)


def test_datetime_togregorian_preserves_clock():
    dt = ec.datetime(2012, 1, 1, 8, 30, 15, 123456)
    g = dt.togregorian()
    assert isinstance(g, gregorian.datetime)
    assert (g.year, g.month, g.day) == (2019, 9, 12)
    assert (g.hour, g.minute, g.second, g.microsecond) == (8, 30, 15, 123456)
    back = ec.fromgretoethio(g)
    assert (back.year, back.month, back.day) == (2012, 1, 1)
    assert (back.hour, back.minute, back.second, back.microsecond) == (8, 30, 15, 123456)


def test_strftime_pagume_and_month_names():
    pagume = ec.date(2011, 13, 6)
    assert pagume.strftime("%Y-%m-%d") == "2011-13-06"
    assert pagume.strftime("%B") == "Puagme"
    meskerem = ec.date(2012, 1, 1)
    assert meskerem.strftime("%Y-%m-%d") == "2012-01-01"
    assert meskerem.strftime("%B") == "Meskerem"


def test_leap_year_helpers():
    assert ec.is_puagume6(2011) is True
    assert ec.is_leap_year(2011) is True
    assert ec.is_leap_year(2012) is False
    assert ec.is_puagume6(2012) is False


def test_today_matches_system_gregorian():
    g = gregorian.date.today()
    assert ec.fromgretoethio(g).togregorian() == g
    eth_obj = ec.date.today()
    assert ec.today() == (eth_obj.year, eth_obj.month, eth_obj.day)


def test_datetime_now_converts_to_today():
    now = ec.datetime.now()
    assert now.date() == ec.date.today()


def test_timestamp_matches_gregorian_instant():
    eth = ec.datetime.now()
    g = eth.togregorian()
    assert abs(eth.timestamp() - g.timestamp()) < 1e-3


def test_pickle_pagume_date_and_datetime():
    d = ec.date(2011, 13, 6)
    assert pickle.loads(pickle.dumps(d)) == d
    dt = ec.datetime(2011, 13, 6, 12, 0)
    assert pickle.loads(pickle.dumps(dt)) == dt


def test_weekday_matches_converted_gregorian():
    eth = ec.date(2012, 1, 1)
    assert eth.weekday() == eth.togregorian().weekday()


def test_new_year_modern_shortcut():
    assert ec.to_gregorian(2011, 1, 1) == (2018, 9, 11)
    assert ec.to_gregorian(2012, 1, 1) == (2019, 9, 12)


def test_public_names_still_present():
    for name in (
        "date", "datetime", "time", "timedelta", "timezone", "tzinfo",
        "fromgretoethio", "is_puagume6", "ETHIOORIGINALDAYDELAY",
        "to_gregorian", "from_gregorian", "today", "is_leap_year",
        "ETHIOPIAN_EPOCH_JDN",
    ):
        assert hasattr(ec, name)


def test_epoch_constant():
    assert ec.ETHIOPIAN_EPOCH_JDN == 1723856
    assert ec.ETHIOORIGINALDAYDELAY == 2795
    g = ec.date(1, 1, 1).togregorian()
    # JDN = python ordinal + 1721425
    assert g.toordinal() + 1721425 == 1724221
