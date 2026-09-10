"""
Multi-year rental projection for Dash ROI v3.
Extends the validated Year-1 engine (rental.py) across the hold period.

Growth conventions (v3 decisions, some deliberately upgraded from Pro v2):
  - Rent:        own rent-growth rate, compounding
  - Property tax: own tax-growth rate, compounding
  - Insurance:   inflation, compounding
  - HOA:         inflation, compounding   [UPGRADED from v2 flat-HOA]
  - Maintenance: inflation, compounding   [UPGRADED from v2 %-of-rent]
  - Vacancy:     % of current rent (scales with rent)
  - Management:  % of current rent (scales with rent) -- mirrors PM contract

Year 1 matches Pro v2 to the penny. Years 2+ diverge on HOA and
maintenance BY DESIGN, per documented upgrade decisions.
"""

from engine.rental import total_receipts, total_disbursements


def project_year(year, base_rent, vacancy_rate, base_annual_tax,
                 base_annual_insurance, base_hoa, base_maint, mgmt_rate,
                 rent_growth, tax_growth, inflation):
    """
    Compute one year's NOI. year=1 is the base (no growth applied).
    Returns a dict of the grown line items plus NOI, all MONTHLY
    except noi_annual.
    """
    n = year - 1  # growth exponent: 0 in year 1

    # --- grow each input to this year ---
    rent = base_rent * (1 + rent_growth) ** n
    annual_tax = base_annual_tax * (1 + tax_growth) ** n
    annual_insurance = base_annual_insurance * (1 + inflation) ** n
    hoa = base_hoa * (1 + inflation) ** n           # upgraded
    maintenance = base_maint * (1 + inflation) ** n  # upgraded

    # --- monthly figures, reusing the validated Year-1 engine ---
    receipts = total_receipts(rent, vacancy_rate)   # rent - vacancy%*rent

    expenses = {
        "property_tax": annual_tax / 12,
        "insurance": annual_insurance / 12,
        "hoa": hoa,
        "maintenance": maintenance,
        "management": rent * mgmt_rate,   # % of CURRENT rent
    }
    disbursements = total_disbursements(expenses)
    noi_monthly = receipts - disbursements

    return {
        "year": year,
        "rent": rent,
        "receipts": receipts,
        "disbursements": disbursements,
        "noi_monthly": noi_monthly,
        "noi_annual": noi_monthly * 12,
    }


def project(hold_years, base_rent, vacancy_rate, price, tax_rate,
            base_annual_insurance, base_hoa, base_maint, mgmt_rate,
            rent_growth, tax_growth, inflation):
    """Run the projection across the full hold period. Returns a list of years."""
    base_annual_tax = price * tax_rate   # tax base = price * rate, per v2
    return [
        project_year(y, base_rent, vacancy_rate, base_annual_tax,
                     base_annual_insurance, base_hoa, base_maint, mgmt_rate,
                     rent_growth, tax_growth, inflation)
        for y in range(1, hold_years + 1)
    ]


# --- Self-check against the Pro v2 reference deal ---
if __name__ == "__main__":
    years = project(
        hold_years=5,
        base_rent=2750,
        vacancy_rate=0.06,
        price=250000,
        tax_rate=0.021,
        base_annual_insurance=1900,
        base_hoa=200,
        base_maint=247.50,   # v2 Year-1 monthly maintenance dollar
        mgmt_rate=0.08,
        rent_growth=0.02,
        tax_growth=0.03,
        inflation=0.032,
    )
    print(f"{'Year':<6}{'Rent':>10}{'NOI/yr':>14}")
    for y in years:
        print(f"{y['year']:<6}{y['rent']:>10,.2f}{y['noi_annual']:>14,.2f}")
    print()
    print("Year 1 NOI should = $15,860.00 (matches v2)")