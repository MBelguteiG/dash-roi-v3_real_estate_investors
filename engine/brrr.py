from engine.projection import project

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

def rate_term_ltv(arv, refi_ltv, purchase_price, hm_ltv):
    """
    Rate/term refi: the new loan only pays off the hard-money principal
    (no cash out), capped by the lender's max refi LTV. Returned as an
    effective LTV on ARV so every downstream refi calculation is unchanged.
    """
    payoff = hard_money_loan(purchase_price, hm_ltv)
    return min(refi_ltv, payoff / arv)


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

from engine.amortization import annual_debt_service, schedule


def post_refi_dscr(post_refi_noi, refi_loan_amt, post_refi_rate):
    """
    Lender-view post-refi DSCR (v2 Property_inputs B39):
    NOI / post-refi annual debt service, on a fresh 30-yr am. of the refi loan.
    """
    return post_refi_noi / annual_debt_service(refi_loan_amt, post_refi_rate)


def post_refi_dscr_with_reserves(post_refi_noi, reserve_amt, refi_loan_amt, post_refi_rate):
    """
    Investor-side conservative DSCR (v2 Property_inputs B40):
    (NOI - reserves) / post-refi annual debt service. Same denominator as B39.
    """
    return (post_refi_noi - reserve_amt) / annual_debt_service(refi_loan_amt, post_refi_rate)

def is_all_cash_out(raw_irr, cash_left):
    """
    Dual-signal all-cash-out test (v2 lesson: a deal with $22,125 cash left
    showed 11,156% IRR - checking cash alone misses it). One rule, used by
    both brrr_verdict() and the IRR solver guard.
    """
    return raw_irr > 1 or cash_left <= 0


def brrr_verdict(raw_irr, cash_left, dscr, target_irr, rent_cushion, dscr_min=1.20):
    """
    BRRR verdict (v2 Main_Dashboard B42, BRRR branch).
    DSCR is the sole hard gate at 1.20 (not 1.0 - a failed refi is fatal to
    the whole strategy, unlike Rental where sub-1.20 is merely "not financeable").
    All-cash-out deals (raw_irr > 1 OR cash_left <= 0) skip the IRR gate
    entirely - v2 achieves this as a side effect of Excel's text > number
    coercion on B27's "Initial Investment Recovered" display string; this is
    the explicit version of that same behavior.
    """
    all_cash_out = is_all_cash_out(raw_irr, cash_left)
    meets_irr = True if all_cash_out else (raw_irr >= target_irr)
    fails_badly = (not all_cash_out) and (raw_irr < target_irr * 0.5)

    if dscr < dscr_min:
        return "HARD REJECT"
    if fails_badly:
        return "REJECT"
    if meets_irr and rent_cushion > 0:
        return "STRONG BUY"
    if meets_irr:
        return "BUY"
    return "NEGOTIATE"

def years_held_post_refi(exit_years, refi_month):
    """
    Years the property is held/appreciating after the refi closes (v2 B29):
    Exit Years - (Refi Month / 12). Feeds the exit sale price appreciation
    calc, not the amortization schedule - refi_month here is just the
    same input used for a different purpose.
    """
    return exit_years - (refi_month / 12)


def build_brrr_schedule(hm_loan, hm_rate, refi_month, refi_loan_amt, post_refi_rate, exit_month):
    """
    Two-phase monthly schedule (v2 'BRRR Amortization' tab):
      Months 1..refi_month:      interest-only Hard Money (flat payment, balance never declines)
      Months refi_month+1..exit: fresh 30-yr amortization on the refi loan (reuses amortization.schedule)
    refi_month is a direct input (1-60+), not solved - the loop boundaries below
    shift automatically for whatever value is passed in.
    Returns a list of dicts: month, interest, principal, payment, balance, phase.
    """
    rows = []
    monthly_hm_interest = hm_loan * (hm_rate / 12)

    for month in range(1, refi_month + 1):
        rows.append({
            "month": month, "interest": monthly_hm_interest, "principal": 0.0,
            "payment": monthly_hm_interest, "balance": hm_loan, "phase": "Hard Money",
        })

    post_refi_rows = schedule(refi_loan_amt, post_refi_rate, term_months=360)
    for i, r in enumerate(post_refi_rows):
        month = refi_month + 1 + i
        if month > exit_month:
            break
        rows.append({
            "month": month, "interest": r["interest"], "principal": r["principal"],
            "payment": r["interest"] + r["principal"], "balance": r["balance"],
            "phase": "Post-Refi",
        })
    return rows



