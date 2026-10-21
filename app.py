import streamlit as st
from engine.analyze import analyze_deal
from engine.solvers import max_price_irr, max_price_dscr, max_price_all_cash_out
from engine.verdict import approval_likelihood
import plotly.graph_objects as go
import pandas as pd
from engine.sensitivity import two_way_irr, tornado_irr, brrr_tornado_irr
from engine.assumptions import get_assumptions


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

with st.expander("Quick start"):
    st.markdown(
        "1. **Pick a model and scenario** in the top bar: Rental, BRRR or Flip; "
        "Conservative, Base or Aggressive.\n"
        "2. **Enter the deal.** Press Enter after typing a number, or use − and +.\n"
        "3. **Read the verdict.** The tiles give the headline numbers; "
        "*Investor view* explains the verdict and what would fix it; "
        "*Lender view* shows how a lender sizes the loan and whether it is likely to fund.\n"
        "4. **Most you should pay** is the most you can pay and still meet your target "
        "(for Flip, the max allowable offer)."
    )


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
        refi_type = d[5].selectbox("Refi type", ["Cash-Out", "Rate/Term"])
        deal = dict(model="BRRR", state=state, property_type=property_type,
                    scenario=scenario, price=price, rehab=rehab,
                    base_rent=rent, exit_year=exit_year,
                    target_irr=target / 100, arv=arv, hm_ltv=hm_ltv / 100,
                    hm_rate=hm_rate / 100, refi_ltv=refi_ltv / 100,
                    refi_month=refi_month, post_refi_rate=post_rate / 100,
                    refi_type=refi_type)
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
    default_hoa = get_assumptions(state, property_type, model, scenario)["HOA Monthly"]
    h = st.columns(8)
    hoa_in = h[0].number_input(
        "HOA / mo", value=None, min_value=0.0, step=25.0,
        placeholder=f"default {money(default_hoa)}",
        help="Leave blank to use the state and property-type default.")
    if hoa_in is not None:
        deal["hoa_override"] = hoa_in
    if model == "Rental":
        buy_pts = h[1].number_input(
            "Points to lower rate", min_value=0.0, max_value=4.0,
            value=0.0, step=0.5,
            help="Each point costs 1% of the loan and lowers your rate by about 0.25%.")
        deal["points"] = buy_pts

try:
    result = analyze_deal(**deal)
except (ValueError, ZeroDivisionError) as e:
    st.error(f"This deal can't be analysed: {e}. Check the inputs above.")
    st.stop()
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
    tile(t[1], "Yearly return", f"{result['irr']:.2%}", f"your goal {target:.2f}%")
    tile(t[2], "Rent covers loan", f"{dscr_value:.2f}x", "bank wants 1.20x+")
    tile(t[3], "First-year cash return", f"{result['cash_on_cash']:.2%}", "of the cash you put in")
elif model == "BRRR":
    irr_solve = max_price_irr(deal)
    aco = max_price_all_cash_out(deal)
    walk_away = irr_solve["price"] if irr_solve["status"] == "SOLVED" else None
    dscr_value = result["dscr"]
    if result["all_cash_out"]:
        tile(t[1], "Yearly return", "All cash out", "no cash left in the deal")
        irr_ok = True
    else:
        tile(t[1], "Yearly return", f"{result['irr']:.2%}", f"your goal {target:.2f}%")
        irr_ok = result["irr"] >= target / 100
        tile(t[2], "Rent covers loan", f"{dscr_value:.2f}x", "bank wants 1.20x+")
    if result["cash_left"] < 0:
        tile(t[3], "Cash left in deal", "$0",
             f"refi returns {money(-result['cash_left'])} more than invested")
    else:
        tile(t[3], "Cash left in deal", money(result["cash_left"]),
             f"of {money(result['cash_invested'])} invested")
else:
    walk_away = result["max_offer_mao"]
    tile(t[1], "Yearly return", f"{result['annualized_roi']:.2%}",
         f"{hold}-month flip, as a yearly rate")
    tile(t[2], "Profit as % of sale price", f"{result['profit_margin']:.2%}",
         f"your goal {target:.2f}%")
    tile(t[3], "Net profit", money(result["net_profit"]),
         f"holding {money(result['monthly_holding'])} / mo")

if walk_away:
    cap = f"vs {money(price)} asking"
    if model == "BRRR" and dscr_value < 1.20:
        cap = "based on your goal; price can't fix the bank test"
    tile(t[4], "Most you should pay", money(walk_away), cap)
elif model == "BRRR" and result["all_cash_out"]:
    tile(t[4], "Most you should pay", "n/a", "you get all your cash back at refi")
else:
    tile(t[4], "Most you should pay", "none", "no price meets the target")

