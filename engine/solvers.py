"""
Solvers for Dash ROI v3 - Phase 3.

max_price_irr: highest purchase price that still hits the target IRR.
Ports v2 Find_Max_Price (Module5): bracket-expand + bisection. v3 solves
to the cent; v2 stops when |IRR - target| < 0.0001, so v2's displayed price
is "close enough", not exact.

Assumes IRR falls as price rises (true for Rental and BRRR: a higher price
means more cash in, a bigger loan, and higher taxes against the same rent).
Every price is tested through analyze_deal() - the same path the UI uses.
"""

from engine.analyze import analyze_deal
from engine.verdict import DSCR_LENDER_MIN
from engine.assumptions import get_assumptions


def metric_at_price(inputs, price, metric):
    """Re-run the whole deal at a different purchase price; return one output."""
    return analyze_deal(**{**inputs, "price": price})[metric]


def irr_at_price(inputs, price):
    return metric_at_price(inputs, price, "irr")


def _solve_max_price(inputs, metric, target, tol=0.01, max_iter=200):
    """
    Shared bracket-expand + bisection. Highest price where metric >= target.
    Assumes the metric falls as price rises. Returns the price, or None.
    """
    base = inputs["price"]
    lo = hi = base
    if metric_at_price(inputs, base, metric) >= target:
        while metric_at_price(inputs, hi, metric) >= target:     # search upward
            lo = hi
            hi *= 1.5
            if hi > base * 100:
                return None
    else:
        while metric_at_price(inputs, lo, metric) < target:      # search downward
            hi = lo
            lo *= 0.5
            if lo < 1000:
                return None

    for _ in range(max_iter):
        if hi - lo <= tol:
            break
        mid = (lo + hi) / 2
        if metric_at_price(inputs, mid, metric) >= target:
            lo = mid
        else:
            hi = mid
    return lo


def _refused(reason):
    return {"status": "REFUSED", "price": None, "value_at_price": None, "reason": reason}


def _no_solution():
    return {"status": "NO SOLUTION", "price": None, "value_at_price": None,
            "reason": "no price in search range hits the target"}


def max_price_irr(inputs, target_irr=None):
    """Highest price that still hits the target IRR (v2 Find_Max_Price, Module5)."""
    if inputs["model"] == "Flip":
        return _refused("Flip has no IRR - use Max Offer (MAO)")
    target = inputs["target_irr"] if target_irr is None else target_irr
    price = _solve_max_price(inputs, "irr", target)
    if price is None:
        return _no_solution()
    return {"status": "SOLVED", "price": price,
            "value_at_price": irr_at_price(inputs, price), "reason": ""}


def max_price_dscr(inputs, dscr_min=DSCR_LENDER_MIN):
    """
    Highest price where min DSCR still meets the lender minimum
    (v2 Find_Max_Price_Lender, Module3). Rental only.
    """
    if inputs["model"] == "BRRR":
        return _refused("BRRR refi is sized off ARV - price can't move post-refi "
                        "DSCR; use Max Price All-Cash-Out")
    if inputs["model"] == "Flip":
        return _refused("Flip has no DSCR - use Max Offer (MAO)")
    price = _solve_max_price(inputs, "min_dscr", dscr_min)
    if price is None:
        return _no_solution()
    return {"status": "SOLVED", "price": price,
            "value_at_price": metric_at_price(inputs, price, "min_dscr"), "reason": ""}

def max_price_all_cash_out(inputs):
    """
    BRRR only. Highest purchase price where the refi returns ALL invested
    cash - cash left in deal = 0, using v3's existing BRRR definition:
        cash left = (price + rehab + closing - HM loan) - (refi loan - HM loan)
                  = price x (1 + closing %) + rehab - refi loan
    That is linear in price, so it solves exactly (no bisection needed):
        price = (ARV x refi LTV - rehab) / (1 + closing %)
    v2 Main_Dashboard B50 gives $518,450 on the reference deal: it also
    subtracts Flip-block HM interest (5-mo hold) and points, evaluated at the
    CURRENT price, so it isn't self-consistent. Documented divergence.
    """
    if inputs["model"] != "BRRR":
        return _refused("All-cash-out applies to BRRR only")
    a = get_assumptions(inputs["state"], inputs["property_type"], "BRRR",
                        inputs["scenario"])
    closing_pct = a["Closing Cost Buying"]
    price = (inputs["arv"] * inputs["refi_ltv"] - inputs["rehab"]) / (1 + closing_pct)
    if price <= 0:
        return _no_solution()
    return {"status": "SOLVED", "price": price,
            "value_at_price": metric_at_price(inputs, price, "cash_left"), "reason": ""}