def sale_price_at_exit(arv, appreciation_rate, years_held):
    """v2 Property_inputs B30: ARV x (1+appreciation)^years_held_post_refi."""
    return arv * (1 + appreciation_rate) ** years_held


def brrr_selling_cost(sale_price, selling_pct):
    """v2 Property_inputs B33: Sale Price at Exit x Selling Cost %."""
    return sale_price * selling_pct


def brrr_net_sale_proceeds(sale_price, selling_cost_amt, remaining_balance):
    """v2 Property_inputs B35: Sale Price - Selling Cost - Remaining Loan Balance."""
    return sale_price - selling_cost_amt - remaining_balance


def build_brrr_stream(purchase_price, rehab, hm_ltv, hm_rate, refi_ltv, refi_month,
                       post_refi_rate, arv, appreciation_rate, exit_year, selling_pct,
                       cash_invested_amt, base_rent, vacancy_rate, tax_rate,
                       annual_insurance, hoa, base_maint, mgmt_rate, annual_capex,
                       rent_growth, tax_growth, inflation):
    """
    Annual Year 0..exit_year stream for BRRR IRR - sums the monthly
    hard-money/post-refi schedule into year buckets, injects cash-out and
    sale proceeds in the right years. Mirrors deal.py's build_stream().
    """
    hm_loan = hard_money_loan(purchase_price, hm_ltv)
    rl = refi_loan(arv, refi_ltv)
    pulled = cash_pulled_out(arv, refi_ltv, purchase_price, hm_ltv)
    exit_month = exit_year * 12

    schedule = build_brrr_schedule(hm_loan, hm_rate, refi_month, rl, post_refi_rate, exit_month)
    years = project(exit_year, base_rent, vacancy_rate, purchase_price, tax_rate,
                    annual_insurance, hoa, base_maint, mgmt_rate,
                    rent_growth, tax_growth, inflation)
    noi_by_year = {y["year"]: y["noi_annual"] for y in years}

    stream = [-cash_invested_amt]
    annual_flows = [0.0] * exit_year
    for row in schedule:
        year_idx = (row["month"] - 1) // 12
        if year_idx >= exit_year:
            continue
        noi = noi_by_year.get(year_idx + 1, 0)
        annual_flows[year_idx] += (noi - annual_capex) / 12 - row["payment"]
        if row["month"] == refi_month:
            annual_flows[year_idx] += pulled

    yh = years_held_post_refi(exit_year, refi_month)
    sale_price = sale_price_at_exit(arv, appreciation_rate, yh)
    sell_cost = brrr_selling_cost(sale_price, selling_pct)
    remaining_balance = schedule[-1]["balance"] if schedule else rl
    annual_flows[-1] += brrr_net_sale_proceeds(sale_price, sell_cost, remaining_balance)

    stream.extend(annual_flows)
    return stream


