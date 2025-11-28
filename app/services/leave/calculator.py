"""Leave Benefit Top-up Calculator.

This module calculates the UIF top-up amount payable while an employee is on
paid maternity / adoption / parental / illness leave, according to the rules
published by the Department of Employment & Labour (2024/2025).

Rules implemented
-----------------
1. Daily benefit amount (DBA)
   DBA = 66 % of the employee's gross *monthly* income, but only up to
   the statutory ceiling of R17 712 per month.

2. Daily income (Y1)
   The employee's normal daily gross remuneration.  It is calculated from the
   *uncapped* average monthly salary:
       Y1 = monthly_salary × 12 / 365.

3. Daily income while on leave (Y2)
   The salary the employee actually receives while on leave, converted to a
   daily amount in the same way:
       Y2 = leave_salary × 12 / 365.

4. UIF daily top-up
       difference = Y1 − Y2
       top_up   = min(difference, DBA)  if difference > 0  else 0

All monetary results are rounded to two decimals for display purposes only.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LeaveBenefitResult:
    """Container for all calculated values needed by the template."""

    monthly_salary: float  # Original salary before leave (uncapped)
    leave_salary: float  # Salary received while on leave (uncapped)
    daily_income: float  # Y1 – daily income from monthly_salary
    daily_leave_income: float  # Y2 – daily income while on leave
    daily_benefit_amount: float  # DBA – daily benefit limit (capped & 66 %)
    difference: float  # Y1 − Y2
    top_up_daily: float  # UIF top-up paid per day


class LeaveBenefitCalculator:
    """Performs the UIF top-up calculation for leave benefits."""

    SALARY_CAP: float = 17_712.0  # Statutory ceiling (monthly)
    PERCENTAGE: float = 0.66  # 66 %
    DAYS_PER_YEAR: int = 365  # Used to convert monthly to daily

    @classmethod
    def _monthly_to_daily(cls, monthly_amount: float) -> float:
        """Convert a monthly amount to a daily amount using the UIF factor."""
        return (monthly_amount * 12) / cls.DAYS_PER_YEAR

    @classmethod
    def calculate(
        cls, monthly_salary: float, leave_salary: float
    ) -> LeaveBenefitResult:
        """Return a fully populated ``LeaveBenefitResult`` instance.

        Parameters
        ----------
        monthly_salary
            Employee's normal gross monthly income before going on leave.
        leave_salary
            Income (if any) that the employee will earn while on leave.
        """
        if monthly_salary < 0 or leave_salary < 0:
            raise ValueError("Salary amounts must be non-negative numbers")

        # 1. Daily income (uncapped) – Y1
        daily_income = cls._monthly_to_daily(monthly_salary)

        # 2. Daily income while on leave – Y2
        daily_leave_income = cls._monthly_to_daily(leave_salary)

        # 3. Daily benefit amount (DBA)
        capped_salary = min(monthly_salary, cls.SALARY_CAP)
        daily_benefit_amount = cls._monthly_to_daily(capped_salary) * cls.PERCENTAGE

        # 4. Difference and UIF top-up
        difference = max(daily_income - daily_leave_income, 0)
        top_up_daily = min(difference, daily_benefit_amount)

        # Round monetary outputs to two decimals for presentation.
        return LeaveBenefitResult(
            monthly_salary=round(monthly_salary, 2),
            leave_salary=round(leave_salary, 2),
            daily_income=round(daily_income, 2),
            daily_leave_income=round(daily_leave_income, 2),
            daily_benefit_amount=round(daily_benefit_amount, 2),
            difference=round(difference, 2),
            top_up_daily=round(top_up_daily, 2),
        )
