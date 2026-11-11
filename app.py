import streamlit as st
from engine.analyze import analyze_deal
from engine.solvers import max_price_irr, max_price_dscr, max_price_all_cash_out
from engine.verdict import approval_likelihood, DSCR_STRONG
import plotly.graph_objects as go
import pandas as pd
from engine.sensitivity import two_way_irr, tornado_irr, brrr_tornado_irr
from engine.assumptions import get_assumptions

from i18n import tr, LANG_NAMES, mn_ord




st.set_page_config(page_title="Dash ROI Pro v3", layout="wide")

st.markdown(
    """<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    [data-testid="stAppViewContainer"] *:not([data-testid="stIconMaterial"]) {
            font-family: 'Inter', sans-serif !important;
    }
    [data-testid="stMetricLabel"], [data-testid="stMetricLabel"] * {
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;
    }
    </style>""",
    unsafe_allow_html=True,
)


def money(x):
    return f"-${abs(x):,.0f}" if x < 0 else f"${x:,.0f}"


def money2(x):
    return f"-${abs(x):,.2f}" if x < 0 else f"${x:,.2f}"


def verdict_tile(col, verdict, label, shown):
    if "REJECT" in verdict:
        bg = "#8A1C12"
    elif verdict == "NEGOTIATE":
        bg = "#B45309"
    else:
        bg = "#1E7A4C"
    col.markdown(
        f'<div style="background:{bg};color:#FFFFFF;border-radius:10px;'
        f'padding:14px 18px"><div style="font-size:13px;letter-spacing:0.08em;'
        f'text-transform:uppercase">{label}</div>'
        f'<div style="font-size:24px;font-weight:700">{shown}</div></div>',
        unsafe_allow_html=True)


def tile(col, label, value, caption):
    with col.container(border=True):
        st.metric(label, value)
        st.caption(caption.replace("$", "\\$"))


def check(text, ok):
    if ok:
        st.success(text)
    else:
        st.error(text)

def driver_note(rows, base, names):
    top = next((r for r in rows if not r.get("all_cash_out")), None)
    if top is None:
        return
    name = var_name(top["variable"]).lower()
    lo, hi = sorted((top["low"], top["high"]))
    st.markdown(T("s_driver", name=name, lo=f"{lo:.2%}", hi=f"{hi:.2%}", base=f"{base:.2%}"))

def tornado_chart(names, rows, base, height):
    fig = go.Figure()
    for label, pick, colour in ((T("s_helps"), max, "#2a78d6"),
                                (T("s_hurts"), min, "#A0AEC0")):
        values, moves = [], []
        for r in rows:
            v = pick(r["low"], r["high"])
            values.append(v)
            moves.append(T("s_lower") if v == r["low"] else T("s_higher"))
        fig.add_trace(go.Bar(
            name=label, y=names, orientation="h",
            x=[v - base for v in values], base=[base] * len(values),
            marker_color=colour, customdata=list(zip(values, moves)),
            hovertemplate=T("s_hover"),
        ))
    fig.add_vline(x=base, line_dash="dot", line_color="#4A5568",
                  annotation_text=T("s_line", base=f"{base:.2%}"),
                  annotation_position="top")
    fig.update_layout(
        title=T("s_title", base=f"{base:.2%}"),
        barmode="overlay", height=height,
        xaxis={"title": T("t_return"), "tickformat": ".1%"},
        yaxis={"type": "category", "autorange": "reversed"},
        legend={"orientation": "h", "y": -0.2},
        margin={"t": 50, "l": 10, "r": 10, "b": 10},
        plot_bgcolor="#FFFFFF",
    )
    return fig


PLAIN = {"ARV": "Value after repairs", "Rehab": "Repair budget",
         "Refi LTV": "New loan % of value", "Post-refi rate": "New loan rate",
         "Rate": "Loan rate", "Interest rate": "Loan rate",
         "Vacancy": "Empty months", "Rent growth": "Rent increases",
         "Appreciation": "Home value growth",
         "Vacancy rate": "Empty months", "Rehab cost": "Repair budget"}


def var_name(v):
    """Chart row name: engine name -> plain English -> chosen language."""
    en = PLAIN.get(v, v)
    return T("var_" + en, default=en)

