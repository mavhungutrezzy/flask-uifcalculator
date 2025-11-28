import logging

from flask import Blueprint, render_template, request

from app.services.unemployment.calculator import UnemploymentBenefitCalculator
from app.services.leave.calculator import LeaveBenefitCalculator

logger = logging.getLogger(__name__)

uif_bp = Blueprint("uif", __name__, url_prefix="/uif")


@uif_bp.route("/unemployment-calculator/", methods=["GET", "POST"])
def unemployment_calculator():
    if request.method == "POST":
        try:
            # 1. Extract form data using the names from your HTML
            start_date = request.form.get("start_date")
            end_date = request.form.get("end_date")
            salary_input = request.form.get(
                "single_salary"
            )  # Matches HTML name="single_salary"

            # 2. Validation: Ensure all fields are present
            if not all([start_date, end_date, salary_input]):
                # You might want to flash a message here
                return render_template(
                    "uif/unemployment/form.html", error="All fields are required"
                )

            # 3. Convert salary to float (Handle value errors)
            try:
                average_salary = float(salary_input)
            except ValueError:
                return render_template(
                    "uif/unemployment/form.html", error="Invalid salary amount"
                )

            # 4. Call the Refactored Calculator
            # We pass the single float salary, not a list
            result = UnemploymentBenefitCalculator.calculate_benefits(
                average_salary=average_salary, start_date=start_date, end_date=end_date
            )

            # 5. Calculate Average Monthly Benefit (derived for view)
            # Total Benefit / Months (avoid division by zero)
            avg_monthly_benefit = 0
            if result.months_for_benefits > 0:
                avg_monthly_benefit = result.total_benefit / result.months_for_benefits

            return render_template(
                "uif/unemployment/result.html",
                # Pass the result object if your template supports it: result=result
                # Or pass individual fields to match your legacy template:
                total_benefit=result.total_benefit,
                credit_days=result.credit_days,
                average_salary=result.average_salary,
                daily_income=result.daily_income,
                irr=result.irr,
                daily_benefit=result.daily_benefit,
                days_worked=result.days_worked,
                months_for_benefits=result.months_for_benefits,
                average_monthly_benefit=round(avg_monthly_benefit, 2),
            )

        except ValueError as e:
            # Catch errors from the calculator (like end_date before start_date)
            logger.warning(f"Calculation Logic Error: {e}")
            return render_template("uif/unemployment/form.html", error=str(e))

        except Exception:
            # Log unexpected errors
            logger.exception("Unexpected error in unemployment_calculator")
            raise

    return render_template("uif/unemployment/form.html")


@uif_bp.route("/leave-benefit-calculator/", methods=["GET", "POST"])
def leave_benefit_calculator():
    if request.method == "POST":
        monthly_salary_input = request.form.get("monthly_salary")
        leave_salary_input = request.form.get("leave_salary")

        # Validation
        if not all([monthly_salary_input, leave_salary_input]):
            return render_template(
                "uif/leave/form.html", error="All fields are required"
            )
        try:
            monthly_salary = float(monthly_salary_input)
            leave_salary = float(leave_salary_input)
        except ValueError:
            return render_template("uif/leave/form.html", error="Invalid salary amount")

        try:
            result = LeaveBenefitCalculator.calculate(monthly_salary, leave_salary)
        except ValueError as e:
            return render_template("uif/leave/form.html", error=str(e))

        return render_template(
            "uif/leave/result.html",
            monthly_salary=result.monthly_salary,
            leave_salary=result.leave_salary,
            daily_income=result.daily_income,
            daily_leave_income=result.daily_leave_income,
            daily_benefit_amount=result.daily_benefit_amount,
            difference=result.difference,
            top_up_daily=result.top_up_daily,
        )

    return render_template("uif/leave/form.html")
