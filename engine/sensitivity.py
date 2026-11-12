from engine.analyze import analyze_deal

PRICE_STEPS = (-0.10, -0.05, 0.0, 0.05, 0.10)
RATE_STEPS = (-0.010, -0.005, 0.0, 0.005, 0.010)


def two_way_irr(deal, price_steps=PRICE_STEPS, rate_steps=RATE_STEPS):
    """
    IRR grid by interest rate (rows) and purchase price (columns),
    matching the v2 2-way sensitivity table. Rental deals only.
    """
    prices = [deal["price"] * (1 + p) for p in price_steps]
    rates = [deal["annual_rate"] + r for r in rate_steps]
    grid = []
    for rate in rates:
        row = []
        for price in prices:
            result = analyze_deal(**{**deal, "price": price, "annual_rate": rate})
            row.append(result["irr"])
        grid.append(row)
    return {"prices": prices, "rates": rates, "irr": grid}


from engine.assumptions import get_assumptions

# (label, where it lives, key, swing, how the swing applies) - v2 Sensitivity_Analysis A2:D8
TORNADO_VARS = [
    ("Purchase price", "input", "price", 0.10, "relative"),
    ("Interest rate", "input", "annual_rate", 0.01, "points"),
    ("Monthly rent", "input", "base_rent", 0.10, "relative"),
    ("Vacancy rate", "assumption", "VacancyRate% Annual", 0.03, "points"),
    ("Appreciation", "assumption", "Appreciation Annual", 0.015, "points"),
    ("Rent growth", "assumption", "RentGrowth Annual", 0.01, "points"),
    ("Rehab cost", "input", "rehab", 0.25, "relative"),
]


# money inputs show as $; everything else is a rate shown as %
_DOLLARS = {"price", "base_rent", "rehab", "arv"}


def _unit(key):
    return "$" if key in _DOLLARS else "%"


def _shift(value, swing, how, sign):
    if how == "relative":
        return value * (1 + sign * swing)
    return value + sign * swing


def tornado_irr(deal):
    """
    IRR at the low and high swing of each v2 tornado variable, sorted
    by swing width (largest first). Rental deals only.
    """
    base = analyze_deal(**deal)["irr"]
    a = get_assumptions(deal["state"], deal["property_type"], "Rental", deal["scenario"])
    rows = []
    for label, where, key, swing, how in TORNADO_VARS:
        irrs, tested = [], []
        start = deal[key] if where == "input" else a[key]
        for sign in (-1, 1):
            new = _shift(start, swing, how, sign)
            tested.append(new)
            if where == "input":
                irrs.append(analyze_deal(**{**deal, key: new})["irr"])
            else:
                irrs.append(analyze_deal(**deal, overrides={key: new})["irr"])
        rows.append({"variable": label, "low": irrs[0], "high": irrs[1],
                     # the input values tested, so the page can show them
                     "low_value": tested[0], "high_value": tested[1],
                     "base_value": start, "unit": _unit(key)})
    rows.sort(key=lambda r: abs(r["high"] - r["low"]), reverse=True)
    return {"base": base, "rows": rows}

# BRRR levers named in v2's sensitivity message box; swings are v3 choices
BRRR_TORNADO_VARS = [
    ("ARV", "arv", 0.10, "relative"),
    ("Refi LTV", "refi_ltv", 0.05, "points"),
    ("Post-refi rate", "post_refi_rate", 0.01, "points"),
    ("Monthly rent", "base_rent", 0.10, "relative"),
    ("Purchase price", "price", 0.10, "relative"),
    ("Rehab cost", "rehab", 0.25, "relative"),
]


def brrr_tornado_irr(deal):
    """
    IRR at the low and high swing of each BRRR lever, sorted by swing
    width. Rows where either swing makes the deal all-cash-out are
    flagged, because their IRR is not comparable.
    """
    base = analyze_deal(**deal)
    rows = []
    for label, key, swing, how in BRRR_TORNADO_VARS:
        tested = [_shift(deal[key], swing, how, sign) for sign in (-1, 1)]
        runs = [analyze_deal(**{**deal, key: v}) for v in tested]
        rows.append({"variable": label,
                     "low": runs[0]["irr"], "high": runs[1]["irr"],
                     "low_value": tested[0], "high_value": tested[1],
                     "base_value": deal[key], "unit": _unit(key),
                     "all_cash_out": runs[0]["all_cash_out"] or runs[1]["all_cash_out"]})
    rows.sort(key=lambda r: abs(r["high"] - r["low"]), reverse=True)
    return {"base": base["irr"], "base_all_cash_out": base["all_cash_out"],
            "rows": rows}