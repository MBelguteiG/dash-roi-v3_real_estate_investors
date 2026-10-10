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