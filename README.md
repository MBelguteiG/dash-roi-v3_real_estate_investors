# Dash ROI Pro v3

A web app for screening residential real estate deals as a **Rental**, **BRRR**
(buy, rehab, rent, refinance, repeat) or **Flip**. It is a Python and Streamlit
rebuild of Dash ROI Pro v2, an Excel/VBA analysis tool.

Each deal gets a verdict, the numbers behind it, a lender's view, and the
highest price that still meets the investor's target.

## Features

- **Three models, one page.** Switch between Rental, BRRR and Flip, and between
  Conservative, Base and Aggressive scenarios. State and property-type
  assumptions (tax, insurance, HOA, vacancy, growth rates) come from an
  assumption table for California and Illinois.
- **Verdicts with reasons.** DSCR is a hard gate for Rental and BRRR; Flip is
  judged on profit margin against a 10% floor and the user's target.
- **Walk-away price.** Solvers find the maximum price that meets the target IRR
  or a 1.20 DSCR (Rental), the IRR target (BRRR), or the max allowable offer (Flip).
- **Lender view.** Loan sizing, NOI, debt service, DSCR and a fundability rating
  for each model.
- **Sensitivity (Rental).** A 2-way IRR heatmap by price and interest rate, and a
  tornado chart of seven key variables.

## Run it

```
pip install -r requirements.txt
python -m streamlit run app.py
```

## Tests

```
python -m pytest -q
```

198 tests cover the engines, the solvers, the lender rules, the sensitivity
functions, and regression cases carried over from the v2 test plan
(Rental R-01 to R-06, BRRR B-01 to B-08, Flip F-01 to F-03).

## Project structure

```
engine/        calculation engines (no UI code)
  analyze.py     analyze_deal(): single entry point, routes by model
  rental.py, brrr.py, flip.py, irr.py, amortization.py, projection.py
  solvers.py     max-price solvers
  verdict.py     verdicts and lender fundability
  sensitivity.py 2-way grid and tornado
  assumptions.py assumption-table lookup
tests/         pytest suite
app.py         Streamlit page
Assumption.csv scenario assumptions by state, property type and model
```

## Design decisions

The v3 engines were checked line by line against v2. Where v3 differs, the
change is deliberate and recorded:

- HOA and maintenance escalate with inflation; CapEx is linked to rent every year.
- BRRR required rent uses the refi loan, not the purchase loan.
- BRRR all-cash-out price uses the exact formula
  (ARV × refi LTV − rehab) ÷ (1 + closing %).
- BRRR lender fundability uses the refi LTV.
- The IRR solver works on long monthly streams (fixes a v2-era crash on BRRR
  holds of 7+ years).