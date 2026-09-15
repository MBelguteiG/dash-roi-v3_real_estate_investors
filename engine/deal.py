"""
Deal assembly for Dash ROI v3.
Builds the full IRR cash-flow stream by orchestrating the validated engines:
  rental/projection (NOI), amortization (debt service + sale-month balance),
  and the assumption lookup (rates).

Cash-flow stream (exit at year N):
  Year 0:  -(down payment + rehab + closing cost)
  Years 1..N-1:  NOI(year) - annual debt service - annual CapEx reserve
  Year N:  that + net sale proceeds
Net sale = price*(1+appr)^(N-1) * (1-selling%) - loan balance at month N*12.

Validation: reference deal must reproduce v2's Year-1..5 stream and -5.14% IRR.
"""

from engine.projection import project
from engine.amortization import annual_interest, balance_at
from engine.irr import irr


def initial_investment(price, down_pct, rehab, closing_pct):
    """Year-0 cash out (v2 Return Analysis B9 = down + rehab + closing)."""
    down = price * down_pct
    closing = price * closing_pct
    return down + rehab + closing


def net_sale_proceeds(price, appreciation, selling_pct, loan_balance, exit_year):
    """
    v2 convention: Year 1 = base price, appreciation compounds from Year 2,
    so exit-year value uses (1+appr)^(exit_year-1).
    Net = sale price - selling costs - remaining loan.
    """
    sale_price = price * (1 + appreciation) ** (exit_year - 1)
    selling_cost = sale_price * selling_pct
    return sale_price - selling_cost - loan_balance


def build_stream(price, down_pct, rehab, closing_pct, annual_rate, exit_year,
                 base_rent, vacancy_rate, tax_rate, base_annual_insurance,
                 base_hoa, base_maint, mgmt_rate, annual_capex,
                 rent_growth, tax_growth, inflation, appreciation):
    """Assemble the Year 0..N investor cash-flow stream for IRR."""
    loan = price - price * down_pct

    # Year 0: initial investment (negative outflow)
    stream = [-initial_investment(price, down_pct, rehab, closing_pct)]

    # Years 1..N: investor cash flow = NOI - INTEREST (not full payment) - CapEx.
    # v2 subtracts interest only; principal paydown is equity, recaptured at sale.
    years = project(exit_year, base_rent, vacancy_rate, price, tax_rate,
                    base_annual_insurance, base_hoa, base_maint, mgmt_rate,
                    rent_growth, tax_growth, inflation)
    for y in years:
        interest = annual_interest(loan, annual_rate, y["year"])
        cf = y["noi_annual"] - interest - annual_capex
        stream.append(cf)

    # Final year: add net sale proceeds
    balance = balance_at(loan, annual_rate, exit_year * 12)
    net_sale = net_sale_proceeds(price, appreciation, 0.08, balance, exit_year)
    stream[-1] += net_sale

    return stream
def cash_on_cash(stream):
    """
    Year-1 cash-on-cash = Year-1 cash flow / initial cash invested.
    Matches v2: Cash Flow Projection!N21 (Yr-1 after-CapEx) / Return Analysis!B9.
    stream[0] is Year-0 outflow (negative); stream[1] is Year-1 cash flow.
    """
    initial_invested = -stream[0]
    year1_cash_flow = stream[1]
    return year1_cash_flow / initial_invested
    
# --- Validation: reproduce v2's -5.14% reference stream automatically ---
if __name__ == "__main__":
    stream = build_stream(
        price=250000, down_pct=0.30, rehab=28000, closing_pct=0.0375,
        annual_rate=0.078, exit_year=5,
        base_rent=2750, vacancy_rate=0.06, tax_rate=0.021,
        base_annual_insurance=1900, base_hoa=200, base_maint=247.50,
        mgmt_rate=0.08, annual_capex=2310,
        rent_growth=0.02, tax_growth=0.03, inflation=0.032, appreciation=0.02,
    )
    print("Assembled stream (Year 0..5):")
    for t, cf in enumerate(stream):
        print(f"  Year {t}: {cf:>14,.2f}")
    print(f"\nIRR: {irr(stream) * 100:.2f}%   (v2 target: -5.14%)")
print(f"Cash-on-cash (Yr 1): {cash_on_cash(stream) * 100:.2f}%   (v2 target: -0.04%)")

