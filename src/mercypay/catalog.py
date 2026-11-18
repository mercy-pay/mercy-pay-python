"""Généré par scripts/generate.py depuis le catalogue Mercy Pay. Ne pas modifier à la main.

The open countries, their mobile money operators and the webhook event types. A new operator
may appear before this list knows it: any code stays accepted.
"""

from typing import Dict, List


COUNTRIES: Dict[str, Dict[str, object]] = {
    "CMR": {
        "name": "Cameroun",
        "currency": "XAF",
        "providers": {
            "MTN_MOMO_CMR": "MTN Mobile Money",
            "ORANGE_CMR": "Orange Money"
        }
    },
    "COG": {
        "name": "Congo",
        "currency": "XAF",
        "providers": {
            "MTN_MOMO_COG": "MTN Mobile Money",
            "AIRTEL_COG": "Airtel Money"
        }
    },
    "GAB": {
        "name": "Gabon",
        "currency": "XAF",
        "providers": {
            "AIRTEL_GAB": "Airtel Money",
            "MOOV_GAB": "Moov Money"
        }
    },
    "BEN": {
        "name": "Bénin",
        "currency": "XOF",
        "providers": {
            "MTN_MOMO_BEN": "MTN Mobile Money",
            "MOOV_BEN": "Moov Money"
        }
    },
    "CIV": {
        "name": "Côte d'Ivoire",
        "currency": "XOF",
        "providers": {
            "MTN_MOMO_CIV": "MTN Mobile Money",
            "ORANGE_CIV": "Orange Money",
            "MOOV_CIV": "Moov Money"
        }
    },
    "SEN": {
        "name": "Sénégal",
        "currency": "XOF",
        "providers": {
            "FREE_SEN": "Free Money",
            "ORANGE_SEN": "Orange Money"
        }
    },
    "COD": {
        "name": "RD Congo",
        "currency": "CDF",
        "providers": {
            "VODACOM_MPESA_COD": "M-Pesa",
            "AIRTEL_COD": "Airtel Money",
            "ORANGE_COD": "Orange Money"
        }
    },
    "RWA": {
        "name": "Rwanda",
        "currency": "RWF",
        "providers": {
            "AIRTEL_RWA": "Airtel Money",
            "MTN_MOMO_RWA": "MTN Mobile Money"
        }
    },
    "SLE": {
        "name": "Sierra Leone",
        "currency": "SLE",
        "providers": {
            "ORANGE_SLE": "Orange Money"
        }
    },
    "UGA": {
        "name": "Ouganda",
        "currency": "UGX",
        "providers": {
            "AIRTEL_OAPI_UGA": "Airtel Money",
            "MTN_MOMO_UGA": "MTN Mobile Money"
        }
    },
    "ZMB": {
        "name": "Zambie",
        "currency": "ZMW",
        "providers": {
            "MTN_MOMO_ZMB": "MTN Mobile Money",
            "AIRTEL_OAPI_ZMB": "Airtel Money",
            "ZAMTEL_ZMB": "Zamtel Money"
        }
    },
    "KEN": {
        "name": "Kenya",
        "currency": "KES",
        "providers": {
            "MPESA_KEN": "M-Pesa"
        }
    },
    "MOZ": {
        "name": "Mozambique",
        "currency": "MZN",
        "providers": {
            "VODACOM_MOZ": "M-Pesa"
        }
    }
}

EVENT_TYPES: List[str] = [
    "payment.succeeded",
    "payment.failed",
    "payment.refunded",
    "payment.disputed",
    "payment.dispute_closed",
    "refund.succeeded",
    "refund.failed",
    "refund.canceled",
    "payout.paid",
    "payout.failed",
    "payout.canceled",
    "subscription.created",
    "subscription.updated",
    "subscription.past_due",
    "subscription.unpaid",
    "subscription.paused",
    "subscription.resumed",
    "subscription.canceled",
    "invoice.created",
    "invoice.upcoming",
    "invoice.paid",
    "invoice.canceled",
    "invoice.payment_failed",
    "checkout_session.completed",
    "provider_status.changed",
    "account.updated"
]

MTN_MOMO_CMR = "MTN_MOMO_CMR"
ORANGE_CMR = "ORANGE_CMR"
MTN_MOMO_COG = "MTN_MOMO_COG"
AIRTEL_COG = "AIRTEL_COG"
AIRTEL_GAB = "AIRTEL_GAB"
MOOV_GAB = "MOOV_GAB"
MTN_MOMO_BEN = "MTN_MOMO_BEN"
MOOV_BEN = "MOOV_BEN"
MTN_MOMO_CIV = "MTN_MOMO_CIV"
ORANGE_CIV = "ORANGE_CIV"
MOOV_CIV = "MOOV_CIV"
FREE_SEN = "FREE_SEN"
ORANGE_SEN = "ORANGE_SEN"
VODACOM_MPESA_COD = "VODACOM_MPESA_COD"
AIRTEL_COD = "AIRTEL_COD"
ORANGE_COD = "ORANGE_COD"
AIRTEL_RWA = "AIRTEL_RWA"
MTN_MOMO_RWA = "MTN_MOMO_RWA"
ORANGE_SLE = "ORANGE_SLE"
AIRTEL_OAPI_UGA = "AIRTEL_OAPI_UGA"
MTN_MOMO_UGA = "MTN_MOMO_UGA"
MTN_MOMO_ZMB = "MTN_MOMO_ZMB"
AIRTEL_OAPI_ZMB = "AIRTEL_OAPI_ZMB"
ZAMTEL_ZMB = "ZAMTEL_ZMB"
MPESA_KEN = "MPESA_KEN"
VODACOM_MOZ = "VODACOM_MOZ"
