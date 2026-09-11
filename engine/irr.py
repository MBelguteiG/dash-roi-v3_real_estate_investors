"""
IRR engine for Dash ROI v3.
Computes the internal rate of return on the investor cash-flow stream:
  Year 0: -initial investment
  Years 1..N-1: annual investor cash flow
  Year N: annual cash flow + net sale proceeds

IRR is the discount rate r where sum( CF_t / (1+r)^t ) = 0.
Solved numerically (no external libraries) via bisection.
"""


def npv(rate, cashflows):
    """Net present value of a cash-flow list at a given discount rate.
    cashflows[0] is time 0 (the initial outflow, negative)."""
    return sum(cf / (1 + rate) ** t for t, cf in enumerate(cashflows))


def irr(cashflows, low=-0.9999, high=10.0, tol=1e-9, max_iter=200):
    """
    Internal rate of return via bisection.
    Returns the rate where NPV crosses zero. Assumes one sign change
    (standard for -outflow then +inflows), which holds for these deals.
    """
    f_low = npv(low, cashflows)
    f_high = npv(high, cashflows)
    if f_low * f_high > 0:
        raise ValueError("IRR not bracketed - check the cash-flow signs.")

    for _ in range(max_iter):
        mid = (low + high) / 2
        f_mid = npv(mid, cashflows)
        if abs(f_mid) < tol:
            return mid
        if f_low * f_mid < 0:
            high = mid
        else:
            low, f_low = mid, f_mid
    return (low + high) / 2


# --- Validation against v2's Return Analysis IRR stream ---
if __name__ == "__main__":
    # Exact stream from v2 Return Analysis (rows 46-51), exit at Year 5.
    # Year 5 = 1,498.53 operating cash flow + 82,896.98 net sale proceeds.
    stream = [
        -112375.00,   # Year 0: total cash invested
        -46.39,       # Year 1: cash flow after CapEx
        366.47,       # Year 2
        699.45,       # Year 3
        1091.92,      # Year 4
        84395.51,     # Year 5: operating + net sale proceeds
    ]
    result = irr(stream)
    print(f"IRR: {result * 100:.2f}%")
    print("v2 target: -5.14%")