def build_brrr_monthly_stream(purchase_price, rehab, hm_ltv, hm_rate, refi_ltv, refi_month,
                              post_refi_rate, arv, appreciation_rate, exit_year, selling_pct,
                              cash_invested_amt, base_rent, vacancy_rate, tax_rate,
                              annual_insurance, hoa, base_maint, mgmt_rate, capex_rate,
                              rent_growth, tax_growth, inflation):
    """
    Monthly Month 0..exit stream (v2 'BRRR Amortization' col H):
    month 0 = -cash invested; each month = (NOI_year - CapEx)/12 - payment,
    + cash pulled out in refi month, + net sale proceeds in exit month.
    """
    hm_loan = hard_money_loan(purchase_price, hm_ltv)
    rl = refi_loan(arv, refi_ltv)
    pulled = cash_pulled_out(arv, refi_ltv, purchase_price, hm_ltv)
    exit_month = exit_year * 12

    sched = build_brrr_schedule(hm_loan, hm_rate, refi_month, rl, post_refi_rate, exit_month)
    years = project(exit_year, base_rent, vacancy_rate, purchase_price, tax_rate,
                    annual_insurance, hoa, base_maint, mgmt_rate,
                    rent_growth, tax_growth, inflation)
    noi_by_year = {y["year"]: y["noi_annual"] for y in years}
    capex_by_year = {y["year"]: y["rent"] * 12 * capex_rate for y in years}

    yh = years_held_post_refi(exit_year, refi_month)
    sale_price = sale_price_at_exit(arv, appreciation_rate, yh)
    sell_cost = brrr_selling_cost(sale_price, selling_pct)
    net_sale = brrr_net_sale_proceeds(sale_price, sell_cost, sched[-1]["balance"])

    stream = [-cash_invested_amt]
    for row in sched:
        m = row["month"]
        year = (m - 1) // 12 + 1
        cf = (noi_by_year[year] - capex_by_year[year]) / 12 - row["payment"]
        if m == refi_month:
            cf += pulled
        if m == exit_month:
            cf += net_sale
        stream.append(cf)
    return stream


