"""
Estimated APR, for comparison only.

Follows the actuarial idea of Reg Z (12 CFR 1026.22 and Appendix J): the APR
is the yearly rate at which the monthly payments, discounted back, equal the
"amount financed" = loan minus prepaid finance charges.

Prepaid finance charges here = discount points + lender fees (origination,
underwriting, processing) - 12 CFR 1026.4(b)(3). Title, appraisal, recording
and other real-estate fees are left out - 12 CFR 1026.4(c)(7).

DSCR / investment-property loans are business-purpose credit and are not
covered by TILA disclosure rules, so this number is an estimate for comparing
offers, not a disclosed APR.
"""
from engine.amortization import monthly_payment


def estimated_apr(loan, note_rate, prepaid, term_months=360):
    """Yearly APR (12 x monthly rate) for a fixed-rate, fully amortizing loan."""
    if loan <= 0:
        raise ValueError("Loan must be more than 0.")
    if prepaid < 0:
        raise ValueError("Points and fees can't be negative.")
    financed = loan - prepaid
    if financed <= 0:
        raise ValueError("Points and fees can't be as large as the loan.")
    pay = monthly_payment(loan, note_rate, term_months)

    def pv(r):
        if r == 0:
            return pay * term_months
        return pay * (1 - (1 + r) ** -term_months) / r

    lo, hi = 0.0, 1.0            # monthly rate bounds (0% to 1200% a year)
    for _ in range(200):         # bisection: pv falls as the rate rises
        mid = (lo + hi) / 2
        if pv(mid) > financed:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2 * 12
