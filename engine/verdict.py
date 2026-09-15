"""
Decision layer for Dash ROI v3: DSCR, required rent, and verdict.
Ports v2's Return Analysis DSCR block + Main_Dashboard verdict logic.

v3 DSCR gate is UPGRADED from v2: v2 hard-rejects only below 1.0; v3 treats
the lender minimum (default 1.20) as a financeability gate, with <1.0 a more
severe tier. Threshold is configurable (lenders vary 1.20-1.25).
"""

from engine.projection import project
from engine.amortization import annual_debt_service

# Lender DSCR minimum. Mainstream floor is 1.20; some lenders want 1.25.
DSCR_LENDER_MIN = 1.20


def dscr_by_year(noi_by_year, annual_debt):
    """DSCR for each year = NOI / annual debt service (v2 Return Analysis B66+)."""
    return [noi / annual_debt for noi in noi_by_year]


def min_dscr(noi_by_year, annual_debt):
    """Minimum DSCR over the hold (v2 B81 = MIN over the years)."""
    return min(dscr_by_year(noi_by_year, annual_debt))


def required_rent(annual_debt, tax_rate, price, annual_insurance, hoa,
                  vacancy_rate, maint_rate, mgmt_rate, capex_rate,
                  dscr_target=DSCR_LENDER_MIN):
    """
    Back-solve the gross monthly rent needed to hit the DSCR target.
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


def verdict(irr_value, min_dscr_value, target_irr, dscr_min=DSCR_LENDER_MIN):
    """
    Investment verdict. v3 tiered DSCR gate (upgraded from v2's single 1.0 line):
      DSCR < 1.0            -> HARD REJECT (asset can't cover its debt)
      1.0 <= DSCR < dscr_min -> REJECT (works, but not financeable)
      DSCR >= dscr_min:
        IRR < target*0.5   -> REJECT (returns far too low)
        IRR >= target       -> STRONG BUY (both gates strong) / BUY
        otherwise           -> NEGOTIATE
    """
    if min_dscr_value < 1.0:
        return "HARD REJECT"
    if min_dscr_value < dscr_min:
        return "REJECT"                      # not financeable
    # DSCR is financeable from here on:
    if irr_value < target_irr * 0.5:
        return "REJECT"                      # returns far too low
    if irr_value >= target_irr:
        return "STRONG BUY"                  # IRR target met AND DSCR >= min
    return "NEGOTIATE"


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
    v = verdict(-0.0514, 1.05, 0.15)
    print(f"Verdict:      {v}   (v2: REJECT)")