import streamlit as st
from engine.analyze import analyze_deal
from engine.solvers import max_price_irr, max_price_dscr, max_price_all_cash_out
from engine.verdict import approval_likelihood

st.set_page_config(page_title="Dash ROI Pro v3", layout="wide")


def money(x):
    return f"-${abs(x):,.0f}" if x < 0 else f"${x:,.0f}"


def money2(x):
    return f"-${abs(x):,.2f}" if x < 0 else f"${x:,.2f}"


def verdict_tile(col, verdict):
    if "REJECT" in verdict:
        bg = "#8A1C12"
    elif verdict == "NEGOTIATE":
        bg = "#B45309"
    else:
        bg = "#1E7A4C"
    col.markdown(
        f'<div style="background:{bg};color:#FFFFFF;border-radius:10px;'
        f'padding:14px 18px"><div style="font-size:13px;letter-spacing:0.08em;'
        f'text-transform:uppercase">Verdict</div>'
        f'<div style="font-size:24px;font-weight:700">{verdict}</div></div>',
        unsafe_allow_html=True)


def tile(col, label, value, caption):
    with col.container(border=True):
        st.metric(label, value)
        st.caption(caption)


def check(text, ok):
    if ok:
        st.success(text)
    else:
        st.error(text)


# Top bar: name, model, scenario
left, mid, right = st.columns([2, 2, 3])
left.markdown("### Dash ROI Pro")
model = mid.segmented_control(
    "Model", ["Rental", "BRRR", "Flip"],
    default="Rental", label_visibility="collapsed") or "Rental"
scenario = right.segmented_control(
    "Scenario", ["Conservative", "Base", "Aggressive"],
    default="Base", label_visibility="collapsed") or "Base"

# Input strip
with st.container(border=True):
    c = st.columns(8)
    state = c[0].selectbox("State", ["Illinois", "California"])
    property_type = c[1].selectbox("Type", ["SFH", "Condo", "Townhouse", "Duplex"])
    if model == "Rental":
        price = c[2].number_input("Price", value=340000, step=5000)
        down_pct = c[3].number_input("Down %", value=25.0, step=1.0)
        rate = c[4].number_input("Rate %", value=6.75, step=0.125)
        rent = c[5].number_input("Rent / mo", value=2300, step=50)
        exit_year = c[6].number_input("Exit year", value=5, min_value=1, step=1)
        target = c[7].number_input("Target IRR %", value=8.0, step=0.5)
        deal = dict(model="Rental", state=state, property_type=property_type,
                    scenario=scenario, price=price, down_pct=down_pct / 100,
                    annual_rate=rate / 100, rehab=0, base_rent=rent,
                    exit_year=exit_year, target_irr=target / 100)
    elif model == "BRRR":
        price = c[2].number_input("Price", value=250000, step=5000)
        rehab = c[3].number_input("Rehab", value=45000, step=1000)
        arv = c[4].number_input("ARV", value=340000, step=5000)
        rent = c[5].number_input("Rent / mo", value=2400, step=50)
        exit_year = c[6].number_input("Exit year", value=5, min_value=1, step=1)
        target = c[7].number_input("Target IRR %", value=10.0, step=0.5)
        d = st.columns(8)
        hm_ltv = d[0].number_input("HM LTV %", value=90.0, step=1.0)
        hm_rate = d[1].number_input("HM rate %", value=10.5, step=0.25)
        refi_month = d[2].number_input("Refi month", value=6, min_value=1, step=1)
        refi_ltv = d[3].number_input("Refi LTV %", value=75.0, step=1.0)
        post_rate = d[4].number_input("Refi rate %", value=7.25, step=0.125)
        deal = dict(model="BRRR", state=state, property_type=property_type,
                    scenario=scenario, price=price, rehab=rehab,
                    base_rent=rent, exit_year=exit_year,
                    target_irr=target / 100, arv=arv, hm_ltv=hm_ltv / 100,
                    hm_rate=hm_rate / 100, refi_ltv=refi_ltv / 100,
                    refi_month=refi_month, post_refi_rate=post_rate / 100)
    else:
        price = c[2].number_input("Price", value=200000, step=5000)
        rehab = c[3].number_input("Rehab", value=55000, step=1000)
        arv = c[4].number_input("ARV", value=340000, step=5000)
        hold = c[5].number_input("Hold months", value=6, min_value=1, step=1)
        target = c[6].number_input("Target margin %", value=15.0, step=0.5)
        d = st.columns(8)
        hm_ltv = d[0].number_input("HM LTV %", value=90.0, step=1.0)
        hm_rate = d[1].number_input("HM rate %", value=10.5, step=0.25)
        points = d[2].number_input("Points %", value=2.0, step=0.25)
        utilities = d[3].number_input("Utilities / mo", value=150, step=25)
        maint = d[4].number_input("Maint & security / mo", value=150, step=25)
        deal = dict(model="Flip", state=state, property_type=property_type,
                    scenario=scenario, price=price, rehab=rehab, arv=arv,
                    hm_ltv=hm_ltv / 100, hm_rate=hm_rate / 100,
                    hold_months=hold, points_pct=points / 100,
                    monthly_utilities=utilities,
                    monthly_maint_security=maint,
                    target_margin=target / 100)