if model in ("Rental", "BRRR") and not result.get("all_cash_out"):
    with t[1].popover("What does this mean?"):
        text = (
            f"**{result['irr']:.2%} a year** is your average yearly return "
            "on the cash you put in.\n\n"
            f"**After inflation: {result['real_irr']:.2%} a year.** Prices rise about "
            f"{result['inflation']:.1%} a year, so future dollars buy less. This is "
            "what your return is worth in today's money.\n\n"
            f"**Total profit over {exit_year} years:** {money(result['total_profit'])}, "
            f"or {money(result['real_total_profit'])} in today's dollars."
        )
        st.markdown(text.replace("$", "\\$"))

if model in ("Rental", "BRRR"):
    when = "in the worst year" if model == "Rental" else "after the refi"
    with t[2].popover("What does this mean?"):
        st.markdown(
            f"After vacancy and expenses, the rent covers your loan payment "
            f"**{dscr_value:.2f} times** {when}. Banks want at least **1.20x**, so "
            "there's a cushion if a tenant leaves or a repair comes up. Below 1.00x, "
            "you pay part of the loan from your own pocket.")

if model == "Rental":
    with t[3].popover("What does this mean?"):
        coc = result["cash_on_cash"]
        if coc >= 0:
            msg = (f"In year 1 you keep **{coc:.2%}** of the cash you put in, after the "
                   "loan, expenses and money set aside for big repairs.")
        else:
            msg = (f"In year 1 the rent doesn't cover everything: you add about "
                   f"**{-coc:.2%}** of the cash you put in, to pay the loan, expenses "
                   "and money set aside for big repairs.")
        st.markdown(msg)
if walk_away:
    goal = (f"hits your {target:.2f}% goal and passes the bank test"
            if model == "Rental" else
            f"still hits your {target:.2f}% goal" if model == "BRRR" else
            "still leaves your target profit after rehab, loan and selling costs")
    with t[4].popover("What does this mean?"):
        st.markdown((f"**{money(walk_away)}** is the highest price that {goal}. "
                     "Pay more and the numbers stop working.").replace("$", "\\$"))

