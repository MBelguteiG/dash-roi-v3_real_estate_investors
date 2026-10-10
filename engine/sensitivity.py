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
        irrs = []
        for sign in (-1, 1):
            if where == "input":
                new = _shift(deal[key], swing, how, sign)
                irrs.append(analyze_deal(**{**deal, key: new})["irr"])
            else:
                new = _shift(a[key], swing, how, sign)
                irrs.append(analyze_deal(**deal, overrides={key: new})["irr"])
        rows.append({"variable": label, "low": irrs[0], "high": irrs[1]})
    rows.sort(key=lambda r: abs(r["high"] - r["low"]), reverse=True)
    return {"base": base, "rows": rows}