from dataclasses import dataclass


@dataclass(frozen=True)
class CompoundInterestResult:
    initial_investment: float
    annual_interest_rate: float
    years: float
    compounds_per_year: int
    contribution_per_period: float
    total_contributions: float
    interest_earned: float
    future_value: float


class CompoundInterestCalculator:
    @staticmethod
    def calculate(
        initial_investment: float,
        annual_interest_rate: float,
        years: float,
        compounds_per_year: int,
        contribution_per_period: float,
    ) -> CompoundInterestResult:
        if initial_investment < 0:
            raise ValueError("Initial investment must be zero or greater")
        if annual_interest_rate < 0:
            raise ValueError("Interest rate must be zero or greater")
        if years <= 0:
            raise ValueError("Years must be greater than zero")
        if compounds_per_year <= 0:
            raise ValueError("Compounding frequency must be greater than zero")
        if contribution_per_period < 0:
            raise ValueError("Contribution per period must be zero or greater")

        total_periods = compounds_per_year * years
        periodic_rate = (annual_interest_rate / 100) / compounds_per_year

        if periodic_rate == 0:
            future_value = initial_investment + (contribution_per_period * total_periods)
        else:
            growth_factor = (1 + periodic_rate) ** total_periods
            future_value_principal = initial_investment * growth_factor
            future_value_contributions = contribution_per_period * (
                (growth_factor - 1) / periodic_rate
            )
            future_value = future_value_principal + future_value_contributions

        total_contributions = initial_investment + (contribution_per_period * total_periods)
        interest_earned = future_value - total_contributions

        return CompoundInterestResult(
            initial_investment=round(initial_investment, 2),
            annual_interest_rate=round(annual_interest_rate, 2),
            years=round(years, 2),
            compounds_per_year=compounds_per_year,
            contribution_per_period=round(contribution_per_period, 2),
            total_contributions=round(total_contributions, 2),
            interest_earned=round(interest_earned, 2),
            future_value=round(future_value, 2),
        )
