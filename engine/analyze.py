
"""
Deal orchestrator for Dash ROI v3.
Single entry point (analyze_deal) routes Rental / BRRR / Flip to each model's
own orchestrator, which pulls scenario assumptions from the lookup, runs that
model's engine, and returns all outputs in one dict. This is what the UI
(Phase 5) will call.
"""

from engine.guards import validate_inputs
from engine.assumptions import get_assumptions
from engine.projection import project
from engine.amortization import annual_debt_service
from engine.deal import build_stream, cash_on_cash
from engine.irr import irr
from engine.verdict import dscr_by_year, min_dscr, required_rent, rental_verdict, verdict

from engine.brrr import (hard_money_loan, hard_money_interest, refi_loan, cash_pulled_out,
                         cash_invested as brrr_cash_invested, cash_left_in_deal,
                         post_refi_dscr, post_refi_dscr_with_reserves,
                         build_brrr_schedule, build_brrr_monthly_stream, brrr_irr,
                         years_held_post_refi, sale_price_at_exit,
                         brrr_selling_cost, brrr_net_sale_proceeds,
                        brrr_selling_cost, brrr_net_sale_proceeds, is_all_cash_out, rate_term_ltv)

from engine.flip import (hm_points, buying_closing_costs, monthly_holding_cost,
                         total_holding_cost, selling_cost, total_project_cost,
                         net_flip_profit, cash_invested as flip_cash_invested,
                         roi_on_cash, annualized_roi, profit_margin,
                         max_offer_mao, max_offer_seventy_pct, over_under_max_offer)



def analyze_rental(state, property_type, scenario,
                 price, down_pct, annual_rate, rehab, base_rent,
                 exit_year, target_irr, overrides=None):           

    """
    Run the full Rental analysis for one deal.
    Deal-specific inputs are passed in; scenario assumptions come from the
    Assumption_DB lookup. Returns a dict of all outputs.
    """


    # --- scenario assumptions from the lookup (the dynamic source) ---
    a = get_assumptions(state, property_type, "Rental", scenario)
    if overrides:
        unknown = set(overrides) - set(a)
        if unknown:
            raise ValueError(f"Unknown assumption(s): {sorted(unknown)}")
        a = {**a, **overrides}
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
    

    # base Year-1 monthly expense dollars for the stream
    base_maint = base_rent * maint_rate

    # --- cash-flow stream + return metrics ---
    stream = build_stream(
        price=price, down_pct=down_pct, rehab=rehab, closing_pct=closing_pct,
        annual_rate=annual_rate, exit_year=exit_year,
        base_rent=base_rent, vacancy_rate=vacancy_rate, tax_rate=tax_rate,
        base_annual_insurance=annual_insurance, base_hoa=hoa,
        base_maint=base_maint, mgmt_rate=mgmt_rate, capex_rate = capex_rate,
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
        "loan_amount": loan,
        "ltv": loan / price,
        "noi_y1": noi_by_year[0],
        "annual_debt_service": debt,
    }