result = analyze_deal(**deal)
verdict = result["verdict"]

# Headline tiles
t = st.columns(5)
verdict_tile(t[0], verdict)

if model == "Rental":
    irr_solve = max_price_irr(deal)
    dscr_solve = max_price_dscr(deal)
    solved = [s["price"] for s in (irr_solve, dscr_solve) if s["status"] == "SOLVED"]
    walk_away = min(solved) if solved else None
    dscr_value = result["min_dscr"]
    irr_ok = result["irr"] >= target / 100
    tile(t[1], "IRR", f"{result['irr']:.2%}", f"target {target:.2f}%")
    tile(t[2], "Min DSCR", f"{dscr_value:.2f}", "lender minimum 1.20")
    tile(t[3], "Cash-on-cash", f"{result['cash_on_cash']:.2%}", "year 1")
elif model == "BRRR":
    irr_solve = max_price_irr(deal)
    aco = max_price_all_cash_out(deal)
    walk_away = irr_solve["price"] if irr_solve["status"] == "SOLVED" else None
    dscr_value = result["dscr"]
    if result["all_cash_out"]:
        tile(t[1], "IRR", "All cash out", "no cash left in the deal")
        irr_ok = True
    else:
        tile(t[1], "IRR", f"{result['irr']:.2%}", f"target {target:.2f}%")
        irr_ok = result["irr"] >= target / 100
    tile(t[2], "Post-refi DSCR", f"{dscr_value:.2f}", "lender minimum 1.20")
    if result["cash_left"] < 0:
        tile(t[3], "Cash left in deal", "$0",
             f"refi returns {money(-result['cash_left'])} more than invested")
    else:
        tile(t[3], "Cash left in deal", money(result["cash_left"]),
             f"of {money(result['cash_invested'])} invested")
else:
    walk_away = result["max_offer_mao"]
    tile(t[1], "Annualized ROI", f"{result['annualized_roi']:.2%}",
         f"{hold}-month hold")
    tile(t[2], "Profit margin", f"{result['profit_margin']:.2%}",
         f"target {target:.2f}%")
    tile(t[3], "Net profit", money(result["net_profit"]),
         f"holding {money(result['monthly_holding'])} / mo")

if walk_away:
    tile(t[4], "Walk-away price", money(walk_away), f"vs {money(price)} asking")
elif model == "BRRR" and result["all_cash_out"]:
    tile(t[4], "Walk-away price", "n/a", "IRR solver skips all-cash-out deals")
else:
    tile(t[4], "Walk-away price", "none", "no price meets the target")

# Tabs
inv, lend, sens, cf = st.tabs(
    ["Investor view", "Lender view", "Sensitivity", "Cash flow table"])

