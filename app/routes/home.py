from flask import Blueprint, render_template, current_app, send_from_directory
from flask import request

from app.services.compound_interest.calculator import CompoundInterestCalculator
from app.services.vat.calculator import VatCalculator

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def index():
    return render_template("home.html")


@home_bp.route("/uif-status-check-online")
def uif_status_check_online():
    return render_template("pages/uif_status_check.html")


@home_bp.route("/calculators/vat-calculator/", methods=["GET", "POST"])
def vat_calculator():
    if request.method == "POST":
        amount_input = request.form.get("amount")
        vat_rate_input = request.form.get("vat_rate")
        amount_type = request.form.get("amount_type")

        if not amount_input or not amount_type:
            return render_template(
                "vat/form.html",
                error="Amount and amount type are required",
                default_vat_rate=VatCalculator.DEFAULT_VAT_RATE,
            )

        try:
            amount = float(amount_input)
        except ValueError:
            return render_template(
                "vat/form.html",
                error="Invalid amount",
                default_vat_rate=VatCalculator.DEFAULT_VAT_RATE,
            )

        try:
            vat_rate = (
                float(vat_rate_input)
                if vat_rate_input
                else VatCalculator.DEFAULT_VAT_RATE
            )
        except ValueError:
            return render_template(
                "vat/form.html",
                error="Invalid VAT rate",
                default_vat_rate=VatCalculator.DEFAULT_VAT_RATE,
            )

        try:
            result = VatCalculator.calculate(amount, vat_rate, amount_type)
        except ValueError as e:
            return render_template(
                "vat/form.html",
                error=str(e),
                default_vat_rate=VatCalculator.DEFAULT_VAT_RATE,
            )

        return render_template(
            "vat/result.html",
            amount=result.amount,
            amount_type=amount_type,
            vat_rate=result.vat_rate,
            vat_amount=result.vat_amount,
            amount_excluding_vat=result.amount_excluding_vat,
            amount_including_vat=result.amount_including_vat,
        )

    return render_template(
        "vat/form.html", default_vat_rate=VatCalculator.DEFAULT_VAT_RATE
    )


@home_bp.route("/calculators/compound-interest-calculator/", methods=["GET", "POST"])
def compound_interest_calculator():
    if request.method == "POST":
        initial_investment_input = request.form.get("initial_investment")
        annual_interest_rate_input = request.form.get("annual_interest_rate")
        years_input = request.form.get("years")
        compounds_per_year_input = request.form.get("compounds_per_year")
        contribution_per_period_input = request.form.get("contribution_per_period")

        if not all(
            [
                initial_investment_input,
                annual_interest_rate_input,
                years_input,
                compounds_per_year_input,
            ]
        ):
            return render_template(
                "compound_interest/form.html", error="All required fields must be filled"
            )

        try:
            initial_investment = float(initial_investment_input)
            annual_interest_rate = float(annual_interest_rate_input)
            years = float(years_input)
            compounds_per_year = int(compounds_per_year_input)
            contribution_per_period = (
                float(contribution_per_period_input)
                if contribution_per_period_input
                else 0.0
            )
        except ValueError:
            return render_template(
                "compound_interest/form.html", error="Invalid number provided"
            )

        try:
            result = CompoundInterestCalculator.calculate(
                initial_investment=initial_investment,
                annual_interest_rate=annual_interest_rate,
                years=years,
                compounds_per_year=compounds_per_year,
                contribution_per_period=contribution_per_period,
            )
        except ValueError as e:
            return render_template("compound_interest/form.html", error=str(e))

        compounding_labels = {
            1: "Annually",
            2: "Semi-Annually",
            4: "Quarterly",
            12: "Monthly",
            365: "Daily",
        }

        return render_template(
            "compound_interest/result.html",
            initial_investment=result.initial_investment,
            annual_interest_rate=result.annual_interest_rate,
            years=result.years,
            compounds_per_year=result.compounds_per_year,
            compounding_label=compounding_labels.get(
                result.compounds_per_year, f"{result.compounds_per_year}x per year"
            ),
            contribution_per_period=result.contribution_per_period,
            total_contributions=result.total_contributions,
            interest_earned=result.interest_earned,
            future_value=result.future_value,
        )

    return render_template("compound_interest/form.html")


@home_bp.route("/robots.txt")
def robots_txt():
    """Serve the robots.txt file from the static directory."""
    return send_from_directory(
        current_app.static_folder, "robots.txt", mimetype="text/plain"
    )


@home_bp.route("/sitemap.xml")
def sitemap_xml():
    """Serve the sitemap.xml file from the static directory."""
    return send_from_directory(
        current_app.static_folder, "sitemap.xml", mimetype="application/xml"
    )


@home_bp.route("/ads.txt")
def ads_txt():
    """Serve the ads.txt file from the static directory."""
    return send_from_directory(
        current_app.static_folder, "ads.txt", mimetype="text/plain"
    )
