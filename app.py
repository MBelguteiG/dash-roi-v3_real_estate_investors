import streamlit as st
from engine.analyze import analyze_deal
from engine.solvers import max_price_irr, max_price_dscr, max_price_all_cash_out
from engine.verdict import approval_likelihood
import plotly.graph_objects as go
import pandas as pd
from engine.sensitivity import two_way_irr, tornado_irr, brrr_tornado_irr
from engine.assumptions import get_assumptions

from i18n import tr, LANG_NAMES




st.set_page_config(page_title="Dash ROI Pro v3", layout="wide")


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
        st.caption(caption)


def check(text, ok):
    if ok:
        st.success(text)
    else:
        st.error(text)

def driver_note(rows, base, names):
    top = next((r for r in rows if not r.get("all_cash_out")), None)
    if top is None:
        return
    name = names.get(top["variable"], top["variable"]).lower()
    lo, hi = sorted((top["low"], top["high"]))
    st.markdown(f"**Biggest driver: {name}.** Within the changes tested below, your "
                f"yearly return ranges from **{lo:.2%}** to **{hi:.2%}** (your deal: {base:.2%}).")

def tornado_chart(names, rows, base, height):
    fig = go.Figure()
    for label, pick, colour in (("Helps your return", max, "#2a78d6"),
                                ("Hurts your return", min, "#A0AEC0")):
        values, moves = [], []
        for r in rows:
            v = pick(r["low"], r["high"])
            values.append(v)
            moves.append("lower" if v == r["low"] else "higher")
        fig.add_trace(go.Bar(
            name=label, y=names, orientation="h",
            x=[v - base for v in values], base=[base] * len(values),
            marker_color=colour, customdata=list(zip(values, moves)),
            hovertemplate="If %{y} is %{customdata[1]}: yearly return "
                          "%{customdata[0]:.2%}<extra></extra>",
        ))
    fig.add_vline(x=base, line_dash="dot", line_color="#4A5568")
    fig.update_layout(
        title=f"What moves your yearly return most<br><sup>Dotted line = your deal, {base:.2%}</sup>",
        barmode="overlay", height=height,
        xaxis={"title": "Yearly return", "tickformat": ".1%"},
        yaxis={"type": "category", "autorange": "reversed"},
        legend={"orientation": "h", "y": -0.2},
        margin={"t": 50, "l": 10, "r": 10, "b": 10},
        plot_bgcolor="#FFFFFF",
    )
    return fig

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
    default_hoa = get_assumptions(state, property_type, model, scenario)["HOA Monthly"]
    h = st.columns([1, 1, 6])
    hoa_in = h[0].number_input(
        T("hoa"), value=None, min_value=0.0, step=25.0,
        placeholder=T("hoa_default", x=money(default_hoa)),
        help=T("h_hoa"), key=K("hoa"))
    if hoa_in is not None:
        deal["hoa_override"] = hoa_in
    if model in ("Rental", "BRRR"):
        buy_pts = h[1].number_input(
            T("points"), min_value=0.0, max_value=4.0,
            value=0.0, step=0.5, help=T("h_points"), key=K("points"))
        deal["points"] = buy_pts



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
    tile(t[2], T("t_dscr"), f"{dscr_value:.2f}x", T("c_bank"))
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
    tile(t[2], T("t_dscr"), f"{dscr_value:.2f}x", T("c_bank"))
    if result["cash_left"] < 0:
        tile(t[3], T("t_cash_left"), "$0", T("c_refi_more", x=money(-result["cash_left"])))
    else:
        tile(t[3], T("t_cash_left"), money(result["cash_left"]),
             T("c_of_invested", x=money(result["cash_invested"])))
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
    if model == "BRRR" and dscr_value < 1.20:
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
        st.markdown(T("p_dscr", x=f"{dscr_value:.2f}", when=when))

if model == "Rental":
    with t[3].popover(T("what_mean")):
        coc = result["cash_on_cash"]
        if coc >= 0:
            st.markdown(T("p_coc_pos", x=f"{coc:.2%}"))
        else:
            st.markdown(T("p_coc_neg", x=f"{-coc:.2%}"))