def brrr_irr(monthly_stream):
    """v2 Property_inputs B38: (1 + monthly IRR)^12 - 1."""
    from engine.irr import irr
    return (1 + irr(monthly_stream)) ** 12 - 1



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


    # --- Post-refi DSCR + verdict ---
    ANNUAL_NOI = 15200.00        # v2 Cash Flow Projection N16 (Year 1)
    RESERVE = 2640.00            # v2 Cash Flow Projection N20 (CapEx/Reserve Year 1)
    POST_REFI_RATE = 0.09

    dscr = post_refi_dscr(ANNUAL_NOI, rl, POST_REFI_RATE)
    dscr_res = post_refi_dscr_with_reserves(ANNUAL_NOI, RESERVE, rl, POST_REFI_RATE)
    print(f"\nPost-refi DSCR (lender):     {dscr:.3f}   (v2: 0.466)")
    print(f"Post-refi DSCR (w/reserves): {dscr_res:.3f}   (v2: 0.385)")

    v = brrr_verdict(raw_irr=0.8521, cash_left=cash_left_in_deal(ci_v2, pulled),
                      dscr=dscr, target_irr=0.15, rent_cushion=-694.12)
    print(f"BRRR Verdict: {v}   (v2: HARD REJECT)")


    # --- Two-phase schedule + years held post-refi ---
    yh = years_held_post_refi(exit_years=5, refi_month=REFI_MONTH)
    print(f"\nYears held post-refi: {yh}   (v2: 4.500)")

    brrr_sched = build_brrr_schedule(hm, HM_RATE, REFI_MONTH, rl, POST_REFI_RATE, exit_month=60)
    print(f"Month 1 (HM phase):   interest ${brrr_sched[0]['interest']:,.2f}   (v2: $1,968.75)")
    print(f"Month 7 (1st post-refi): interest ${brrr_sched[6]['interest']:,.2f}, "
          f"principal ${brrr_sched[6]['principal']:,.2f}   (v2: $2,531.25 / $184.35)")


    # --- Full BRRR stream + IRR (current $650K/$800K reference deal) ---
    from engine.assumptions import get_assumptions

    a = get_assumptions("California", "Townhouse", "BRRR", "Base")
    vacancy_rate = a["VacancyRate% Annual"]
    maint_rate = a["Maintenance% Annual"]
    mgmt_rate = a["Management Fee"]
    capex_rate = a["CapEx% Annual"]
    tax_rate_b = a["PropertyTaxRate Annual"]
    selling_pct_b = a["SellingCost% Annual"]
    annual_insurance_b = a["Insurance Yearly"]
    hoa_b = a["HOA Monthly"]
    rent_growth = a["RentGrowth Annual"]
    tax_growth = a["Tax Growth"]
    inflation = a["Inflation Annual"]

    PURCHASE2 = 650000
    REHAB2 = 25000
    ARV2 = 800000
    HM_LTV2 = 0.85
    HM_RATE2 = 0.12
    REFI_LTV2 = 0.75
    REFI_MONTH2 = 6
    POST_REFI_RATE2 = 0.09
    BASE_RENT = 4500
    APPRECIATION = 0.04
    CASH_INVESTED = 140375.00   # v2 Property_inputs B27
    base_maint = BASE_RENT * maint_rate
    annual_capex = BASE_RENT * 12 * capex_rate

    monthly = build_brrr_monthly_stream(

    purchase_price=PURCHASE2, rehab=REHAB2, hm_ltv=HM_LTV2, hm_rate=HM_RATE2,
    refi_ltv=REFI_LTV2, refi_month=REFI_MONTH2, post_refi_rate=POST_REFI_RATE2,
    arv=ARV2, appreciation_rate=APPRECIATION, exit_year=5, selling_pct=selling_pct_b,
    cash_invested_amt=CASH_INVESTED, base_rent=BASE_RENT, vacancy_rate=vacancy_rate,
    tax_rate=tax_rate_b, annual_insurance=annual_insurance_b, hoa=hoa_b,
    base_maint=base_maint, mgmt_rate=mgmt_rate, capex_rate=capex_rate,
    rent_growth=rent_growth, tax_growth=tax_growth, inflation=inflation,

    )
    print("\n=== BRRR MONTHLY STREAM (current $650K/$800K deal) ===")
    print(f"Stream length: {len(monthly)}   (v2: 61)")
    print(f"Months 7-18 sum: ${sum(monthly[7:19]):,.2f}   (v2 B36: -$29,850.95)")
    print(f"BRRR IRR (monthly, annualized): {brrr_irr(monthly)*100:.2f}%   (v2 B38: 7.42%)")

    pulled2 = cash_pulled_out(ARV2, REFI_LTV2, PURCHASE2, HM_LTV2)
    coc = sum(monthly[7:19]) / cash_left_in_deal(CASH_INVESTED, pulled2)
    print(f"Cash-on-cash (post-refi): {coc*100:.2f}%   (v2: -32.14%)")

    yh2 = years_held_post_refi(5, REFI_MONTH2)
    sp = sale_price_at_exit(ARV2, APPRECIATION, yh2)
    rl2 = refi_loan(ARV2, REFI_LTV2)
    sched2 = build_brrr_schedule(hard_money_loan(PURCHASE2, HM_LTV2), HM_RATE2,
                                 REFI_MONTH2, rl2, POST_REFI_RATE2, exit_month=60)
    bal = sched2[-1]["balance"]
    print(f"Sale price at exit: ${sp:,.2f}   (v2: $954,421.06)")
    print(f"Remaining balance:  ${bal:,.2f}   (v2: $578,767.35)")
    print(f"Equity at exit:     ${sp - bal:,.2f}   (v2: $375,653.71)")


    print("\n=== Monthly checkpoints (compare to v2 BRRR Amortization col H) ===")
    for m in [1, 6, 7, 13, 19, 25, 37, 49, 59, 60]:
        print(f"  Month {m:>2}: {monthly[m]:>14,.2f}")

    print("\n=== v3 projection line items ===")
    for y in project(5, BASE_RENT, vacancy_rate, PURCHASE2, tax_rate_b,
                     annual_insurance_b, hoa_b, base_maint, mgmt_rate,
                     rent_growth, tax_growth, inflation):
        print(y)

        # --- Proof: v2's exact inputs through v3's stream logic -> should be 7.42% ---
    v2_noi = {1: 30595.00, 2: 32048.76, 3: 33560.99, 4: 35133.98, 5: 36770.10}
    v2_capex = {1: 3240.00, 2: 3240.00, 3: 3490.92, 4: 3623.57, 5: 3761.27}
    test = [-CASH_INVESTED]
    for row in sched2:
        m = row["month"]
        yr = (m - 1) // 12 + 1
        cf = (v2_noi[yr] - v2_capex[yr]) / 12 - row["payment"]
        if m == REFI_MONTH2:
            cf += pulled2
        if m == 60:
            cf += 308844.24          # v2 B35 net sale proceeds
        test.append(cf)
    print(f"\nProof IRR (v2 inputs): {brrr_irr(test)*100:.2f}%   (v2 B38: 7.42%)")