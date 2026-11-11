from engine.brrr import brrr_verdict
from engine.flip import flip_verdict

"""
Decision layer for Dash ROI v3: DSCR, required rent, and verdict.
Ports v2's Return Analysis DSCR block + Main_Dashboard verdict logic.

v3 DSCR gate is UPGRADED from v2: v2 hard-rejects only below 1.0; v3 treats
the lender minimum (default 1.20) as a financeability gate, with <1.0 a more
severe tier. Threshold is configurable (lenders vary 1.20-1.25).
"""

from engine.projection import project
from engine.amortization import annual_debt_service

# Lender DSCR minimum (DSCR-loan convention: gross rent / PITIA).
# 1.00 is the typical DSCR-loan floor; the user can raise it (1.20, 1.25...).
DSCR_LENDER_MIN = 1.00
DSCR_STRONG = 1.25


def pitia(annual_debt, monthly_tax, monthly_insurance, monthly_hoa):
    """Monthly PITIA = principal & interest + property tax + insurance + HOA."""
    return annual_debt / 12 + monthly_tax + monthly_insurance + monthly_hoa


def lender_dscr(monthly_rent, monthly_pitia):
    """DSCR the way DSCR lenders size it: gross monthly rent / PITIA."""
    return monthly_rent / monthly_pitia


def lender_dscr_by_year(years, annual_debt):
    """Rent / PITIA for each projected year (rent, tax, insurance, HOA grow)."""
    return [lender_dscr(y["rent"], pitia(annual_debt, y["property_tax"],
                                         y["insurance"], y["hoa"]))
            for y in years]


def required_rent_lender(monthly_pitia, dscr_target=DSCR_LENDER_MIN):
    """Gross monthly rent a DSCR lender needs to see: target x PITIA."""
    return dscr_target * monthly_pitia


def dscr_by_year(noi_by_year, annual_debt):
    """DSCR for each year = NOI / annual debt service (v2 Return Analysis B66+)."""
    return [noi / annual_debt for noi in noi_by_year]


def min_dscr(noi_by_year, annual_debt):
    """Minimum DSCR over the hold (v2 B81 = MIN over the years)."""
    return min(dscr_by_year(noi_by_year, annual_debt))


def required_rent(annual_debt, tax_rate, price, annual_insurance, hoa,
                  vacancy_rate, maint_rate, mgmt_rate, capex_rate,
                  dscr_target=1.20):
    """
    Investor-side: back-solve the gross monthly rent whose NOI, after a
    CapEx reserve, covers the loan payment 1.20x (drives the rent cushion and
    "rent to also cover big repairs"). Not the lender DSCR - see
    required_rent_lender() for rent / PITIA.
    Ports v2 Main_Dashboard B35:
      (required_monthly_NOI + fixed monthly expenses) / (1 - rent-based rates)
    Required monthly NOI = dscr_target * annual_debt / 12.
    Fixed monthly expenses = property tax + insurance + HOA (per month).
    Rent-based rates = vacancy + maintenance + management + capex.
    """
    required_monthly_noi = dscr_target * annual_debt / 12
    monthly_tax = price * tax_rate / 12
    monthly_insurance = annual_insurance / 12
    fixed_monthly = monthly_tax + monthly_insurance + hoa
    rent_based_rate = vacancy_rate + maint_rate + mgmt_rate + capex_rate
    return (required_monthly_noi + fixed_monthly) / (1 - rent_based_rate)


def rental_verdict(irr_value, min_dscr_value, target_irr, rent_cushion,
                   dscr_min=DSCR_LENDER_MIN):
    """
    Rental verdict. DSCR (rent / PITIA) is the sole hard gate, at the
    user's minimum (default 1.00):
      DSCR < dscr_min -> HARD REJECT (a DSCR lender won't fund it)
      DSCR >= dscr_min:
        IRR < target*0.5                  -> REJECT
        IRR >= target and rent_cushion > 0 -> STRONG BUY
        IRR >= target                      -> BUY
        otherwise                          -> NEGOTIATE
    """
    if min_dscr_value < dscr_min:
        return "HARD REJECT"
    if irr_value < target_irr * 0.5:
        return "REJECT"
    if irr_value >= target_irr and rent_cushion > 0:
        return "STRONG BUY"
    if irr_value >= target_irr:
        return "BUY"
    return "NEGOTIATE"