if walk_away:
    goal = (T("g_rental", x=f"{target:.2f}") if model == "Rental" else
            T("g_brrr", x=f"{target:.2f}") if model == "BRRR" else T("g_flip"))
    with t[4].popover(T("what_mean")):
        st.markdown(T("p_max", price=money(walk_away), goal=goal).replace("$", "\\$"))

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
            check(T("k_bank", x=f"{dscr_value:.2f}"), dscr_value >= 1.20)
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
        approval = approval_likelihood("Rental", result["min_dscr"], result["ltv"])
        l = st.columns(5)
        tile(l[0], "Loan amount", money(result["loan_amount"]),
             f"{result['ltv']:.0%} of the price")
        tile(l[1], "Rent left after expenses", money(result["noi_y1"]),
             "year 1, before the loan payment")
        tile(l[2], "Loan payments / yr", money(result["annual_debt_service"]),
            f"{round(result['rate_used'] * 100, 3):g}% fixed, 30 years")
        tile(l[3], "Rent covers loan", f"{result['min_dscr']:.2f}x",
             "bank wants 1.20x, 1.25x for strong")
        note = (f"Rent covers the loan {result['min_dscr']:.2f}x and the loan is "
                f"{result['ltv']:.0%} of the price. Strong needs 1.25x and 80% or less; "
                "conditional needs 1.20x.")
        cap_rate = result["noi_y1"] / price
        tile(l[4], "Cap rate", f"{cap_rate:.2%}", "rent left after expenses ÷ price")
        with l[4].popover("What does this mean?"):
            st.markdown((
                f"If you paid **all cash** with no loan, you'd earn **{cap_rate:.2%}** a year "
                f"from rent: {money(result['noi_y1'])} left after expenses ÷ "
                f"{money(price)} price.\n\n"
                "It ignores the loan, so you can compare properties side by side. "
                "Compare it with similar rentals in the same area: higher means more "
                "income for the price.").replace("$", "\\$"))
    elif model == "BRRR":
        refi = result["refi_ltv_effective"]
        approval = approval_likelihood("BRRR", result["dscr"], refi)
        l = st.columns(4)
        tile(l[0], "New loan", money(result["refi_loan"]),
             f"on a value after repairs of {money(arv)}")
        tile(l[1], "New loan % of value", f"{refi:.0%}",
             f"{refi_type}, refinance at month {refi_month}")
        tile(l[2], "Cash back at refinance", money(result["cash_pulled_out"]),
             "after paying off the short-term loan")
        tile(l[3], "Rent covers loan", f"{result['dscr']:.2f}x",
             "bank wants 1.20x, 1.25x for strong")
        note = (f"After the refinance, rent covers the loan {result['dscr']:.2f}x and the "
                f"new loan is {refi:.0%} of the value. Strong needs 1.25x and 80% or less; "
                "conditional needs 1.20x.")
    else:
        hm_ltv_arv = result["hm_loan"] / arv
        ltc = result["hm_loan"] / (price + rehab)
        approval = approval_likelihood("Flip", hm_ltv_on_arv=hm_ltv_arv)
        l = st.columns(4)
        tile(l[0], "Short-term loan", money(result["hm_loan"]),
             f"{hm_ltv:.0f}% of the price")
        tile(l[1], "Loan % of sale price", f"{hm_ltv_arv:.2%}",
             "lenders cap this at 75%")
        tile(l[2], "Loan % of total cost", f"{ltc:.2%}",
             "loan ÷ (price + repairs)")
        tile(l[3], "Time to sell", f"{hold} months", "from buying to selling")
        if approval == "LIKELY":
            note = (f"The loan is {hm_ltv_arv:.2%} of the sale price, under the 75% cap. "
                    "A short-term lender is likely to fund.")
        else:
            note = (f"The loan is {hm_ltv_arv:.2%} of the sale price, over the 75% cap. "
                    "Expect the lender to lower the loan or say no.")

    st.markdown("#### Will a lender fund it?")
    if approval in ("STRONG", "LIKELY"):
        st.success(f"{approval}: {note}")
    elif approval == "CONDITIONAL":
        st.warning(f"{approval}: {note}")
    else:
        st.error(f"{approval}: {note}")

