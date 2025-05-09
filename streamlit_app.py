import streamlit as st
import math

# --- Title ---
st.title("🧾 Break-Even Tax Withholding Calculator")

# --- Filing status and state ---
filing_status = st.selectbox("Filing Status", ["Single", "Married Filing Jointly", "Head of Household"])
state = st.selectbox("State", ["Utah", "Other (coming soon)"])

# --- Income and pay ---
annual_income = st.number_input("Annual Gross Income ($)", min_value=0.0, value=60000.0, step=1000.0)
pay_frequency = st.selectbox("Pay Frequency", ["Weekly", "Bi-Weekly", "Semi-Monthly", "Monthly"])
pay_periods_remaining = st.number_input("Remaining Pay Periods This Year", min_value=1, max_value=52, value=20)

# --- Deductions ---
deduction_type = st.radio("Deduction Type", ["Standard", "Itemized"])
itemized_deductions = 0
if deduction_type == "Itemized":
    itemized_deductions = st.number_input("Total Itemized Deductions ($)", min_value=0.0, value=0.0, step=100.0)

# --- Credits and other income ---
other_income = st.number_input("Other Income (Dividends, Interest, etc.) ($)", min_value=0.0, value=0.0)
tax_credits = st.number_input("Tax Credits ($)", min_value=0.0, value=0.0)

ytd_federal_withheld = st.number_input("YTD Federal Tax Withheld ($)", min_value=0.0, value=5000.0)
ytd_state_withheld = st.number_input("YTD State Tax Withheld ($)", min_value=0.0, value=1500.0)

# --- Constants (2024 Standard Deductions) ---
standard_deductions = {
    "Single": 14600,
    "Married Filing Jointly": 29200,
    "Head of Household": 21900
}

federal_brackets = [
    (0, 0.10),
    (11600, 0.12),
    (47150, 0.22),
    (100525, 0.24)
    # Extend further as needed
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
    if state == "Utah":
        return taxable_income * utah_tax_rate
    return 0

# --- Taxable Income ---
standard_deduction = standard_deductions.get(filing_status, 0)
deductions = itemized_deductions if deduction_type == "Itemized" else standard_deduction
taxable_income = max(0, annual_income + other_income - deductions)

federal_tax = calculate_federal_tax(taxable_income)
state_tax = calculate_state_tax(taxable_income)

total_tax = federal_tax + state_tax - tax_credits
total_withheld = ytd_federal_withheld + ytd_state_withheld

# --- Recommendations ---
deficit_or_refund = total_withheld - total_tax
recommended_withholding_per_period = max(0, (total_tax - total_withheld) / pay_periods_remaining)

# --- Output ---
st.subheader("📊 Results")
st.write(f"Estimated Federal Tax: ${federal_tax:,.2f}")
st.write(f"Estimated State Tax: ${state_tax:,.2f}")
st.write(f"Total Estimated Tax Liability: ${total_tax:,.2f}")
st.write(f"Total YTD Withheld: ${total_withheld:,.2f}")

if deficit_or_refund > 0:
    st.success(f"You're on track to receive a refund of ${deficit_or_refund:,.2f}")
elif deficit_or_refund < 0:
    st.error(f"You may owe approximately ${-deficit_or_refund:,.2f} at tax time")
else:
    st.info("You're on track to break even")

st.write(f"✅ Recommended Withholding Per Pay Period (Remaining): ${recommended_withholding_per_period:,.2f}")
