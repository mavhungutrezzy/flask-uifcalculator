from dataclasses import dataclass


@dataclass(frozen=True)
class VatCalculationResult:
    amount: float
    vat_rate: float
    vat_amount: float
    amount_excluding_vat: float
    amount_including_vat: float


class VatCalculator:
    DEFAULT_VAT_RATE = 15.0

    @staticmethod
    def calculate(amount: float, vat_rate: float, amount_type: str) -> VatCalculationResult:
        if amount < 0:
            raise ValueError("Amount must be zero or greater")

        if vat_rate < 0:
            raise ValueError("VAT rate must be zero or greater")

        rate_decimal = vat_rate / 100

        if amount_type == "exclusive":
            amount_excluding_vat = amount
            vat_amount = amount_excluding_vat * rate_decimal
            amount_including_vat = amount_excluding_vat + vat_amount
        elif amount_type == "inclusive":
            amount_including_vat = amount
            divisor = 1 + rate_decimal
            amount_excluding_vat = amount_including_vat / divisor if divisor else amount_including_vat
            vat_amount = amount_including_vat - amount_excluding_vat
        else:
            raise ValueError("Invalid amount type selected")

        return VatCalculationResult(
            amount=round(amount, 2),
            vat_rate=round(vat_rate, 2),
            vat_amount=round(vat_amount, 2),
            amount_excluding_vat=round(amount_excluding_vat, 2),
            amount_including_vat=round(amount_including_vat, 2),
        )