with sens:
    plain = {"ARV": "Value after repairs", "Rehab": "Repair budget",
             "Refi LTV": "New loan % of value", "Post-refi rate": "New loan rate",
             "Rate": "Loan rate", "Interest rate": "Loan rate",
             "Vacancy": "Empty months", "Rent growth": "Rent increases",
             "Appreciation": "Home value growth",
             "Vacancy rate": "Empty months", "Rehab cost": "Repair budget"}
    
    if model == "Flip":
        st.info("These charts are for rentals. A flip is judged on its profit, so check "
                "the profit tests and Most you should offer in the Investor view.")
    elif model == "BRRR":
        tor = brrr_tornado_irr(deal)
        if tor["base_all_cash_out"]:
            st.info("This deal gives back all the cash you put in at the refinance, so there's "
                    "no yearly return to compare. Lower the value after repairs or the new "
                    "loan % to see this chart.")
        else:
            rows = tor["rows"]
            names = [plain.get(r["variable"], r["variable"]) + (" *" if r["all_cash_out"] else "")
                     for r in rows]
            base_irr = tor["base"]
            driver_note(rows, base_irr, plain)
            st.plotly_chart(tornado_chart(names, rows, base_irr, 360))    
            caption = ("Blue bars help your return, grey bars hurt it. Each bar changes one input up or down, "
                       "with everything else the same. Changes tested: value after repairs, "
                       "rent and price ±10%; repairs ±25%; new loan % ±5%; new loan rate ±1%.")
            if any(r["all_cash_out"] for r in rows):
                caption += (" * At that change you'd get all your cash back at the refinance, "
                            "so that bar isn't comparable.")
            st.caption(caption)
    else:
        if irr_solve["status"] == "SOLVED":
            typed = round(deal["annual_rate"] * 100, 3)
            used = round(result["rate_used"] * 100, 3)
            rate_txt = f"{typed:g}%" + (f" ({used:g}% after points)" if used != typed else "")
            st.markdown((f"**At your {rate_txt} rate, you reach your {target:.2f}% goal "
                         f"if you pay {money(irr_solve['price'])} or less.**").replace("$", "\\$"))
        else:
            st.markdown(f"**No price in this range reaches your {target:.2f}% goal at this rate.**")
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
            hovertemplate="Loan rate %{y}<br>Price %{x}<br>Yearly return %{z:.2%}<extra></extra>",
            xgap=2, ygap=2,
            colorbar={"title": "Return", "tickformat": ".0%"},
        ))
        fig.update_layout(
            title=f"Yearly return by price and loan rate (grey = your {target:.2f}% goal)",
            xaxis={"title": "Price", "type": "category"},
            yaxis={"title": "Loan rate", "type": "category", "autorange": "reversed"},
            height=420,
            margin={"t": 50, "l": 10, "r": 10, "b": 10},
            plot_bgcolor="#FFFFFF",
        )
        st.plotly_chart(fig)
        st.caption("How to read this: each cell is your yearly return if you paid that price "
                   "(across) at that loan rate (down). Blue beats your goal, red misses it. "
                   "The middle cell is your deal as entered.")

        tor = tornado_irr(deal)
        tor["rows"] = [r for r in tor["rows"] if r["low"] != r["high"]]
        names = [plain.get(r["variable"], r["variable"]) for r in tor["rows"]]
        base_irr = tor["base"]
        driver_note(tor["rows"], base_irr, plain)
        st.plotly_chart(tornado_chart(names, tor["rows"], base_irr, 380))
        st.caption("Blue bars help your return, grey bars hurt it. Each bar changes one input up "
                   "or down, with everything else the same. Changes tested: price and rent ±10%; "
                   "loan rate and rent increases ±1%; empty months ±3%; home value growth ±1.5%.")
        
with cf:
    if model == "Flip":
        items = [
            ("Purchase price", price),
            ("Repairs", rehab),
            ("Short-term loan interest", result["hm_interest"]),
            ("Short-term lender fee", result["hm_points"]),
            ("Buying closing costs", result["closing_costs"]),
            (f"Holding costs ({hold} months)", result["total_holding"]),
            ("Selling costs", result["selling_cost"]),
            ("Total cost", result["total_project_cost"]),
            ("Sale price", arv),
            ("Net profit", result["net_profit"]),
            ("Cash you put in", result["cash_invested"]),
        ]
        table = pd.DataFrame({"Amount": [v for _, v in items]},
                             index=[k for k, _ in items])
        st.dataframe(table.style.format(money), width=420, height=422)
        st.caption("A flip is one buy and one sale, so this is a cost list rather than a "
                   "yearly table. Net profit = sale price minus total cost.")
    elif model == "BRRR":
        rows = result["cash_flow_table"]
        labels = {
            "noi": "Rent left after expenses",
            "debt_service": "Loan payments",
            "capex_reserve": "Saved for big repairs",
            "cash_flow": "Cash flow",
            "cash_out_at_refi": "Cash back at refinance",
            "sale_proceeds": "Cash from sale",
        }
        table = pd.DataFrame(
            {f"Year {r['year']}": [r[k] for k in labels] for r in rows},
            index=list(labels.values()),
        )
        st.dataframe(table.style.format(money), width="stretch")
        st.caption(f"Months 1 to {refi_month}: you pay only interest on the short-term loan. "
                   "After that, the new 30-year loan's payments start. Cash flow is rent left "
                   "after expenses, minus loan payments and money saved for big repairs.")
    else:
        rows = result["cash_flow_table"]
        labels = {
            "gross_rent": "Rent charged",
            "effective_income": "Rent after empty months",
            "operating_expenses": "Running costs",
            "noi": "Rent left after expenses",
            "interest": "Loan interest",
            "capex_reserve": "Saved for big repairs",
            "cash_flow": "Cash flow",
            "principal": "Loan paid down (yours at sale)",
            "sale_proceeds": "Cash from sale",
        }
        table = pd.DataFrame(
            {f"Year {r['year']}": [r[k] for k in labels] for r in rows},
            index=list(labels.values()),
        )
        st.dataframe(table.style.format(money), width="stretch")
        dscr_row = "  ·  ".join(f"Y{r['year']}: {r['dscr']:.2f}x" for r in rows)
        st.caption(f"Rent covers loan, by year: {dscr_row}")
        st.caption("Cash flow is rent left after expenses, minus loan interest and money "
                   "saved for big repairs. The loan you pay down is shown separately, "
                   "because you get it back when you sell.")
st.divider()
st.caption("For education and deal screening only. Not financial, lending, tax or "
           "investment advice. Check every number with your own lender and advisors.")