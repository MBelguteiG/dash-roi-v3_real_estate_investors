import streamlit as st
from engine.analyze import analyze_deal
from engine.solvers import max_price_irr, max_price_dscr

st.set_page_config(page_title="Dash ROI Pro v3", layout="wide")


def money(x):
    return f"-${abs(x):,.0f}" if x < 0 else f"${x:,.0f}"


def money2(x):
    return f"-${abs(x):,.2f}" if x < 0 else f"${x:,.2f}"


# Top bar: name, model, scenario
left, mid, right = st.columns([2, 2, 3])
left.markdown("### Dash ROI Pro")
model = mid.segmented_control(
    "Model", ["Rental", "BRRR", "Flip"],
    default="Rental", label_visibility="collapsed") or "Rental"
scenario = right.segmented_control(
    "Scenario", ["Conservative", "Base", "Aggressive"],
    default="Base", label_visibility="collapsed") or "Base"

if model != "Rental":
    st.info(f"{model} inputs come in the next step.")
    st.stop()

# Input strip
with st.container(border=True):
    c = st.columns(8)
    state = c[0].selectbox("State", ["Illinois", "California"])
    property_type = c[1].selectbox("Type", ["SFH", "Condo", "Townhouse", "Duplex"])
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
result = analyze_deal(**deal)
irr_solve = max_price_irr(deal)
dscr_solve = max_price_dscr(deal)
solved = [s["price"] for s in (irr_solve, dscr_solve) if s["status"] == "SOLVED"]
walk_away = min(solved) if solved else None

# Headline tiles
verdict = result["verdict"]
if "REJECT" in verdict:
    bg = "#8A1C12"
elif verdict == "NEGOTIATE":
    bg = "#B45309"
else:
    bg = "#1E7A4C"

t = st.columns(5)
t[0].markdown(
    f'<div style="background:{bg};color:#FFFFFF;border-radius:10px;'
    f'padding:14px 18px"><div style="font-size:13px;letter-spacing:0.08em;'
    f'text-transform:uppercase">Verdict</div>'
    f'<div style="font-size:24px;font-weight:700">{verdict}</div></div>',
    unsafe_allow_html=True)
with t[1].container(border=True):
    st.metric("IRR", f"{result['irr']:.2%}")
    st.caption(f"target {target:.2f}%")
with t[2].container(border=True):
    st.metric("Min DSCR", f"{result['min_dscr']:.2f}")
    st.caption("lender minimum 1.20")
with t[3].container(border=True):
    st.metric("Cash-on-cash", f"{result['cash_on_cash']:.2%}")
    st.caption("year 1")
with t[4].container(border=True):
    st.metric("Walk-away price", money(walk_away) if walk_away else "none")
    st.caption(f"vs {money(price)} asking")

# Tabs
inv, lend, sens, cf = st.tabs(
    ["Investor view", "Lender view", "Sensitivity", "Cash flow table"])

with inv:
    a, b = st.columns(2)
    with a:
        st.markdown("#### Why this verdict")
        debt = f"Debt check: DSCR {result['min_dscr']:.2f} vs 1.20 minimum"
        if result["min_dscr"] >= 1.20:
            st.success(debt)
        else:
            st.error(debt)
        ret = f"Return check: IRR {result['irr']:.2%} vs {target:.2f}% target"
        if result["irr"] >= target / 100:
            st.success(ret)
        else:
            st.error(ret)
    with b:
        st.markdown("#### What would make it work")
        st.write(f"Rent needed for 1.20 DSCR: **{money2(result['required_rent'])}**")
        if irr_solve["status"] == "SOLVED":
            st.write(f"Max price at {target:.2f}% IRR: **{money(irr_solve['price'])}**")
        if dscr_solve["status"] == "SOLVED":
            st.write(f"Max price at 1.20 DSCR: **{money(dscr_solve['price'])}**")

with lend:
    st.info("Lender view comes in Week 23.")
with sens:
    st.info("Sensitivity comes in Phase 6.")
with cf:
    st.info("Cash flow table comes later.")