def analyze_brrr(state, property_type, scenario,
                 price, rehab, base_rent, exit_year, target_irr,
                 arv, hm_ltv, hm_rate, refi_ltv, refi_month, post_refi_rate, refi_type="Cash-Out"):
    """
    Run the full BRRR analysis for one deal. Uses only the BRRR engine
    (brrr.py) - never retrofits Rental. Monthly stream + annualized IRR
    mirrors v2 Property_inputs B38.
    """
    a = get_assumptions(state, property_type, "BRRR", scenario)
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
    base_maint = base_rent * maint_rate

    if refi_type not in ("Cash-Out", "Rate/Term"):
        raise ValueError(f"Unknown refi type: {refi_type}")
    if refi_type == "Rate/Term":
        refi_ltv = rate_term_ltv(arv, refi_ltv, price, hm_ltv)

    # --- loans + cash (v2 method: the stream already carries HM interest) ---
    hm = hard_money_loan(price, hm_ltv)
    rl = refi_loan(arv, refi_ltv)
    closing = price * closing_pct
    ci = brrr_cash_invested(price, rehab, closing, hm_ltv, hm, 0, 0, 0,
                            include_carrying=False)
    pulled = cash_pulled_out(arv, refi_ltv, price, hm_ltv)
    left = cash_left_in_deal(ci, pulled)

    # --- monthly stream + IRR ---
    monthly = build_brrr_monthly_stream(
        purchase_price=price, rehab=rehab, hm_ltv=hm_ltv, hm_rate=hm_rate,
        refi_ltv=refi_ltv, refi_month=refi_month, post_refi_rate=post_refi_rate,
        arv=arv, appreciation_rate=appreciation, exit_year=exit_year,
        selling_pct=selling_pct, cash_invested_amt=ci, base_rent=base_rent,
        vacancy_rate=vacancy_rate, tax_rate=tax_rate,
        annual_insurance=annual_insurance, hoa=hoa, base_maint=base_maint,
        mgmt_rate=mgmt_rate, capex_rate=capex_rate, rent_growth=rent_growth,
        tax_growth=tax_growth, inflation=inflation,
    )
    irr_value = brrr_irr(monthly)
    post_refi_cf = sum(monthly[refi_month + 1: refi_month + 13])
    coc = post_refi_cf / left if left > 0 else None   # all cash out: no denominator

    # --- lender view: post-refi DSCR on Year-1 NOI (v2 B39 / B40) ---
    years = project(exit_year, base_rent, vacancy_rate, price, tax_rate,
                    annual_insurance, hoa, base_maint, mgmt_rate,
                    rent_growth, tax_growth, inflation)
    noi_y1 = years[0]["noi_annual"]
    capex_y1 = base_rent * 12 * capex_rate
    dscr = post_refi_dscr(noi_y1, rl, post_refi_rate)
    dscr_res = post_refi_dscr_with_reserves(noi_y1, capex_y1, rl, post_refi_rate)

    # --- required rent on POST-REFI debt (v2 B35 wrongly uses purchase mortgage) ---
    refi_debt = annual_debt_service(rl, post_refi_rate)
    req_rent = required_rent(refi_debt, tax_rate, price, annual_insurance, hoa,
                             vacancy_rate, maint_rate, mgmt_rate, capex_rate)
    cushion = base_rent - req_rent

    # --- exit ---
    sale = sale_price_at_exit(arv, appreciation,
                              years_held_post_refi(exit_year, refi_month))
    sched = build_brrr_schedule(hm, hm_rate, refi_month, rl, post_refi_rate,
                                exit_year * 12)
    balance = sched[-1]["balance"]
    net_sale = brrr_net_sale_proceeds(sale, brrr_selling_cost(sale, selling_pct),
                                      balance)

    v = verdict("BRRR", raw_irr=irr_value, cash_left=left, dscr=dscr,
                target_irr=target_irr, rent_cushion=cushion)

    return {
        "irr": irr_value,
        "cash_invested": ci,
        "cash_pulled_out": pulled,
        "cash_left": left,
        "post_refi_cash_flow": post_refi_cf,
        "cash_on_cash": coc,
        "dscr": dscr,
        "dscr_with_reserves": dscr_res,
        "refi_type": refi_type,
        "refi_loan": rl,
        "refi_ltv_effective": refi_ltv,
        "required_rent": req_rent,
        "rent_cushion": cushion,
        "sale_price": sale,
        "remaining_balance": balance,
        "net_sale_proceeds": net_sale,
        "equity_at_exit": sale - balance,
        "all_cash_out": is_all_cash_out(irr_value, left),
        "verdict": v,
    }

