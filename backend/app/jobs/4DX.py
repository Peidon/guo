# Financial inputs for 4DMedical Ltd (ASX: 4DX) valuation simulation based on the AIRCARE for Vets pilot program
# and broader US reimbursement scaling.

# Existing Capital Structure as of Aug 2026
shares_outstanding = 599672265
current_share_price = 3.64
market_cap = shares_outstanding * current_share_price
net_cash = 278000000
enterprise_value = market_cap - net_cash

# Baseline financial performance (Pre-pilot, trailing trend)
base_revenue_fy26 = 7200000
base_operating_cash_burn = -37000000
saas_gross_margin = 0.92

# Scenario Modeling: Impact of the US$20M AIRCARE for Vets Pilot Program over a 3-year rollout
# Converting US$20M to AUD (approximate FX rate of 0.65 AUD/USD -> 1 USD = 1.54 AUD)
usd_to_aud = 1.54
pilot_funding_usd = 20000000
pilot_funding_aud = pilot_funding_usd * usd_to_aud

# Annualized incremental pilot revenue assuming straight-line 3-year execution
annual_pilot_revenue_aud = pilot_funding_aud / 3
annual_pilot_gross_profit = annual_pilot_revenue_aud * saas_gross_margin

# We will model three 5-year DCF/Revenue growth paths from FY2027 to FY2031 to calculate implicit intrinsic value.
# Discount rate (WACC) is set high at 11.5% reflecting early-stage biotech/medtech risk.
wacc = 0.115
terminal_growth_rate = 0.035


def calculate_dcf(growth_rate_base, includes_pilot=True):
    # assuming baseline per scan price $650, 344000 scan per year
    revenue = base_revenue_fy26
    yearly_fcf = base_operating_cash_burn
    discounted_fcf_sum = 0

    # Yearly projection loop
    for year in range(1, 6):
        # Base business growth
        revenue = revenue * (1 + growth_rate_base)

        # Add pilot impact if active
        yearly_rev = revenue
        if includes_pilot and year <= 3:
            yearly_rev += annual_pilot_revenue_aud

        # Operating leverage calculation: as revenue scales, operating loss shrinks
        # Assuming fixed cost base increases at 5% annually, but software margin covers variable costs
        fixed_costs = 44200000 * (1.05 ** year)
        yearly_fcf = (yearly_rev * saas_gross_margin) - fixed_costs

        # Present value calculation
        discount_factor = (1 + wacc) ** year
        discounted_fcf_sum += yearly_fcf / discount_factor

    # Terminal Value calculation
    terminal_value = (yearly_fcf * (1 + terminal_growth_rate)) / (wacc - terminal_growth_rate)
    discounted_tv = terminal_value / ((1 + wacc) ** 5)

    # Intrinsic Enterprise Value
    intrinsic_ev = discounted_fcf_sum + discounted_tv
    intrinsic_equity_value = intrinsic_ev + net_cash
    intrinsic_share_price = intrinsic_equity_value / shares_outstanding
    return max(0.10, intrinsic_share_price), yearly_fcf


if __name__ == '__main__':
    # Run Scenarios
    # quanter 10% increase, 46% per year
    # quanter 20%, 107% per year
    # what market share will it have ?
    # price_pessimistic, final_fcf_pess = calculate_dcf(0.15, includes_pilot=False)  # Slow US adoption, pilot stalls
    price_base, final_fcf_base = calculate_dcf(0.46, includes_pilot=False)  # Steady US commercialization + pilot approved
    price_optimistic, final_fcf_opt = calculate_dcf(1.07,
                                                    includes_pilot=False)  # Explosive outpatient scaling + pilot approved

    # print(f"Pessimistic Share Price: AU${price_pessimistic:.2f} (Final FCF: AU${final_fcf_pess / 1e6:.1f}M)")
    print(f"Base Share Price: AU${price_base:.2f} (Final FCF: AU${final_fcf_base / 1e6:.1f}M)")
    print(f"Optimistic Share Price: AU${price_optimistic:.2f} (Final FCF: AU${final_fcf_opt / 1e6:.1f}M)")
    # print(f"Current Enterprise Value: AU${enterprise_value / 1e6:.1f}M")
    # print(f"Pilot total AUD funding: AU${pilot_funding_aud / 1e6:.1f}M")