def verdict(model, **kwargs):
    """
    Single entry point for all three models (mirrors v2 Main_Dashboard C42).
    Routes only - each model's logic stays in its own engine.
      Rental: irr_value, min_dscr_value, target_irr, rent_cushion
      BRRR:   raw_irr, cash_left, dscr, target_irr, rent_cushion
      Flip:   net_profit, margin, target_margin
    """
    if model == "Rental":
        return rental_verdict(**kwargs)
    if model == "BRRR":
        return brrr_verdict(**kwargs)
    if model == "Flip":
        return flip_verdict(**kwargs)
    raise ValueError(f"Unknown model: {model}")

# --- Validation against the v2 reference deal ---
if __name__ == "__main__":
    # NOI per year from v2 Return Analysis (rows 66-70, first 5 years):
    noi = [15860.00, 16149.90, 16443.29, 16740.18, 17040.56]
    debt = annual_debt_service(175000, 0.078)   # 15,117.28

    dscrs = dscr_by_year(noi, debt)
    print("DSCR by year:", [f"{d:.2f}" for d in dscrs], "(v2: 1.05,1.07,1.09,1.11,1.13)")
    print(f"Min DSCR:     {min_dscr(noi, debt):.2f}   (v2: 1.05)")

    rr = required_rent(
        annual_debt=debt, tax_rate=0.021, price=250000,
        annual_insurance=1900, hoa=200,
        vacancy_rate=0.06, maint_rate=0.09, mgmt_rate=0.08, capex_rate=0.07,
    )
    print(f"Required rent: ${rr:,.2f}   (v2: $3,296.52)")

    # Reference deal: IRR -5.14%, min DSCR 1.05, target 15%
    v = rental_verdict(-0.0514, 1.05, 0.15, rent_cushion=0)
    print(f"Verdict:      {v}   (v2: REJECT)")

    # --- Week 13: one call, all three models, against v2 C42 ---
    print("\n=== verdict() dispatcher: all 3 models ===")
    r = verdict("Rental", irr_value=-0.0539, min_dscr_value=1.05,
                target_irr=0.15, rent_cushion=-546.52)
    b = verdict("BRRR", raw_irr=0.0740, cash_left=92875.00, dscr=0.528,
                target_irr=0.13, rent_cushion=-2920.79)
    f = verdict("Flip", net_profit=9710.42, margin=0.0121, target_margin=0.13)
    print(f"Rental: {r}   (v2: REJECT)")
    print(f"BRRR:   {b}   (v2: HARD REJECT)")
    print(f"Flip:   {f}   (v2: REJECT)")
    try:
        verdict("Condo")
    except ValueError as e:
        print(f"Bad model caught: {e}")

def approval_likelihood(model, min_dscr=None, ltv=None, hm_ltv_on_arv=None,
                        dscr_min=DSCR_LENDER_MIN):
    """
    Lender fundability. DSCR here is rent / PITIA.
    Flip: hard-money loan / ARV must be at or under 75%.
    Rental/BRRR: STRONG at DSCR >= 1.25 (or the user's minimum, if higher)
    and LTV <= 80%; CONDITIONAL at the user's minimum; else LIKELY DECLINE.
    """
    if model == "Flip":
        return "LIKELY" if hm_ltv_on_arv <= 0.75 else "UNLIKELY"
    if min_dscr >= max(DSCR_STRONG, dscr_min) and ltv <= 0.80:
        return "STRONG"
    if min_dscr >= dscr_min:
        return "CONDITIONAL"
    return "LIKELY DECLINE"   