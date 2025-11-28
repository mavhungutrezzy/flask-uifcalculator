from dataclasses import dataclass
from datetime import datetime


@dataclass
class UnemploymentBenefitResult:
    average_salary: float
    daily_income: float  # Y1
    irr: float  # The calculated percentage (e.g., 38.0)
    daily_benefit: float  # The actual daily payout amount
    credit_days: int  # Days available to claim
    total_benefit: float  # Total payout (daily * credits)
    days_worked: int  # Total days employed
    months_for_benefits: float  # Estimated duration in months


class UnemploymentBenefitCalculator:
    # Constants based on regulations
    SALARY_CAP: float = 17_712.00  # Monthly ceiling
    MAX_CREDIT_DAYS: int = 365  # Maximum accruable days
    DAYS_PER_YEAR: int = 365  # Fixed year divisor

    # IRR Formula Constants
    IRR_BASE: float = 29.2
    IRR_NUMERATOR: float = 7173.92
    IRR_DENOMINATOR_OFFSET: float = 232.92

    @staticmethod
    def calculate_credit_days(start_date: str, end_date: str) -> tuple:
        """
        Calculate credit days: 1 credit day for every 4 days worked.
        Returns (credit_days, days_worked).
        """
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")

            # Calculate total days worked (inclusive)
            days_worked = (end - start).days + 1

            if days_worked < 0:
                raise ValueError("End date cannot be before start date")

            # Rule: 1 credit day for every 4 days worked
            credit_days = days_worked // 4

            # Rule: Cap at 365 credit days
            final_credits = min(
                credit_days, UnemploymentBenefitCalculator.MAX_CREDIT_DAYS
            )

            return final_credits, days_worked

        except ValueError as e:
            raise ValueError(f"Date calculation error: {str(e)}")

    @classmethod
    def calculate_benefits(
        cls,
        average_salary: float,
        start_date: str,
        end_date: str,
    ) -> UnemploymentBenefitResult:
        """
        Calculate benefits using the formula:
        1. Cap Salary at 17,712
        2. Daily Income (Y1) = Salary * 12 / 365
        3. IRR = 29.2 + (7173.92 / (232.92 + Y1))
        4. Daily Benefit = Y1 * IRR
        """

        # 1. Apply Salary Cap
        # If input is 20,000, we use 17,712. If 10,000, we use 10,000.
        capped_salary = min(average_salary, cls.SALARY_CAP)

        # 2. Calculate Daily Income (Y1)
        # Formula: Average salary x 12 / 365
        daily_income_y1 = (capped_salary * 12) / cls.DAYS_PER_YEAR

        # 3. Calculate Income Replacement Rate (IRR)
        # Formula: 29.2 + (7173.92 / (232.92 + Y1))
        if daily_income_y1 > 0:
            irr_percentage = cls.IRR_BASE + (
                cls.IRR_NUMERATOR / (cls.IRR_DENOMINATOR_OFFSET + daily_income_y1)
            )
        else:
            irr_percentage = 0.0

        # Ensure IRR doesn't exceed bounds (though the formula naturally curves it)
        # Typically caps between 38% (high earners) and 60% (low earners)

        # 4. Calculate Daily Benefit Amount (DBA)
        # Formula: Y1 x IRR%
        daily_benefit = daily_income_y1 * (irr_percentage / 100)

        # 5. Calculate Credit Days
        credit_days, days_worked = cls.calculate_credit_days(start_date, end_date)

        # 6. Calculate Total Benefit
        total_benefit = daily_benefit * credit_days

        # derived metric: how many months (approx) will the money last?
        months_for_benefits = credit_days / 30.44 if credit_days > 0 else 0

        return UnemploymentBenefitResult(
            average_salary=round(capped_salary, 2),
            daily_income=round(daily_income_y1, 2),
            irr=round(irr_percentage, 2),  # Rounded to 2 decimals for display
            daily_benefit=round(daily_benefit, 2),
            credit_days=credit_days,
            total_benefit=round(total_benefit, 2),
            days_worked=days_worked,
            months_for_benefits=round(months_for_benefits, 1),
        )
