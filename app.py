import streamlit as st
from engine.analyze import analyze_deal
from engine.solvers import max_price_irr, max_price_dscr, max_price_all_cash_out

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

if model == "Flip":
    st.info("Flip inputs come in the next step.")
    st.stop()

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
    else:
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

result = analyze_deal(**deal)
verdict = result["verdict"]
irr_solve = max_price_irr(deal)

# Headline tiles
t = st.columns(5)
verdict_tile(t[0], verdict)

if model == "Rental":
    dscr_solve = max_price_dscr(deal)
    solved = [s["price"] for s in (irr_solve, dscr_solve) if s["status"] == "SOLVED"]
    walk_away = min(solved) if solved else None
    dscr_value = result["min_dscr"]
    irr_ok = result["irr"] >= target / 100
    tile(t[1], "IRR", f"{result['irr']:.2%}", f"target {target:.2f}%")
    tile(t[2], "Min DSCR", f"{dscr_value:.2f}", "lender minimum 1.20")
    tile(t[3], "Cash-on-cash", f"{result['cash_on_cash']:.2%}", "year 1")
else:
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
        check(f"Debt check: DSCR {dscr_value:.2f} vs 1.20 minimum",
              dscr_value >= 1.20)
        if model == "BRRR" and result["all_cash_out"]:
            check("Return check: the refi returns all the cash invested", True)
        else:
            check(f"Return check: IRR {result['irr']:.2%} vs {target:.2f}% target",
                  irr_ok)
    with b:
        st.markdown("#### What would make it work")
        st.write(f"Rent needed for 1.20 DSCR: **{money2(result['required_rent'])}**")
        if irr_solve["status"] == "SOLVED":
            st.write(f"Max price at {target:.2f}% IRR: **{money(irr_solve['price'])}**")
        if model == "Rental" and dscr_solve["status"] == "SOLVED":
            st.write(f"Max price at 1.20 DSCR: **{money(dscr_solve['price'])}**")
        if model == "BRRR" and aco["status"] == "SOLVED":
            st.write(f"Price for all cash out at refi: **{money(aco['price'])}**")

with lend:
    st.info("Lender view comes in Week 23.")
with sens:
    st.info("Sensitivity comes in Phase 6.")
with cf:
    st.info("Cash flow table comes later.")