if model == "Rental" and result.get("points_cost", 0) > 0:
    be = int(-(-result["breakeven_months"] // 1))   # round up
    hold_months = exit_year * 12
    text = (
        f"Paying **{money(result['points_cost'])}** lowers your rate from "
        f"{deal['annual_rate']:.2%} to **{result['rate_used']:.2%}** and saves "
        f"**{money(result['monthly_saving'])} a month**. The monthly savings pay it "
        f"back in **{be} months** (you plan to hold {hold_months})."
    ).replace("$", "\\$")
    if be <= hold_months:
        st.success(text + " Worth it.")
    else:
        st.warning(text + " The monthly savings alone won't repay it before you sell. "
                   "A lower rate also pays down more of your loan, so check your "
                   "Yearly return above to see the full effect.")


# Tabs
inv, lend, sens, cf = st.tabs(
    ["Investor view", "Lender view", "Sensitivity", "Cash flow table"])

with inv:
    a, b = st.columns(2)
    with a:
        st.markdown("#### Why this verdict")
        if model == "Flip":
            margin = result["profit_margin"]
            check(f"Profit test: {money(result['net_profit'])} after all costs",
                  result["net_profit"] > 0)
            check(f"Minimum profit test: {margin:.2%} of the sale price. Needs at least 10%.", margin >= 0.10)
            check(f"Profit goal: {margin:.2%} of the sale price. Your goal is {target:.2f}%.",
                  margin >= target / 100)
        else:
            check(f"Bank test: rent covers the loan {dscr_value:.2f}x. The bank wants 1.20x.",
                  dscr_value >= 1.20)
            if model == "BRRR" and result["all_cash_out"]:
                check("Return test: the refi gives back all the cash you put in", True)
            else:
                check(f"Return test: {result['irr']:.2%} a year. Your goal is {target:.2f}%.",
                      irr_ok)
            res = result["dscr_with_reserves"]
            msg = (f"Repairs test (yours, not the bank's): after saving for big repairs, "
                   f"rent covers the loan {res:.2f}x")
            if res >= 1.0:
                st.info(msg)
            else:
                st.warning(msg + ". Below 1.00x, you'd add your own money for big repairs.")

    with b:
        st.markdown("#### What would make it work")
        if model == "Flip":
            over = result["over_under_mao"]
            mao = money(result["max_offer_mao"])
            if over > 0:
                line = f"Most you should offer: **{mao}**, {money(over)} below the asking price"
            else:
                line = f"Most you should offer: **{mao}**. The asking price is already {money(-over)} under it"
            st.write(line.replace("$", "\\$"))
        else:
            st.write(f"Rent the bank needs to see: **{money2(result['required_rent_lender'])}**")
            st.write(f"Rent to also cover big repairs: **{money2(result['required_rent'])}**")
            if irr_solve["status"] == "SOLVED":
                st.write(f"Most you can pay to hit your {target:.2f}% goal: **{money(irr_solve['price'])}**")
            if model == "Rental" and dscr_solve["status"] == "SOLVED":
                st.write(f"Most you can pay to pass the bank test: **{money(dscr_solve['price'])}**")
            if model == "BRRR" and aco["status"] == "SOLVED":
                st.write(f"Price where the refi gives back all your cash: **{money(aco['price'])}**")

with lend:
    if model == "Rental":
        approval = approval_likelihood("Rental", result["min_dscr"], result["ltv"])
        l = st.columns(4)
        tile(l[0], "Loan amount", money(result["loan_amount"]),
             f"{result['ltv']:.0%} loan-to-value")
        tile(l[1], "NOI, year 1", money(result["noi_y1"]), "after vacancy and expenses")
        tile(l[2], "Debt service / yr", money(result["annual_debt_service"]),
             f"{rate:.3f}% fixed, 30 years")
        tile(l[3], "Rent covers loan", f"{result['min_dscr']:.2f}", "1.20 minimum, 1.25 for strong")
        note = (f"DSCR {result['min_dscr']:.2f} at {result['ltv']:.0%} LTV. Strong needs "
                "DSCR 1.25 and LTV 80% or less; conditional needs DSCR 1.20.")
    elif model == "BRRR":
        refi = result["refi_ltv_effective"]
        approval = approval_likelihood("BRRR", result["dscr"], refi)
        l = st.columns(4)
        tile(l[0], "Refi loan", money(result["refi_loan"]), f"on ARV {money(arv)}")
        tile(l[1], "Refi LTV", f"{refi:.0%}", f"{refi_type}, refi at month {refi_month}")
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
    if model == "Flip":
        st.info("Sensitivity charts don't apply to Flip deals. A flip turns on its "
                "profit margin, so check the margin verdict and the max allowable "
                "offer (MAO) in the Investor view.")
    elif model == "BRRR":
        tor = brrr_tornado_irr(deal)
        if tor["base_all_cash_out"]:
            st.info("This deal returns all the cash invested at refi, so its IRR is not "
                    "a meaningful base for a tornado. Lower the ARV or refi LTV to see one.")
        else:
            rows = tor["rows"]
            names = [r["variable"] + (" *" if r["all_cash_out"] else "") for r in rows]
            base_irr = tor["base"]
            fig3 = go.Figure()
            for label, key, colour in (("Low swing", "low", "#2a78d6"),
                                       ("High swing", "high", "#eb6834")):
                values = [r[key] for r in rows]
                fig3.add_trace(go.Bar(
                    name=label, y=names, orientation="h",
                    x=[v - base_irr for v in values], base=[base_irr] * len(values),
                    marker_color=colour, customdata=values,
                    hovertemplate="%{y}<br>" + label + ": IRR %{customdata:.2%}<extra></extra>",
                ))
            fig3.add_vline(x=base_irr, line_dash="dot", line_color="#4A5568")
            fig3.update_layout(
                title=f"BRRR: IRR impact by variable (dotted line = your deal, {base_irr:.2%})",
                barmode="overlay", height=360,
                xaxis={"title": "IRR", "tickformat": ".1%"},
                yaxis={"type": "category", "autorange": "reversed"},
                legend={"orientation": "h", "y": -0.2},
                margin={"t": 50, "l": 10, "r": 10, "b": 10},
                plot_bgcolor="#FFFFFF",
            )
            st.plotly_chart(fig3)
            caption = ("Each bar shows IRR when one input moves to its low (blue) or high "
                       "(orange) swing, all else unchanged. Swings: ARV, rent, price ±10%; "
                       "rehab ±25%; refi LTV ±5 pts; post-refi rate ±1 pt.")
            if any(r["all_cash_out"] for r in rows):
                caption += " * One swing makes the deal all-cash-out, so that bar's IRR is not comparable."
            st.caption(caption)
    else:
        g = two_way_irr(deal)
        t_irr = target / 100
        span = max(abs(v - t_irr) for row in g["irr"] for v in row) or 0.01
        fig = go.Figure(go.Heatmap(
            z=g["irr"],
            x=[money(p) for p in g["prices"]],
            y=[f"{r:.2%}" for r in g["rates"]],
            colorscale=[[0, "#e34948"], [0.5, "#f0efec"], [1, "#2a78d6"]],
            zmin=t_irr - span, zmax=t_irr + span,
            texttemplate="%{z:.2%}", textfont={"color": "#172036"},
            hovertemplate="Rate %{y}<br>Price %{x}<br>IRR %{z:.2%}<extra></extra>",
            xgap=2, ygap=2,
            colorbar={"title": "IRR", "tickformat": ".0%"},
        ))
        fig.update_layout(
            title=f"IRR by purchase price and interest rate (grey = {target:.2f}% target)",
            xaxis={"title": "Purchase price", "type": "category"},
            yaxis={"title": "Interest rate", "type": "category",
                   "autorange": "reversed"},
            height=420,
            margin={"t": 50, "l": 10, "r": 10, "b": 10},
            plot_bgcolor="#FFFFFF",
        )
        st.plotly_chart(fig)
        st.caption("Blue cells beat your target IRR, red cells miss it. "
                   "The centre cell is your deal as entered.")

        tor = tornado_irr(deal)
        names = [r["variable"] for r in tor["rows"]]
        base_irr = tor["base"]
        fig2 = go.Figure()
        for label, key, colour in (("Low swing", "low", "#2a78d6"),
                                   ("High swing", "high", "#eb6834")):
            values = [r[key] for r in tor["rows"]]
            fig2.add_trace(go.Bar(
                name=label, y=names, orientation="h",
                x=[v - base_irr for v in values], base=[base_irr] * len(values),
                marker_color=colour, customdata=values,
                hovertemplate="%{y}<br>" + label + ": IRR %{customdata:.2%}<extra></extra>",
            ))
        fig2.add_vline(x=base_irr, line_dash="dot", line_color="#4A5568")
        fig2.update_layout(
            title=f"IRR impact by variable (dotted line = your deal, {base_irr:.2%})",
            barmode="overlay", height=380,
            xaxis={"title": "IRR", "tickformat": ".1%"},
            yaxis={"type": "category", "autorange": "reversed"},
            legend={"orientation": "h", "y": -0.2},
            margin={"t": 50, "l": 10, "r": 10, "b": 10},
            plot_bgcolor="#FFFFFF",
        )
        st.plotly_chart(fig2)
        st.caption("Each bar shows IRR when one input moves to its low (blue) or "
                   "high (orange) swing, all else unchanged. Swings follow v2: price, "
                   "rent ±10%; rehab ±25%; rate, rent growth ±1 pt; vacancy ±3 pts; "
                   "appreciation ±1.5 pts.")

with cf:
    if model == "Flip":
        items = [
            ("Purchase price", price),
            ("Rehab", rehab),
            ("Hard-money interest", result["hm_interest"]),
            ("Hard-money points", result["hm_points"]),
            ("Buying closing costs", result["closing_costs"]),
            (f"Holding costs ({hold} months)", result["total_holding"]),
            ("Selling costs", result["selling_cost"]),
            ("Total project cost", result["total_project_cost"]),
            ("Sale price (ARV)", arv),
            ("Net profit", result["net_profit"]),
            ("Cash invested", result["cash_invested"]),
        ]
        table = pd.DataFrame({"Amount": [v for _, v in items]},
                             index=[k for k, _ in items])
        st.dataframe(table.style.format(money), width="content", height=422)
        st.caption("A flip is one buy and one sale, so this is a cost breakdown "
                   "rather than a yearly table. Net profit = sale price minus "
                   "total project cost.")
    elif model == "BRRR":
        rows = result["cash_flow_table"]
        labels = {
            "noi": "NOI",
            "debt_service": "Debt service",
            "capex_reserve": "CapEx reserve",
            "cash_flow": "Cash flow",
            "cash_out_at_refi": "Cash pulled out at refi",
            "sale_proceeds": "Net sale proceeds",
        }
        table = pd.DataFrame(
            {f"Year {r['year']}": [r[k] for k in labels] for r in rows},
            index=list(labels.values()),
        )
        st.dataframe(table.style.format(money), width="stretch")
        st.caption(f"Months 1 to {refi_month} pay hard-money interest only; the refi "
                   "loan's payments start after that. Cash flow follows v2: "
                   "NOI minus debt service and CapEx reserve. These are the monthly "
                   "figures behind the IRR, added up by year.")
    else:
        rows = result["cash_flow_table"]
        labels = {
            "gross_rent": "Gross rent",
            "effective_income": "Effective income (after vacancy)",
            "operating_expenses": "Operating expenses",
            "noi": "NOI",
            "interest": "Interest",
            "capex_reserve": "CapEx reserve",
            "cash_flow": "Cash flow (used in IRR)",
            "principal": "Principal paid (equity)",
            "sale_proceeds": "Net sale proceeds",
        }
        table = pd.DataFrame(
            {f"Year {r['year']}": [r[k] for k in labels] for r in rows},
            index=list(labels.values()),
        )
        st.dataframe(table.style.format(money), width="stretch")
        dscr_row = "  ·  ".join(f"Y{r['year']}: {r['dscr']:.2f}" for r in rows)
        st.caption(f"DSCR by year: {dscr_row}")
        st.caption("Cash flow follows v2: NOI minus interest and CapEx reserve. "
                   "Principal is shown separately because it builds equity, "
                   "which you get back at sale.")                 