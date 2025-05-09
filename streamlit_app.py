import streamlit as st
import math

# --- App Title ---
st.title("🧾 Simple Tax Withholding Planner")
st.write("Estimate your ideal per-paycheck withholding amount to break even at tax time.")

# --- User Inputs ---
filing_status = st.selectbox("Filing Status", ["Single", "Married Filing Jointly", "Head of Household"])
state = st.selectbox("State", ["Utah"])
annual_income = st.number_input("Annual Gross Income ($)", min_value=0.0, value=60000.0, step=1000.0)
pay_frequency = st.selectbox("Pay Frequency", ["Weekly", "Bi-Weekly", "Semi-Monthly", "Monthly"])
tax_credits = st.number_input("Tax Credits ($)", min_value=0.0, value=0.0, step=100.0)
other_income = st.number_input("Other Income (Dividends, Side Jobs, etc.) ($)", min_value=0.0, value=0.0)

# --- Frequency Conversion ---
pay_periods_per_year = {
    "Weekly": 52,
    "Bi-Weekly": 26,
    "Semi-Monthly": 24,
    "Monthly": 12
}[pay_frequency]

# --- Standard Deductions for 2024 ---
standard_deductions = {
    "Single": 14600,
    "Married Filing Jointly": 29200,
    "Head of Household": 21900
}

# --- Federal Brackets (2024 single filer, simplified) ---
federal_brackets = [
    (0, 0.10),
    (11600, 0.12),
    (47150, 0.22),
    (100525, 0.24),
    (191950, 0.32),
    (243725, 0.35),
    (609350, 0.37)
]

utah_tax_rate = 0.0485

# --- Tax Calculation Functions ---
def calculate_federal_tax(taxable_income):
    tax = 0
    for i in range(len(federal_brackets)):
        lower, rate = federal_brackets[i]
        upper = federal_brackets[i+1][0] if i+1 < len(federal_brackets) else math.inf
        if taxable_income > lower:
            tax += (min(taxable_income, upper) - lower) * rate
        else:
            break
    return tax

def calculate_state_tax(taxable_income):
    return taxable_income * utah_tax_rate

# --- Taxable Income ---
deductions = standard_deductions[filing_status]
taxable_income = max(0, annual_income + other_income - deductions)

# --- Tax Estimates ---
federal_tax = calculate_federal_tax(taxable_income)
state_tax = calculate_state_tax(taxable_income)
total_tax = federal_tax + state_tax - tax_credits

withholding_per_check = total_tax / pay_periods_per_year

# --- Output ---
st.subheader("📊 Results")
st.write(f"**Estimated Federal Tax:** ${federal_tax:,.2f}")
st.write(f"**Estimated State Tax (Utah):** ${state_tax:,.2f}")
st.write(f"**Total Tax Liability:** ${total_tax:,.2f}")

st.success(f"✅ You should withhold approximately **${withholding_per_check:,.2f}** per {pay_frequency.lower()} to break even.")