def analyze_flip(state, property_type, scenario,
                 price, rehab, arv, hm_ltv, hm_rate, hold_months, points_pct,
                 monthly_utilities, monthly_maint_security, target_margin):
    """
    Run the full Flip analysis for one deal. Uses only the Flip engine
    (flip.py) - single-exit model: no cash-flow stream, no DSCR, no IRR.
    """
    a = get_assumptions(state, property_type, "Flip", scenario)
    tax_rate = a["PropertyTaxRate Annual"]
    annual_insurance = a["Insurance Yearly"]
    monthly_hoa = a["HOA Monthly"]
    closing_pct = a["Closing Cost Buying"]
    selling_pct = a["SellingCost% Annual"]

    # --- project costs ---
    hm = hard_money_loan(price, hm_ltv)
    hm_int = hard_money_interest(hm, hm_rate, hold_months)
    points = hm_points(hm, points_pct)
    closing = buying_closing_costs(price, closing_pct)
    mhc = monthly_holding_cost(price, tax_rate, annual_insurance,
                               monthly_utilities, monthly_hoa, monthly_maint_security)
    thc = total_holding_cost(mhc, hold_months)
    sell = selling_cost(arv, selling_pct)
    tpc = total_project_cost(price, rehab, hm_int, points, closing, thc, sell)

    # --- returns ---
    profit = net_flip_profit(arv, tpc)
    ci = flip_cash_invested(tpc, hm)
    roi = roi_on_cash(profit, ci)
    aroi = annualized_roi(roi, hold_months)
    margin = profit_margin(profit, arv)

    # --- max offer ---
    mao = max_offer_mao(arv, target_margin, sell, rehab, thc, hm_int, points, closing)
    mao_70 = max_offer_seventy_pct(arv, rehab)

    v = verdict("Flip", net_profit=profit, margin=margin, target_margin=target_margin)

    return {
        "hm_loan": hm,
        "hm_interest": hm_int,
        "hm_points": points,
        "closing_costs": closing,
        "monthly_holding": mhc,
        "total_holding": thc,
        "selling_cost": sell,
        "total_project_cost": tpc,
        "net_profit": profit,
        "cash_invested": ci,
        "roi_on_cash": roi,
        "annualized_roi": aroi,
        "profit_margin": margin,
        "max_offer_mao": mao,
        "max_offer_70pct": mao_70,
        "over_under_mao": over_under_max_offer(price, mao),
        "verdict": v,
    }


def analyze_deal(model, **inputs):
    """
    Single entry point for the UI. Routes to each model's own orchestrator -
    inputs differ by model, so each analyze_* function declares its own.
    """

    if model not in ("Rental", "BRRR", "Flip"):
        raise ValueError(f"Unknown model: {model}")
    overrides = inputs.pop("overrides", None)
    if overrides and model != "Rental":
        raise ValueError("Assumption overrides are Rental-only for now")
    validate_inputs(model, inputs)


    if model == "Rental":
        return analyze_rental(**inputs, overrides=overrides)
    if model == "BRRR":
        return analyze_brrr(**inputs)
    if model == "Flip":
        return analyze_flip(**inputs)
    raise ValueError(f"Unknown model: {model}")

