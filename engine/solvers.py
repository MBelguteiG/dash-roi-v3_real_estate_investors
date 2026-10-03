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


def irr_at_price(inputs, price):
    """Re-run the whole deal at a different purchase price; return its IRR."""
    return analyze_deal(**{**inputs, "price": price})["irr"]


def max_price_irr(inputs, target_irr=None, tol=0.01, max_iter=200):
    """
    inputs: the same dict you would pass to analyze_deal() (must include model).
    Returns {"status", "price", "irr_at_price", "reason"}.
    status: SOLVED / REFUSED / NO SOLUTION
    """
    model = inputs["model"]
    if model == "Flip":
        return {"status": "REFUSED", "price": None, "irr_at_price": None,
                "reason": "Flip has no IRR - use Max Offer (MAO)"}

    target = inputs["target_irr"] if target_irr is None else target_irr
    base = inputs["price"]
    no_solution = {"status": "NO SOLUTION", "price": None, "irr_at_price": None,
                   "reason": "no price in search range hits the target"}

    # --- bracket: lo meets the target, hi misses it ---
    lo = hi = base
    if irr_at_price(inputs, base) >= target:
        while irr_at_price(inputs, hi) >= target:      # search upward
            lo = hi
            hi *= 1.5
            if hi > base * 100:
                return no_solution
    else:
        while irr_at_price(inputs, lo) < target:       # search downward
            hi = lo
            lo *= 0.5
            if lo < 1000:
                return no_solution

    # --- bisection: halve the gap until it is under one cent ---
    for _ in range(max_iter):
        if hi - lo <= tol:
            break
        mid = (lo + hi) / 2
        if irr_at_price(inputs, mid) >= target:
            lo = mid
        else:
            hi = mid

    return {"status": "SOLVED", "price": lo,
            "irr_at_price": irr_at_price(inputs, lo), "reason": ""}


# --- Self-consistency tests ---
if __name__ == "__main__":
    from engine.crosscheck import DEALS

    rental = DEALS["Rental"]   # IL deal: IRR -5.39% at $250,000

    print("=== Max Price IRR - self-consistency ===\n")

    # Test 1: target ABOVE current IRR -> answer must be BELOW $250,000
    r = max_price_irr(rental, target_irr=0.15)
    print(f"Target 15%:  {r['status']}  price ${r['price']:,.2f}  "
          f"IRR there {r['irr_at_price']*100:.4f}%")

    # Test 2: target BELOW current IRR -> answer must be ABOVE $250,000
    r2 = max_price_irr(rental, target_irr=-0.10)
    print(f"Target -10%: {r2['status']}  price ${r2['price']:,.2f}  "
          f"IRR there {r2['irr_at_price']*100:.4f}%")

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
          f"IRR there {b['irr_at_price']*100:.4f}%")

    # Test 6: BRRR - target BELOW current IRR -> price ABOVE $650,000
    b2 = max_price_irr(brrr, target_irr=0.05)
    print(f"BRRR target 5%:  {b2['status']}  price ${b2['price']:,.2f}  "
          f"IRR there {b2['irr_at_price']*100:.4f}%")