with inv:
    a, b = st.columns(2)
    with a:
        st.markdown("#### Why this verdict")
        if model == "Flip":
            margin = result["profit_margin"]
            check(f"Profit check: net profit {money(result['net_profit'])}",
                  result["net_profit"] > 0)
            check(f"Margin floor: {margin:.2%} vs 10.00% minimum", margin >= 0.10)
            check(f"Margin target: {margin:.2%} vs {target:.2f}% target",
                  margin >= target / 100)
        else:
            check(f"Debt check: DSCR {dscr_value:.2f} vs 1.20 minimum",
                  dscr_value >= 1.20)
            if model == "BRRR" and result["all_cash_out"]:
                check("Return check: the refi returns all the cash invested", True)
            else:
                check(f"Return check: IRR {result['irr']:.2%} vs {target:.2f}% target",
                      irr_ok)
    with b:
        st.markdown("#### What would make it work")
        if model == "Flip":
            over = result["over_under_mao"]
            mao = money(result["max_offer_mao"])
            if over > 0:
                line = f"Max offer (MAO): **{mao}**, {money(over)} below the asking price"
            else:
                line = f"Max offer (MAO): **{mao}**; the price is already {money(-over)} under it"
            st.write(line.replace("$", "\\$"))
        else:
            st.write(f"Rent needed for 1.20 DSCR: **{money2(result['required_rent'])}**")
            if irr_solve["status"] == "SOLVED":
                st.write(f"Max price at {target:.2f}% IRR: **{money(irr_solve['price'])}**")
            if model == "Rental" and dscr_solve["status"] == "SOLVED":
                st.write(f"Max price at 1.20 DSCR: **{money(dscr_solve['price'])}**")
            if model == "BRRR" and aco["status"] == "SOLVED":
                st.write(f"Price for all cash out at refi: **{money(aco['price'])}**")

with lend:
    if model == "Rental":
        approval = approval_likelihood("Rental", result["min_dscr"], result["ltv"])
        l = st.columns(4)
        tile(l[0], "Loan amount", money(result["loan_amount"]),
             f"{result['ltv']:.0%} loan-to-value")
        tile(l[1], "NOI, year 1", money(result["noi_y1"]), "after vacancy and expenses")
        tile(l[2], "Debt service / yr", money(result["annual_debt_service"]),
             f"{rate:.3f}% fixed, 30 years")
        tile(l[3], "Min DSCR", f"{result['min_dscr']:.2f}", "1.20 minimum, 1.25 for strong")
        note = (f"DSCR {result['min_dscr']:.2f} at {result['ltv']:.0%} LTV. Strong needs "
                "DSCR 1.25 and LTV 80% or less; conditional needs DSCR 1.20.")
    elif model == "BRRR":
        refi = refi_ltv / 100
        approval = approval_likelihood("BRRR", result["dscr"], refi)
        l = st.columns(4)
        tile(l[0], "ARV", money(arv), "refi appraisal basis")
        tile(l[1], "Refi LTV", f"{refi:.0%}", f"refi at month {refi_month}")
        tile(l[2], "Cash pulled out", money(result["cash_pulled_out"]), "at refi")
        tile(l[3], "Post-refi DSCR", f"{result['dscr']:.2f}", "1.20 minimum, 1.25 for strong")
        note = (f"Post-refi DSCR {result['dscr']:.2f} at {refi:.0%} refi LTV. Strong needs "
                "DSCR 1.25 and LTV 80% or less; conditional needs DSCR 1.20.")
    else:
        hm_ltv_arv = result["hm_loan"] / arv
        ltc = result["hm_loan"] / (price + rehab)
        approval = approval_likelihood("Flip", hm_ltv_on_arv=hm_ltv_arv)
        l = st.columns(4)
        tile(l[0], "Hard money loan", money(result["hm_loan"]),
             f"{hm_ltv:.0f}% of purchase price")
        tile(l[1], "LTV on ARV", f"{hm_ltv_arv:.2%}", "75% ceiling")
        tile(l[2], "Loan-to-cost", f"{ltc:.2%}", "loan / (price + rehab)")
        tile(l[3], "Exit timeline", f"{hold} months", "hold period")
        if approval == "LIKELY":
            note = (f"HM LTV {hm_ltv_arv:.2%} of ARV, under the 75% ceiling. "
                    "A hard money lender is likely to fund.")
        else:
            note = (f"HM LTV {hm_ltv_arv:.2%} of ARV, over the 75% ceiling. "
                    "Expect the lender to cut the loan or decline.")

    st.markdown("#### Fundability")
    if approval in ("STRONG", "LIKELY"):
        st.success(f"{approval}: {note}")
    elif approval == "CONDITIONAL":
        st.warning(f"{approval}: {note}")
    else:
        st.error(f"{approval}: {note}")
        
with sens:
    st.info("Sensitivity comes in Phase 6.")
with cf:
    st.info("Cash flow table comes later.")