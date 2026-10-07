import streamlit as st
from engine.analyze import analyze_deal

st.set_page_config(page_title="Dash ROI Pro v3", layout="wide")
st.title("Dash ROI Pro v3")


def money(x):
    return f"-${abs(x):,.2f}" if x < 0 else f"${x:,.2f}"


with st.sidebar:
    st.header("Deal inputs")
    model = st.selectbox("Model", ["Rental", "BRRR", "Flip"])
    state = st.selectbox("State", ["Illinois", "California"])
    property_type = st.selectbox("Property type",
                                 ["SFH", "Condo", "Townhouse", "Duplex"])
    price = st.number_input("Purchase price", value=340000, step=5000)
    if model == "Rental":
        down_pct = st.number_input("Down payment %", value=25.0, step=1.0)
        rate = st.number_input("Interest rate %", value=6.75, step=0.125)
        rent = st.number_input("Monthly rent", value=2300, step=50)
        exit_year = st.number_input("Exit year", value=5, min_value=1, step=1)
        target = st.number_input("Target IRR %", value=8.0, step=0.5)

if model == "Rental":
    result = analyze_deal(
        model="Rental", state=state, property_type=property_type,
        scenario="Base", price=price, down_pct=down_pct / 100,
        annual_rate=rate / 100, rehab=0, base_rent=rent,
        exit_year=exit_year, target_irr=target / 100)

    verdict = result["verdict"]
    if "REJECT" in verdict:
        st.error(f"Verdict: {verdict}")
    elif verdict == "NEGOTIATE":
        st.warning(f"Verdict: {verdict}")
    else:
        st.success(f"Verdict: {verdict}")

    c1, c2, c3 = st.columns(3)
    c1.metric("IRR", f"{result['irr']:.2%}")
    c2.metric("Cash-on-cash", f"{result['cash_on_cash']:.2%}")
    c3.metric("Min DSCR", f"{result['min_dscr']:.2f}")

    c4, c5, c6 = st.columns(3)
    c4.metric("Required rent", money(result["required_rent"]))
    c5.metric("Rent cushion", money(result["rent_cushion"]))
else:
    st.info("BRRR and Flip inputs come in the next step.")