# --- Self-consistency tests ---
if __name__ == "__main__":
    from engine.crosscheck import DEALS

    rental = DEALS["Rental"]   # IL deal: IRR -5.39% at $250,000

    print("=== Max Price IRR - self-consistency ===\n")

    # Test 1: target ABOVE current IRR -> answer must be BELOW $250,000
    r = max_price_irr(rental, target_irr=0.15)
    print(f"Target 15%:  {r['status']}  price ${r['price']:,.2f}  "
          f"IRR there {r['value_at_price']*100:.4f}%")

    # Test 2: target BELOW current IRR -> answer must be ABOVE $250,000
    r2 = max_price_irr(rental, target_irr=-0.10)
    print(f"Target -10%: {r2['status']}  price ${r2['price']:,.2f}  "
          f"IRR there {r2['value_at_price']*100:.4f}%")

    # Test 3: one dollar more must MISS the target (proves it's the maximum)
    over = irr_at_price(rental, r["price"] + 1)
    print(f"$1 above the 15% answer: IRR {over*100:.4f}%  (must be < 15%)")

    # Test 4: Flip must refuse
    f = max_price_irr(DEALS["Flip"])
    print(f"Flip: {f['status']} - {f['reason']}")

    # Test 5: BRRR - target ABOVE current IRR (7.40%) -> price BELOW $650,000
    brrr = DEALS["BRRR"]
    b = max_price_irr(brrr, target_irr=0.13)
    print(f"\nBRRR target 13%: {b['status']}  price ${b['price']:,.2f}  "
          f"IRR there {b['value_at_price']*100:.4f}%")

    # Test 6: BRRR - target BELOW current IRR -> price ABOVE $650,000
    b2 = max_price_irr(brrr, target_irr=0.05)
    print(f"BRRR target 5%:  {b2['status']}  price ${b2['price']:,.2f}  "
          f"IRR there {b2['value_at_price']*100:.4f}%")

    # Test 7: v2 cross-check - CA Rental $650K deal (v2 B4=Rental: IRR 1.82%, target 13%)
    ca_rental = dict(model="Rental", state="California", property_type="Townhouse",
                     scenario="Base", price=650000, down_pct=0.15, annual_rate=0.071,
                     rehab=25000, base_rent=4500, exit_year=5, target_irr=0.13)
    base_irr = analyze_deal(**ca_rental)["irr"]
    print(f"\nCA Rental at $650,000: v3 IRR {base_irr*100:.2f}%   (v2 B27: 1.82%)")
    r7 = max_price_irr(ca_rental)
    print(f"CA Rental max price for 13%: {r7['status']}  ${r7['price']:,.2f}  "
          f"IRR there {r7['value_at_price']*100:.4f}%")

        # --- Max Price DSCR ---
    print("\n=== Max Price DSCR ===\n")
    d = max_price_dscr(ca_rental)
    print(f"CA Rental max price for DSCR 1.20: {d['status']}  ${d['price']:,.2f}  "
          f"min DSCR there {d['value_at_price']:.6f}")
    over_d = metric_at_price(ca_rental, d["price"] + 1, "min_dscr")
    print(f"$1 above: min DSCR {over_d:.6f}  (must be < 1.20)")
    print(f"BRRR: {max_price_dscr(DEALS['BRRR'])['status']}")
    print(f"Flip: {max_price_dscr(DEALS['Flip'])['status']}")


        # --- Max Price All-Cash-Out (BRRR) ---
    print("\n=== Max Price All-Cash-Out (BRRR) ===\n")
    ac = max_price_all_cash_out(DEALS["BRRR"])
    print(f"BRRR all-cash-out price: {ac['status']}  ${ac['price']:,.2f}  "
          f"cash left there ${ac['value_at_price']:,.2f}   (v2 B50: $518,450.00 - documented)")
    over_ac = metric_at_price(DEALS["BRRR"], ac["price"] + 1, "cash_left")
    print(f"$1 above: cash left ${over_ac:,.2f}  (must be > 0)")
    print(f"Rental: {max_price_all_cash_out(DEALS['Rental'])['status']}")
    print(f"Flip:   {max_price_all_cash_out(DEALS['Flip'])['status']}")
    