# --- Full Rental parity check against the v2 reference deal ---
if __name__ == "__main__":
    result = analyze_deal(
        state="Illinois", property_type="Townhouse",
        model="Rental", scenario="Conservative",
        price=250000, down_pct=0.30, annual_rate=0.078, rehab=28000,
        base_rent=2750, exit_year=5, target_irr=0.15,
    )   
    print("=== FULL RENTAL PARITY CHECK (Illinois/Townhouse/Rental/Conservative) ===\n")
    print(f"IRR:            {result['irr']*100:>8.2f}%    (v2: -5.14%; v3 -5.39% w/ documented upgrades)")
    print(f"Cash-on-cash:   {result['cash_on_cash']*100:>8.2f}%    (v2: -0.04%)")
    print(f"Min DSCR:       {result['min_dscr']:>8.2f}     (v2: 1.05)")
    print(f"Required rent:  ${result['required_rent']:>10,.2f} (v2: $3,296.52)")
    print(f"Rent cushion:   ${result['rent_cushion']:>10,.2f} (v2: -$546.52)")
    print(f"Verdict:        {result['verdict']:>10}   (v2: REJECT)")


        # --- Bad model must fail loudly ---
    try:
        analyze_deal(model="Condo")
        print("\nROUTER FAILED: unknown model accepted")
    except ValueError as e:
        print(f"\nBad model caught: {e}")


        # --- BRRR parity check (CA/Townhouse/BRRR/Base, $650K/$800K) ---
    b = analyze_deal(model="BRRR", state="California", property_type="Townhouse",
                     scenario="Base", price=650000, rehab=25000, base_rent=4500,
                     exit_year=5, target_irr=0.13, arv=800000, hm_ltv=0.85,
                     hm_rate=0.12, refi_ltv=0.75, refi_month=6, post_refi_rate=0.09)
    print("\n=== FULL BRRR PARITY CHECK (California/Townhouse/BRRR/Base) ===\n")
    print(f"IRR:              {b['irr']*100:.2f}%   (v2: 7.42%; v3 7.40% documented)")
    print(f"Cash invested:    ${b['cash_invested']:,.2f}   (v2: $140,375.00)")
    print(f"Cash pulled out:  ${b['cash_pulled_out']:,.2f}   (v2: $47,500.00)")
    print(f"Cash left:        ${b['cash_left']:,.2f}   (v2: $92,875.00)")
    print(f"Post-refi CF:     ${b['post_refi_cash_flow']:,.2f}   (v2: -$29,850.95; v3 -$29,937.35 documented)")
    print(f"Cash-on-cash:     {b['cash_on_cash']*100:.2f}%   (v2: -32.14%; v3 -32.23% documented)")
    print(f"DSCR:             {b['dscr']:.3f}   (v2: 0.528)")
    print(f"DSCR w/ reserves: {b['dscr_with_reserves']:.3f}   (v2: 0.472)")
    print(f"Required rent:    ${b['required_rent']:,.2f}   (v2: $7,420.79 - v2 uses purchase loan)")
    print(f"Rent cushion:     ${b['rent_cushion']:,.2f}")
    print(f"Sale price:       ${b['sale_price']:,.2f}   (v2: $954,421.06)")
    print(f"Equity at exit:   ${b['equity_at_exit']:,.2f}   (v2: $375,653.71; v3 $376,140.69 B34 fix)")
    print(f"Verdict:          {b['verdict']}   (v2: HARD REJECT)")


    # --- Flip parity check (CA/Townhouse/Flip/Base, $650K/$800K) ---
    f = analyze_deal(model="Flip", state="California", property_type="Townhouse",
                     scenario="Base", price=650000, rehab=25000, arv=800000,
                     hm_ltv=0.85, hm_rate=0.12, hold_months=5, points_pct=0.02,
                     monthly_utilities=150.00, monthly_maint_security=150.00,
                     target_margin=0.13)
    print("\n=== FULL FLIP PARITY CHECK (California/Townhouse/Flip/Base) ===\n")
    print(f"HM loan:          ${f['hm_loan']:,.2f}   (v2: $552,500.00)")
    print(f"HM interest:      ${f['hm_interest']:,.2f}   (v2: $27,625.00)")
    print(f"HM points:        ${f['hm_points']:,.2f}   (v2: $11,050.00)")
    print(f"Closing costs:    ${f['closing_costs']:,.2f}   (v2: $17,875.00)")
    print(f"Monthly holding:  ${f['monthly_holding']:,.2f}   (v2: $1,347.92)")
    print(f"Total holding:    ${f['total_holding']:,.2f}   (v2: $6,739.58)")
    print(f"Selling cost:     ${f['selling_cost']:,.2f}   (v2: $52,000.00)")
    print(f"Total cost:       ${f['total_project_cost']:,.2f}   (v2: $790,289.58)")
    print(f"Net profit:       ${f['net_profit']:,.2f}   (v2: $9,710.42)")
    print(f"Cash invested:    ${f['cash_invested']:,.2f}   (v2: $237,789.58)")
    print(f"ROI on cash:      {f['roi_on_cash']:.2%}   (v2: 4.08%)")
    print(f"Annualized ROI:   {f['annualized_roi']:.2%}   (v2: 9.80%)")
    print(f"Profit margin:    {f['profit_margin']:.2%}   (v2: 1.21%)")
    print(f"Max Offer (MAO):  ${f['max_offer_mao']:,.2f}   (v2: $555,710.42)")
    print(f"Max Offer (70%):  ${f['max_offer_70pct']:,.2f}   (v2: $535,000.00)")
    print(f"Over/(Under):     ${f['over_under_mao']:,.2f}   (v2: $94,289.58)")
    print(f"Verdict:          {f['verdict']}   (v2: REJECT)")