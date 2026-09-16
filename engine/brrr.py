"""
BRRR engine for Dash ROI v3 - refi sizing and cash-out netting.
SEPARATE from Rental (per engine principles: never retrofit Rental for BRRR).

BRRR loan is sized off ARV x refi LTV, not purchase price. The cash-out at
refinance (refi loan - hard-money payoff) can drive net cash invested
negative - the "all cash out" scenario that needs a guard later.

v3 upgrade (documented): cash invested INCLUDES hard-money carrying costs
(interest, points, holding), which v2 omits. More conservative/auditable.
"""


def hard_money_loan(purchase_price, hm_ltv):
    """HM loan sized off PURCHASE price (v2: B3*B14). Not purchase+rehab."""
    return purchase_price * hm_ltv


def refi_loan(arv, refi_ltv):
    """New long-term loan sized off ARV (v2: B11*B15)."""
    return arv * refi_ltv


def hard_money_interest(hm_loan, hm_rate, refi_month):
    """
    Interest-only carrying cost on the HM loan until refi.
    v2 treats this as simple interest-only: loan * rate/12 * months.
    """
    return hm_loan * (hm_rate / 12) * refi_month


def cash_pulled_out(arv, refi_ltv, purchase_price, hm_ltv):
    """Gross cash from refi = refi loan - hard-money principal (v2: B23)."""
    return refi_loan(arv, refi_ltv) - hard_money_loan(purchase_price, hm_ltv)


def cash_invested(purchase_price, rehab, closing_cost, hm_ltv,
                  hm_loan, hm_interest, hm_points, holding_cost,
                  include_carrying=True):
    """
    Out-of-pocket cash. v2 (B27): purchase + rehab + closing - hm_loan.
    v3 upgrade: also add HM interest + points + holding costs (real cash out).
    Set include_carrying=False to reproduce v2 exactly.
    """
    base = purchase_price + rehab + closing_cost - hm_loan
    if include_carrying:
        return base + hm_interest + hm_points + holding_cost
    return base


def cash_left_in_deal(cash_invested_amt, cash_pulled_out_amt):
    """Net cash still in the deal after refi (v2: B24). Negative = all cash out."""
    return cash_invested_amt - cash_pulled_out_amt


# --- Validation against the v2 BRRR reference deal ---
if __name__ == "__main__":
    # Inputs (v2 Property_inputs, BRRR mode):
    PURCHASE = 250000
    REHAB = 28000
    ARV = 450000
    HM_LTV = 0.90
    HM_RATE = 0.105
    REFI_LTV = 0.75
    REFI_MONTH = 6
    CLOSING = 9375          # 3.75% x purchase (B26)
    HM_POINTS = 4500        # 2% x hard money (B50)
    HOLDING = 6575          # total holding cost (B53)

    hm = hard_money_loan(PURCHASE, HM_LTV)
    rl = refi_loan(ARV, REFI_LTV)
    hm_int = hard_money_interest(hm, HM_RATE, REFI_MONTH)
    pulled = cash_pulled_out(ARV, REFI_LTV, PURCHASE, HM_LTV)

    print("=== BRRR CASH-OUT NETTING ===\n")
    print(f"Hard money loan:   ${hm:>12,.2f}   (v2: $225,000.00)")
    print(f"Refi new loan:     ${rl:>12,.2f}   (v2: $337,500.00)")
    print(f"HM interest (6mo): ${hm_int:>12,.2f}   (v2: $11,812.50)")
    print(f"Cash pulled out:   ${pulled:>12,.2f}   (v2: $112,500.00)")

    # v2-style cash invested (exclude carrying) - should match $62,375
    ci_v2 = cash_invested(PURCHASE, REHAB, CLOSING, HM_LTV, hm,
                          hm_int, HM_POINTS, HOLDING, include_carrying=False)
    print(f"\nCash invested (v2 method):  ${ci_v2:>12,.2f}   (v2: $62,375.00)")

    # v3 upgraded cash invested (include carrying)
    ci_v3 = cash_invested(PURCHASE, REHAB, CLOSING, HM_LTV, hm,
                          hm_int, HM_POINTS, HOLDING, include_carrying=True)
    print(f"Cash invested (v3 upgrade): ${ci_v3:>12,.2f}   (adds $22,887.50 carrying)")

    print(f"\nCash left in deal (v2):  ${cash_left_in_deal(ci_v2, pulled):>12,.2f}   (v2: -$50,125.00)")
    print(f"Cash left in deal (v3):  ${cash_left_in_deal(ci_v3, pulled):>12,.2f}   (upgraded)")