# Top bar: name, model, scenario, language
left, mid, right, lang_col = st.columns([2, 2, 3, 1.5])
lang = lang_col.segmented_control(
    "Language", ["en", "mn"], format_func=lambda k: LANG_NAMES[k],
    default="en", label_visibility="collapsed") or "en"
T = tr(lang)
left.markdown("### Dash ROI Pro")
model = mid.segmented_control(
    T("strategy"), ["Rental", "BRRR", "Flip"], format_func=lambda m: T("model_" + m),
    default="Rental", key="model") or "Rental"
scenario = right.segmented_control(
    T("scenario"), ["Conservative", "Base", "Aggressive"], format_func=lambda s: T("sc_" + s),
    default="Base", key="scenario") or "Base"
with st.expander(T("quick_start")):
    st.markdown(T("quick_body"))


def K(name):
    """Widget key per model, so values survive a language switch."""
    return f"{model}_{name}"


# Input strip
with st.container(border=True):
    c = st.columns(8)
    STATES = ["Illinois", "California"]
    TYPES = ["SFH", "Condo", "Townhouse", "Duplex"]
    state = c[0].selectbox(T("state"), STATES,
                           index=STATES.index(st.session_state.get("state_val", "Illinois")),
                           format_func=lambda s: T("st_" + s), key=f"state_{lang}")
    property_type = c[1].selectbox(T("type"), TYPES,
                                   index=TYPES.index(st.session_state.get("ptype_val", "SFH")),
                                   format_func=lambda p: T("pt_" + p), key=f"ptype_{lang}")
    st.session_state["state_val"] = state
    st.session_state["ptype_val"] = property_type
    if model == "Rental":
        price = c[2].number_input(T("price"), value=340000, step=5000,
                                  help=T("h_price"), key=K("price"))
        down_pct = c[3].number_input(T("down"), value=25.0, step=1.0,
                                     help=T("h_down"), key=K("down"))
        rate = c[4].number_input(T("rate"), value=6.75, step=0.125, format="%.3f",
                                 help=T("h_rate"), key=K("rate"))
        rent = c[5].number_input(T("rent"), value=2300, step=50,
                                 help=T("h_rent"), key=K("rent"))
        exit_year = c[6].number_input(T("years"), value=5, min_value=1, step=1,
                                      help=T("h_years"), key=K("years"))
        target = c[7].number_input(T("goal"), value=8.0, step=0.5,
                                   help=T("h_goal"), key=K("goal"))
        deal = dict(model="Rental", state=state, property_type=property_type,
                    scenario=scenario, price=price, down_pct=down_pct / 100,
                    annual_rate=rate / 100, rehab=0, base_rent=rent,
                    exit_year=exit_year, target_irr=target / 100)
    elif model == "BRRR":
        price = c[2].number_input(T("price"), value=250000, step=5000,
                                  help=T("h_price_before"), key=K("price"))
        rehab = c[3].number_input(T("rehab"), value=45000, step=1000,
                                  help=T("h_rehab"), key=K("rehab"))
        arv = c[4].number_input(T("arv"), value=340000, step=5000,
                                help=T("h_arv"), key=K("arv"))
        rent = c[5].number_input(T("rent"), value=2400, step=50,
                                 help=T("h_rent_brrr"), key=K("rent"))
        exit_year = c[6].number_input(T("years"), value=5, min_value=1, step=1,
                                      help=T("h_years"), key=K("years"))
        target = c[7].number_input(T("goal"), value=10.0, step=0.5,
                                   help=T("h_goal"), key=K("goal"))
        d = st.columns([1, 1, 1, 1, 1, 1, 2])
        hm_ltv = d[0].number_input(T("hm_ltv"), value=90.0, step=1.0,
                                   help=T("h_hm_ltv"), key=K("hm_ltv"))
        hm_rate = d[1].number_input(T("hm_rate"), value=10.5, step=0.25,
                                    help=T("h_hm_rate"), key=K("hm_rate"))
        refi_month = d[2].number_input(T("refi_month"), value=6, min_value=1, step=1,
                                       help=T("h_refi_month"), key=K("refi_month"))
        refi_ltv = d[3].number_input(T("refi_ltv"), value=75.0, step=1.0,
                                     help=T("h_refi_ltv"), key=K("refi_ltv"))
        post_rate = d[4].number_input(T("post_rate"), value=7.25, step=0.125,
                                      help=T("h_post_rate"), key=K("post_rate"))
        REFI = ["Cash-Out", "Rate/Term"]
        refi_type = d[5].selectbox(T("refi_type"), REFI,
                                   index=REFI.index(st.session_state.get("refi_val", "Cash-Out")),
                                   format_func=lambda r: T("rt_" + r),
                                   help=T("h_refi_type"), key=f"refi_{lang}")
        st.session_state["refi_val"] = refi_type
        deal = dict(model="BRRR", state=state, property_type=property_type,
                    scenario=scenario, price=price, rehab=rehab,
                    base_rent=rent, exit_year=exit_year,
                    target_irr=target / 100, arv=arv, hm_ltv=hm_ltv / 100,
                    hm_rate=hm_rate / 100, refi_ltv=refi_ltv / 100,
                    refi_month=refi_month, post_refi_rate=post_rate / 100,
                    refi_type=refi_type)
    else:
        price = c[2].number_input(T("price"), value=200000, step=5000,
                                  help=T("h_price_before"), key=K("price"))
        rehab = c[3].number_input(T("rehab"), value=55000, step=1000,
                                  help=T("h_rehab"), key=K("rehab"))
        arv = c[4].number_input(T("arv_flip"), value=340000, step=5000,
                                help=T("h_arv_flip"), key=K("arv"))
        hold = c[5].number_input(T("hold"), value=6, min_value=1, step=1,
                                 help=T("h_hold"), key=K("hold"))
        target = c[6].number_input(T("profit_goal"), value=15.0, step=0.5,
                                   help=T("h_profit_goal"), key=K("goal"))
        d = st.columns([1, 1, 1, 1, 1, 3])
        hm_ltv = d[0].number_input(T("hm_ltv"), value=90.0, step=1.0,
                                   help=T("h_hm_ltv"), key=K("hm_ltv"))
        hm_rate = d[1].number_input(T("hm_rate"), value=10.5, step=0.25,
                                    help=T("h_hm_rate"), key=K("hm_rate"))
        points = d[2].number_input(T("lender_fee"), value=2.0, step=0.25,
                                   help=T("h_lender_fee"), key=K("lender_fee"))
        utilities = d[3].number_input(T("utilities"), value=150, step=25,
                                      help=T("h_utilities"), key=K("utilities"))
        maint = d[4].number_input(T("upkeep"), value=150, step=25,
                                  help=T("h_upkeep"), key=K("upkeep"))
        deal = dict(model="Flip", state=state, property_type=property_type,
                    scenario=scenario, price=price, rehab=rehab, arv=arv,
                    hm_ltv=hm_ltv / 100, hm_rate=hm_rate / 100,
                    hold_months=hold, points_pct=points / 100,
                    monthly_utilities=utilities,
                    monthly_maint_security=maint,
                    target_margin=target / 100)
    defaults = get_assumptions(state, property_type, model, scenario)
    default_hoa = defaults["HOA Monthly"]
    h = st.columns([1, 1, 1, 1, 1, 3])
    hoa_in = h[0].number_input(
        T("hoa"), value=None, min_value=0.0, step=25.0,
        placeholder=T("hoa_default", x=money(default_hoa)),
        help=T("h_hoa"), key=K("hoa"))
    if hoa_in is not None:
        deal["hoa_override"] = hoa_in
    tax_in = h[2].number_input(
        T("tax_yr"), value=None, min_value=0.0, step=100.0,
        placeholder=money(price * defaults["PropertyTaxRate Annual"]),
        help=T("h_tax_yr"), key=K("tax_yr"))
    if tax_in is not None:
        deal["tax_override"] = tax_in
    ins_in = h[3].number_input(
        T("ins_yr"), value=None, min_value=0.0, step=100.0,
        placeholder=money(defaults["Insurance Yearly"]),
        help=T("h_ins_yr"), key=K("ins_yr"))
    if ins_in is not None:
        deal["insurance_override"] = ins_in
    dscr_min = 1.00   # Flip has no DSCR; kept so shared text calls work
    if model in ("Rental", "BRRR"):
        buy_pts = h[1].number_input(
            T("points"), min_value=0.0, max_value=4.0,
            value=0.0, step=0.5, help=T("h_points"), key=K("points"))
        deal["points"] = buy_pts
        dscr_min = h[4].number_input(
            T("dscr_min"), min_value=0.50, max_value=2.00, value=1.00, step=0.05,
            format="%.2f", help=T("h_dscr_min"), key=K("dscr_min"))
        deal["dscr_min"] = dscr_min



