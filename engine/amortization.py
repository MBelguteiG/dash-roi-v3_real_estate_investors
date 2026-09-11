"""
Mortgage amortization engine for Dash ROI v3.
Standard fixed-rate, fully-amortizing loan (30-year default).

Feeds two downstream needs:
  - Debt service (monthly payment) -> IRR annual cash flow, DSCR
  - Remaining balance at sale month -> IRR net sale proceeds

Reference deal: $175,000 loan, 7.80% annual, 360 months.
  Expected monthly payment ~ $1,259.77 (matches Pro v2).
"""


def monthly_payment(loan, annual_rate, term_months=360):
    """Fixed monthly payment via the standard amortization formula."""
    r = annual_rate / 12
    if r == 0:                       # guard: 0% loan is just principal/term
        return loan / term_months
    factor = (1 + r) ** term_months
    return loan * (r * factor) / (factor - 1)


def schedule(loan, annual_rate, term_months=360):
    """
    Full month-by-month schedule.
    Returns a list of dicts: month, interest, principal, balance.
    """
    r = annual_rate / 12
    payment = monthly_payment(loan, annual_rate, term_months)
    balance = loan
    rows = []
    for month in range(1, term_months + 1):
        interest = balance * r
        principal = payment - interest
        balance = balance - principal
        rows.append({
            "month": month,
            "interest": interest,
            "principal": principal,
            "balance": balance,
        })
    return rows


def balance_at(loan, annual_rate, month, term_months=360):
    """Remaining balance after a given month (e.g. month 60 = end of year 5)."""
    return schedule(loan, annual_rate, term_months)[month - 1]["balance"]


def annual_debt_service(loan, annual_rate, term_months=360):
    """Total yearly mortgage payment (12 x monthly). Used by IRR and DSCR."""
    return monthly_payment(loan, annual_rate, term_months) * 12


# --- Self-check against the Pro v2 reference deal ---
if __name__ == "__main__":
    LOAN, RATE = 175000, 0.078

    pmt = monthly_payment(LOAN, RATE)
    print(f"Monthly payment: ${pmt:,.2f}   (v2 target: $1,259.77)")

    print("\nFirst 3 months (month | interest | principal | balance):")
    for row in schedule(LOAN, RATE)[:3]:
        print(f"  {row['month']:>2}  "
              f"{row['interest']:>10,.2f}  "
              f"{row['principal']:>8,.2f}  "
              f"{row['balance']:>12,.2f}")

    bal60 = balance_at(LOAN, RATE, 60)
    print(f"\nBalance at month 60 (end of Yr 5): ${bal60:,.2f}")
    print(f"Annual debt service: ${annual_debt_service(LOAN, RATE):,.2f}")