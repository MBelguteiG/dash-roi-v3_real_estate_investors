"""
Deal orchestrator for Dash ROI v3.
Single entry point that runs the full Rental analysis: takes deal inputs,
pulls scenario assumptions from the lookup, runs every engine, and returns
all outputs in one dict. This is what the UI (Phase 5) will call.
"""

from engine.assumptions import get_assumptions
from engine.projection import project
from engine.amortization import annual_debt_service
from engine.deal import build_stream, cash_on_cash
from engine.irr import irr
from engine.verdict import dscr_by_year, min_dscr, required_rent, rental_verdict


def analyze_deal(state, property_type, model, scenario,
                 price, down_pct, annual_rate, rehab, base_rent,
                 exit_year, target_irr):
    """
    Run the full Rental analysis for one deal.
    Deal-specific inputs are passed in; scenario assumptions come from the
    Assumption_DB lookup. Returns a dict of all outputs.
    """
    # --- scenario assumptions from the lookup (the dynamic source) ---
    a = get_assumptions(state, property_type, model, scenario)
    vacancy_rate = a["VacancyRate% Annual"]
    maint_rate = a["Maintenance% Annual"]
    mgmt_rate = a["Management Fee"]
    capex_rate = a["CapEx% Annual"]
    tax_rate = a["PropertyTaxRate Annual"]
    closing_pct = a["Closing Cost Buying"]
    selling_pct = a["SellingCost% Annual"]
    annual_insurance = a["Insurance Yearly"]
    hoa = a["HOA Monthly"]
    rent_growth = a["RentGrowth Annual"]
    tax_growth = a["Tax Growth"]
    inflation = a["Inflation Annual"]
    appreciation = a["Appreciation Annual"]

    loan = price - price * down_pct
    debt = annual_debt_service(loan, annual_rate)
    annual_capex = base_rent * 12 * capex_rate   # capex as % of gross rent

    # base Year-1 monthly expense dollars for the stream
    base_maint = base_rent * maint_rate

    # --- cash-flow stream + return metrics ---
    stream = build_stream(
        price=price, down_pct=down_pct, rehab=rehab, closing_pct=closing_pct,
        annual_rate=annual_rate, exit_year=exit_year,
        base_rent=base_rent, vacancy_rate=vacancy_rate, tax_rate=tax_rate,
        base_annual_insurance=annual_insurance, base_hoa=hoa,
        base_maint=base_maint, mgmt_rate=mgmt_rate, annual_capex=annual_capex,
        rent_growth=rent_growth, tax_growth=tax_growth,
        inflation=inflation, appreciation=appreciation,selling_pct=selling_pct,
    )
    irr_value = irr(stream)
    coc = cash_on_cash(stream)

    # --- DSCR + verdict ---
    years = project(exit_year, base_rent, vacancy_rate, price, tax_rate,
                    annual_insurance, hoa, base_maint, mgmt_rate,
                    rent_growth, tax_growth, inflation)
    noi_by_year = [y["noi_annual"] for y in years]
    dscrs = dscr_by_year(noi_by_year, debt)
    min_d = min_dscr(noi_by_year, debt)

    req_rent = required_rent(debt, tax_rate, price, annual_insurance, hoa,
                             vacancy_rate, maint_rate, mgmt_rate, capex_rate)


    cushion = base_rent - req_rent
    v = rental_verdict(irr_value, min_d, target_irr, rent_cushion=cushion)
    

    return {
        "irr": irr_value,
        "cash_on_cash": coc,
        "dscr_by_year": dscrs,
        "min_dscr": min_d,
        "required_rent": req_rent,
        "rent_cushion":  cushion,
        "verdict": v,
    }


# --- Full Rental parity check against the v2 reference deal ---
if __name__ == "__main__":
    result = analyze_deal(
        state="Illinois", property_type="Townhouse",
        model="Rental", scenario="Conservative",
        price=250000, down_pct=0.30, annual_rate=0.078, rehab=28000,
        base_rent=2750, exit_year=5, target_irr=0.15,
    )

    print("=== FULL RENTAL PARITY CHECK (Illinois/Townhouse/Rental/Conservative) ===\n")
    print(f"IRR:            {result['irr']*100:>8.2f}%    (v2: -5.14%)")
    print(f"Cash-on-cash:   {result['cash_on_cash']*100:>8.2f}%    (v2: -0.04%)")
    print(f"Min DSCR:       {result['min_dscr']:>8.2f}     (v2: 1.05)")
    print(f"Required rent:  ${result['required_rent']:>10,.2f} (v2: $3,296.52)")
    print(f"Rent cushion:   ${result['rent_cushion']:>10,.2f} (v2: -$546.52)")
    print(f"Verdict:        {result['verdict']:>10}   (v2: REJECT)")