try:
    result = analyze_deal(**deal)
except (ValueError, ZeroDivisionError) as e:
    st.error(f"{e} Fix that box above and the numbers will update.")
    st.stop()
verdict = result["verdict"]

# Headline tiles
t = st.columns(5)
verdict_tile(t[0], verdict, T("verdict"), T("v_" + verdict, default=verdict))

if model == "Rental":
    irr_solve = max_price_irr(deal)
    dscr_solve = max_price_dscr(deal)
    solved = [s["price"] for s in (irr_solve, dscr_solve) if s["status"] == "SOLVED"]
    walk_away = min(solved) if solved else None
    dscr_value = result["min_dscr"]
    irr_ok = result["irr"] >= target / 100
    tile(t[1], T("t_return"), f"{result['irr']:.2%}", T("c_goal", x=f"{target:.2f}"))
    tile(t[2], T("t_dscr"), f"{dscr_value:.3f}x", T("c_bank", m=f"{dscr_min:.2f}"))
    tile(t[3], T("t_coc"), f"{result['cash_on_cash']:.2%}", T("c_coc"))
elif model == "BRRR":
    irr_solve = max_price_irr(deal)
    aco = max_price_all_cash_out(deal)
    walk_away = irr_solve["price"] if irr_solve["status"] == "SOLVED" else None
    dscr_value = result["dscr"]
    if result["all_cash_out"]:
        tile(t[1], T("t_return"), T("all_cash_out"), T("c_no_cash_left"))
        irr_ok = True
    else:
        tile(t[1], T("t_return"), f"{result['irr']:.2%}", T("c_goal", x=f"{target:.2f}"))
        irr_ok = result["irr"] >= target / 100
    tile(t[2], T("t_dscr"), f"{dscr_value:.3f}x", T("c_bank", m=f"{dscr_min:.2f}"))
    if result["cash_left"] < 0:
        tile(t[3], T("t_cash_left"), "$0", T("c_refi_more", x=money(-result["cash_left"])))
    else:
        back = result["cash_invested"] - result["cash_left"]
        tile(t[3], T("t_cash_left"), money(result["cash_left"]),
             T("c_of_invested", x=money(result["cash_invested"]), y=money(back)))
