"""
Rental cash-flow engine for Dash ROI v3.
Ports the Year-1 operating math from Pro v2's Cash Flow Projection sheet.
All figures are MONTHLY unless a function name says otherwise.
Validation target: annual NOI = $15,860.00 on the reference deal.
"""


def vacancy_loss(rent, vacancy_rate):
    """Vacancy is a % of GROSS rent (v2 row 5 = rent * rate)."""
    return rent * vacancy_rate


def total_receipts(rent, vacancy_rate):
    """Collected rent after vacancy (v2 row 6 = row 4 - row 5)."""
    return rent - vacancy_loss(rent, vacancy_rate)


def operating_expenses(rent, annual_tax, annual_insurance, hoa,
                       maint_rate, mgmt_rate):
    """
    The 5 monthly disbursements (v2 rows 9-13), returned itemized.
    Tax and insurance are annual inputs divided to monthly.
    Maintenance and management are % of GROSS rent (v2 uses B4, not row 6).
    """
    return {
        "property_tax": annual_tax / 12,
        "insurance": annual_insurance / 12,
        "hoa": hoa,
        "maintenance": rent * maint_rate,
        "management": rent * mgmt_rate,
    }


def total_disbursements(expenses):
    """Sum of the 5 expense lines (v2 row 14)."""
    return sum(expenses.values())


def noi_monthly(rent, vacancy_rate, annual_tax, annual_insurance, hoa,
                maint_rate, mgmt_rate):
    """Net Operating Income per month (v2 row 16 = receipts - disbursements)."""
    receipts = total_receipts(rent, vacancy_rate)
    expenses = operating_expenses(rent, annual_tax, annual_insurance, hoa,
                                  maint_rate, mgmt_rate)
    return receipts - total_disbursements(expenses)


def noi_annual(rent, vacancy_rate, annual_tax, annual_insurance, hoa,
               maint_rate, mgmt_rate):
    """Annual NOI (v2 Total column, row 16)."""
    return noi_monthly(rent, vacancy_rate, annual_tax, annual_insurance, hoa,
                       maint_rate, mgmt_rate) * 12


# --- Quick self-check against the Pro v2 reference deal ---
if __name__ == "__main__":
    result = noi_annual(
        rent=2750,
        vacancy_rate=0.06,
        annual_tax=5250,
        annual_insurance=1900,
        hoa=200,
        maint_rate=0.09,
        mgmt_rate=0.08,
    )
    print(f"Annual NOI: ${result:,.2f}")
    print("Target:     $15,860.00")