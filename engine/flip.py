"""
Flip engine for Dash ROI v3 - profit margin, ROI, annualized ROI, verdict.
SEPARATE from Rental and BRRR (per engine principles: never retrofit one
model's logic onto another). Flip is a single-exit model: no monthly cash
flow series, no DSCR relevance - just total project cost vs. sale price
at one point in time.

Reuses hard_money_loan() and hard_money_interest() from brrr.py unchanged -
both loan types are sized identically off purchase price (rows labeled
"BRRR+Flip" in Property_inputs), Flip just runs interest-only for the full
hold instead of stopping at a refi month.
"""

from engine.brrr import hard_money_loan, hard_money_interest


def hm_points(hm_loan, points_pct):
    """v2 Property_inputs B50: HM Loan x Points %."""
    return hm_loan * points_pct


def buying_closing_costs(purchase_price, closing_cost_pct):
    """
    v2 Property_inputs B51: purchase price x closing cost %.
    closing_cost_pct comes from Assumption_DB, keyed on
    (State, PropertyType, ModelType="Flip", Scenario) via
    assumptions.get_assumptions(...)["Closing Cost Buying"].
    """
    return purchase_price * closing_cost_pct


def monthly_holding_cost(purchase_price, tax_rate, annual_insurance,
                          monthly_utilities, monthly_hoa, monthly_maint_security):
    """
    v2 Property_inputs B52. tax_rate/annual_insurance/monthly_hoa all come
    from the same Assumption_DB lookup as closing/selling cost - Dashboard
    Inputs just caches each field from its own INDEX/MATCH call.
    """
    return ((purchase_price * tax_rate / 12) + (annual_insurance / 12)
             + monthly_utilities + monthly_hoa + monthly_maint_security)


def total_holding_cost(monthly_holding, hold_months):
    """v2 Property_inputs B53."""
    return monthly_holding * hold_months


def selling_cost(sale_price, selling_pct):
    """v2 Property_inputs B54: sale price x selling cost %."""
    return sale_price * selling_pct


def total_project_cost(purchase_price, rehab_cost, hm_interest, hm_points_amt,
                        buying_closing_costs_amt, total_holding, selling_cost_amt):
    """v2 Property_inputs B55."""
    return (purchase_price + rehab_cost + hm_interest + hm_points_amt
             + buying_closing_costs_amt + total_holding + selling_cost_amt)


def net_flip_profit(sale_price, total_cost):
    """v2 Property_inputs B56: Sale Price - Total Project Cost."""
    return sale_price - total_cost


def cash_invested(total_cost, hm_loan):
    """v2 Property_inputs B57: Total Project Cost - HM Loan."""
    return total_cost - hm_loan


def roi_on_cash(net_profit, cash_invested_amt):
    """v2 Property_inputs B58."""
    return net_profit / cash_invested_amt


def annualized_roi(roi_cash, hold_months):
    """v2 Property_inputs B59, zero-guarded."""
    return "-" if hold_months == 0 else roi_cash * (12 / hold_months)


def profit_margin(net_profit, sale_price):
    """v2 Property_inputs B60: Net Profit / Sale Price (ARV)."""
    return net_profit / sale_price


def flip_verdict(net_profit, margin, target_margin):
    """
    v2 Property_inputs B62 (IFS). Dynamic-threshold gate on Target Margin
    (Main_Dashboard B13), NOT fixed 25%/15%/10% tiers - correcting the
    prior engine-principles.md record. Only fixed thresholds are the 10%
    REJECT floor and net-loss HARD REJECT; STRONG BUY/BUY scale with
    whatever target margin the user set (1.5x / 1.0x).
    """
    if net_profit <= 0:
        return "HARD REJECT"
    if margin < 0.10:
        return "REJECT"
    if margin >= target_margin * 1.5:
        return "STRONG BUY"
    if margin >= target_margin:
        return "BUY"
    return "NEGOTIATE"


# --- Validation against the v2 Flip reference deal ---
if __name__ == "__main__":
    from engine.assumptions import get_assumptions

    PURCHASE = 650000
    REHAB = 25000
    ARV = 800000            # also Flip Sale Price
    HM_LTV = 0.85
    HM_RATE = 0.12
    HOLD_MONTHS = 5
    POINTS_PCT = 0.02
    TARGET_MARGIN = 0.13
    MONTHLY_UTILITIES = 150.00
    MONTHLY_MAINT_SECURITY = 150.00

    a = get_assumptions("California", "Townhouse", "Flip", "Base")
    tax_rate = a["PropertyTaxRate Annual"]
    annual_insurance = a["Insurance Yearly"]
    monthly_hoa = a["HOA Monthly"]
    closing_pct = a["Closing Cost Buying"]
    selling_pct = a["SellingCost% Annual"]

    hm = hard_money_loan(PURCHASE, HM_LTV)
    hm_int = hard_money_interest(hm, HM_RATE, HOLD_MONTHS)
    points = hm_points(hm, POINTS_PCT)
    closing = buying_closing_costs(PURCHASE, closing_pct)
    mhc = monthly_holding_cost(PURCHASE, tax_rate, annual_insurance,
                                MONTHLY_UTILITIES, monthly_hoa, MONTHLY_MAINT_SECURITY)
    thc = total_holding_cost(mhc, HOLD_MONTHS)
    sell = selling_cost(ARV, selling_pct)
    tpc = total_project_cost(PURCHASE, REHAB, hm_int, points, closing, thc, sell)
    profit = net_flip_profit(ARV, tpc)
    ci = cash_invested(tpc, hm)
    roi = roi_on_cash(profit, ci)
    aroi = annualized_roi(roi, HOLD_MONTHS)
    margin = profit_margin(profit, ARV)
    verdict = flip_verdict(profit, margin, TARGET_MARGIN)

    print("=== FLIP ENGINE VALIDATION ===\n")
    print(f"HM loan:         ${hm:>12,.2f}   (v2: $552,500.00)")
    print(f"HM interest:     ${hm_int:>12,.2f}   (v2: $27,625.00)")
    print(f"HM points:       ${points:>12,.2f}   (v2: $11,050.00)")
    print(f"Closing costs:   ${closing:>12,.2f}   (v2: $17,875.00)")
    print(f"Monthly holding: ${mhc:>12,.2f}   (v2: $1,347.92)")
    print(f"Total holding:   ${thc:>12,.2f}   (v2: $6,739.58)")
    print(f"Selling cost:    ${sell:>12,.2f}   (v2: $52,000.00)")
    print(f"Total cost:      ${tpc:>12,.2f}   (v2: $790,289.58)")
    print(f"\nNet profit:      ${profit:>12,.2f}   (v2: $9,710.42)")
    print(f"Cash invested:   ${ci:>12,.2f}   (v2: $237,789.58)")
    print(f"ROI on cash:     {roi:.2%}          (v2: 4.08%)")
    print(f"Annualized ROI:  {aroi:.2%}          (v2: 9.80%)")
    print(f"Profit margin:   {margin:.2%}          (v2: 1.21%)")
    print(f"Verdict:         {verdict}   (v2: REJECT)")