else:
    walk_away = result["max_offer_mao"]
    tile(t[1], T("t_return"), f"{result['annualized_roi']:.2%}", T("c_flip_months", n=hold))
    tile(t[2], T("t_margin"), f"{result['profit_margin']:.2%}", T("c_goal", x=f"{target:.2f}"))
    tile(t[3], T("t_net_profit"), money(result["net_profit"]),
         T("c_holding", x=money(result["monthly_holding"])))

if walk_away:
    cap = T("c_vs_asking", x=money(price))
    if model == "Rental":
        bank_limit = dscr_solve["status"] == "SOLVED" and walk_away == dscr_solve["price"]
        cap = T("c_bank_sets" if bank_limit else "c_goal_sets", x=money(price))
    if model == "BRRR" and dscr_value < dscr_min:
        cap = T("c_price_cant_fix")
    tile(t[4], T("t_max_pay"), money(walk_away), cap)
elif model == "BRRR" and result["all_cash_out"]:
    tile(t[4], T("t_max_pay"), T("na"), T("c_all_back"))
else:
    tile(t[4], T("t_max_pay"), T("none"), T("c_no_price"))

if model in ("Rental", "BRRR") and not result.get("all_cash_out"):
    with t[1].popover(T("what_mean")):
        st.markdown(T("p_return", irr=f"{result['irr']:.2%}", real=f"{result['real_irr']:.2%}",
                      infl=f"{result['inflation']:.1%}", years=exit_year,
                      profit=money(result["total_profit"]),
                      real_profit=money(result["real_total_profit"])).replace("$", "\\$"))

if model in ("Rental", "BRRR"):
    when = T("when_rental") if model == "Rental" else T("when_brrr")
    with t[2].popover(T("what_mean")):
        st.markdown(T("p_dscr", x=f"{dscr_value:.3f}", when=when, m=f"{dscr_min:.2f}",
                      rent=money(rent), pitia=money(result["pitia"]),
                      pi=money(result["pi_monthly"]), tax=money(result["tax_monthly"]),
                      ins=money(result["insurance_monthly"]),
                      hoa=money(result["hoa_monthly"])).replace("$", "\\$"))

if model == "Rental":
    with t[3].popover(T("what_mean")):
        coc = result["cash_on_cash"]
        amt = money(abs(result["cash_flow_table"][0]["cash_flow"]))
        if coc >= 0:
                st.markdown(T("p_coc_pos", x=f"{coc:.2%}", amt=amt).replace("$", "\\$"))
        else:
                st.markdown(T("p_coc_neg", x=f"{-coc:.2%}", amt=amt).replace("$", "\\$"))

if walk_away:
    if model == "Rental":
        pm_key = "pm_bank" if bank_limit else "pm_goal"
    elif model == "BRRR":
        pm_key = "pm_goal"
    else:
        pm_key = "pm_flip"
    with t[4].popover(T("what_mean")):
        st.markdown(T(pm_key, price=money(walk_away), asking=money(price),
                      goal=f"{target:.2f}", m=f"{dscr_min:.2f}").replace("$", "\\$"))

if model in ("Rental", "BRRR") and result.get("points_cost", 0) > 0:
    be = int(-(-result["breakeven_months"] // 1))   # round up
    hold_months = exit_year * 12 - (refi_month if model == "BRRR" else 0)
    typed_rate = deal["annual_rate"] if model == "Rental" else deal["post_refi_rate"]
    text = T("p_points", cost=money(result["points_cost"]),
             frm=f"{round(typed_rate * 100, 3):g}",
             to=f"{round(result['rate_used'] * 100, 3):g}",
             save=money(result["monthly_saving"]), be=be,
             hold=hold_months).replace("$", "\\$")
    if be <= hold_months:
        st.success(text + T("p_worth"))
    else:
        st.warning(text + T("p_not_worth"))


# Tabs
inv, lend, sens, cf = st.tabs(
    [T("tab_inv"), T("tab_lend"), T("tab_sens"), T("tab_cf")])

with inv:
    a, b = st.columns(2)
    with a:
        st.markdown("#### " + T("why"))
        if model == "Flip":
            margin = result["profit_margin"]
            check(T("k_profit", x=money(result["net_profit"])), result["net_profit"] > 0)
            check(T("k_min_profit", x=f"{margin:.2%}"), margin >= 0.10)
            check(T("k_profit_goal", x=f"{margin:.2%}", goal=f"{target:.2f}"),
                  margin >= target / 100)
        else:
            check(T("k_bank", x=f"{dscr_value:.3f}", m=f"{dscr_min:.2f}"),
                  dscr_value >= dscr_min)
            if model == "BRRR" and result["all_cash_out"]:
                check(T("k_return_aco"), True)
            else:
                check(T("k_return", x=f"{result['irr']:.2%}", goal=f"{target:.2f}"), irr_ok)
            res = result["dscr_with_reserves"]
            msg = T("k_repairs", x=f"{res:.2f}")
            if res >= 1.0:
                st.info(msg)
            else:
                st.warning(msg + T("k_repairs_low"))

    with b:
        st.markdown("#### " + T("fix"))
        if model == "Flip":
            over = result["over_under_mao"]
            mao = money(result["max_offer_mao"])
            if over > 0:
                line = T("f_mao_below", mao=mao, x=money(over))
            else:
                line = T("f_mao_under", mao=mao, x=money(-over))
            st.write(line.replace("$", "\\$"))
        else:
            st.write(T("f_rent_bank", x=money2(result["required_rent_lender"])))
            st.write(T("f_rent_repairs", x=money2(result["required_rent"])))
            if irr_solve["status"] == "SOLVED":
                st.write(T("f_max_goal", goal=f"{target:.2f}", x=money(irr_solve["price"])))
            if model == "Rental" and dscr_solve["status"] == "SOLVED":
                st.write(T("f_max_bank", x=money(dscr_solve["price"])))
            if model == "BRRR" and aco["status"] == "SOLVED":
                st.write(T("f_aco", x=money(aco["price"])))

with lend:
    if model == "Rental":
        approval = approval_likelihood("Rental", result["min_dscr"], result["ltv"],
                                       dscr_min=dscr_min)
        l = st.columns(5)
        tile(l[0], T("l_loan"), money(result["loan_amount"]),
             T("c_of_price", x=f"{result['ltv']:.0%}"))
        tile(l[1], T("l_noi"), money(result["noi_y1"]), T("c_noi"))
        tile(l[2], T("l_debt"), money(result["annual_debt_service"]),
             T("c_fixed", x=f"{round(result['rate_used'] * 100, 3):g}"))
        tile(l[3], T("t_dscr"), f"{result['min_dscr']:.3f}x",
             T("c_bank_strong", rent=money(rent), pitia=money(result["pitia"]),
               m=f"{dscr_min:.2f}"))
        note = T("note_rental", d=f"{result['min_dscr']:.3f}", ltv=f"{result['ltv']:.0%}",
                 m=f"{dscr_min:.2f}", s=f"{max(DSCR_STRONG, dscr_min):.2f}")
        cap_rate = result["noi_y1"] / price
        tile(l[4], T("l_cap"), f"{cap_rate:.2%}", T("c_cap"))
        with l[4].popover(T("what_mean")):
            st.markdown(T("p_cap", x=f"{cap_rate:.2%}", noi=money(result["noi_y1"]),
                          price=money(price)).replace("$", "\\$"))
    elif model == "BRRR":
        refi = result["refi_ltv_effective"]
        approval = approval_likelihood("BRRR", result["dscr"], refi, dscr_min=dscr_min)
        l = st.columns(4)
        tile(l[0], T("l_new_loan"), money(result["refi_loan"]), T("c_on_arv", x=money(arv)))
        tile(l[1], T("l_refi_ltv"), f"{refi:.0%}",
            T("c_refi_at", type=T("rt_" + refi_type), m=refi_month, o=mn_ord(refi_month)))
        tile(l[2], T("l_cash_back"), money(result["cash_pulled_out"]), T("c_after_hm"))
        tile(l[3], T("t_dscr"), f"{result['dscr']:.3f}x",
             T("c_bank_strong", rent=money(rent), pitia=money(result["pitia"]),
               m=f"{dscr_min:.2f}"))
        note = T("note_brrr", d=f"{result['dscr']:.3f}", ltv=f"{refi:.0%}",
                 m=f"{dscr_min:.2f}", s=f"{max(DSCR_STRONG, dscr_min):.2f}")
    else:
        hm_ltv_arv = result["hm_loan"] / arv
        ltc = result["hm_loan"] / (price + rehab)
        approval = approval_likelihood("Flip", hm_ltv_on_arv=hm_ltv_arv)
        l = st.columns(4)
        tile(l[0], T("l_hm_loan"), money(result["hm_loan"]), T("c_pct_price", x=f"{hm_ltv:.0f}"))
        tile(l[1], T("l_ltv_arv"), f"{hm_ltv_arv:.2%}", T("c_cap75"))
        tile(l[2], T("l_ltc"), f"{ltc:.2%}", T("c_ltc"))
        tile(l[3], T("l_time"), T("v_months", n=hold), T("c_buy_sell"))
        if approval == "LIKELY":
            note = T("note_flip_ok", x=f"{hm_ltv_arv:.2%}")
        else:
            note = T("note_flip_bad", x=f"{hm_ltv_arv:.2%}")

    st.markdown("#### " + T("fund"))
    shown = T("a_" + approval, default=approval)
    if approval in ("STRONG", "LIKELY"):
        st.success(f"{shown}: {note}")
    elif approval == "CONDITIONAL":
        st.warning(f"{shown}: {note}")
    else:
        st.error(f"{shown}: {note}")

with sens:
    if model == "Flip":
        st.info(T("s_flip_info"))
    elif model == "BRRR":
        tor = brrr_tornado_irr(deal)
        if tor["base_all_cash_out"]:
            st.info(T("s_brrr_aco_info"))
        else:
            rows = tor["rows"]
            names = [var_name(r["variable"]) + (" *" if r["all_cash_out"] else "") for r in rows]
            base_irr = tor["base"]
            driver_note(rows, base_irr, PLAIN)
            st.plotly_chart(tornado_chart(names, rows, base_irr, 360))
            caption = T("s_cap_brrr")
            if any(r["all_cash_out"] for r in rows):
                caption += T("s_aco_star")
            st.caption(caption)
    else:
        if irr_solve["status"] == "SOLVED":
            typed = round(deal["annual_rate"] * 100, 3)
            used = round(result["rate_used"] * 100, 3)
            rate_txt = f"{typed:g}%" + (T("s_after_points", x=f"{used:g}") if used != typed else "")
            st.markdown(T("s_reach", rate=rate_txt, goal=f"{target:.2f}",
                          price=money(irr_solve["price"])).replace("$", "\\$"))
        else:
            st.markdown(T("s_no_price", goal=f"{target:.2f}"))
        g = two_way_irr(deal)
        t_irr = target / 100
        span = max(abs(v - t_irr) for row in g["irr"] for v in row) or 0.01
        fig = go.Figure(go.Heatmap(
            z=g["irr"],
            x=[money(p) for p in g["prices"]],
            y=[f"{round(r * 100, 3):g}%" for r in g["rates"]],
            colorscale=[[0, "#e34948"], [0.5, "#f0efec"], [1, "#2a78d6"]],
            zmin=t_irr - span, zmax=t_irr + span,
            texttemplate="%{z:.2%}", textfont={"color": "#172036"},
            hovertemplate=T("s_heat_hover"),
            xgap=2, ygap=2,
            colorbar={"title": T("s_return_short"), "tickformat": ".0%"},
        ))
        fig.update_layout(
            title=T("s_heat_title", goal=f"{target:.2f}"),
            xaxis={"title": T("price"), "type": "category"},
            yaxis={"title": T("s_loan_rate"), "type": "category", "autorange": "reversed"},
            height=420,
            margin={"t": 50, "l": 10, "r": 10, "b": 10},
            plot_bgcolor="#FFFFFF",
        )
        st.plotly_chart(fig)
        st.caption(T("s_heat_cap"))

        tor = tornado_irr(deal)
        tor["rows"] = [r for r in tor["rows"] if r["low"] != r["high"]]
        names = [var_name(r["variable"]) for r in tor["rows"]]
        base_irr = tor["base"]
        driver_note(tor["rows"], base_irr, PLAIN)
        st.plotly_chart(tornado_chart(names, tor["rows"], base_irr, 380))
        st.caption(T("s_cap_rental"))

with cf:
    if model == "Flip":
        items = [
            (T("cf_price"), price),
            (T("cf_repairs"), rehab),
            (T("cf_hm_interest"), result["hm_interest"]),
            (T("cf_hm_fee"), result["hm_points"]),
            (T("cf_closing"), result["closing_costs"]),
            (T("cf_holding", n=hold), result["total_holding"]),
            (T("cf_selling"), result["selling_cost"]),
            (T("cf_total"), result["total_project_cost"]),
            (T("cf_sale"), arv),
            (T("t_net_profit"), result["net_profit"]),
            (T("cf_cash_in"), result["cash_invested"]),
        ]
        table = pd.DataFrame({T("cf_amount"): [v for _, v in items]},
                             index=[k for k, _ in items])
        st.dataframe(table.style.format(money), width=420, height=422)
        st.caption(T("cf_cap_flip"))
    elif model == "BRRR":
        rows = result["cash_flow_table"]
        keys = ["noi", "debt_service", "capex_reserve", "cash_flow", "cash_out_at_refi",
                "sale_proceeds"]
        table = pd.DataFrame(
            {T("cf_year", n=r["year"], o=mn_ord(r["year"])): [r[k] for k in keys] for r in rows},
            index=[T("cf_" + k) for k in keys],
        )
        st.dataframe(table.style.format(money), width="stretch",
                     column_config={"_index": st.column_config.Column(width="large")})
        st.caption(T("cf_cap_brrr", m=refi_month, o=mn_ord(refi_month)))
    else:
        rows = result["cash_flow_table"]
        keys = ["gross_rent", "effective_income", "operating_expenses", "noi", "interest",
                "capex_reserve", "cash_flow", "principal", "sale_proceeds"]
        table = pd.DataFrame(
            {T("cf_year", n=r["year"], o=mn_ord(r["year"])): [r[k] for k in keys] for r in rows},
            index=[T("cf_" + k) for k in keys],
        )
        st.dataframe(table.style.format(money), width="stretch",
                     column_config={"_index": st.column_config.Column(width="large")})
        dscr_row = "  ·  ".join(f"{T('cf_year_short', n=r['year'], o=mn_ord(r['year']))}: {r['dscr']:.3f}x" for r in rows)
        st.caption(T("cf_dscr_by_year", x=dscr_row))
        st.caption(T("cf_cap_rental"))
st.divider()
st.caption(T("disclaimer"))