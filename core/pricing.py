"""
Pricing engine for Helping Hand services.

Ported from: Webpage/src/lib/pricing.js
Rates are in INR (Indian Rupees) per day.
"""

from decimal import Decimal, ROUND_HALF_UP
from typing import Optional


# ─── Service Rates (per day) ──────────────────────────────────────────────────

SERVICE_RATES = {
    'nursing': {'daily': Decimal('1500'), 'label': 'Nursing Care'},
    'homecare': {'daily': Decimal('1000'), 'label': 'Home Care'},
    'onetime': {'daily': Decimal('500'), 'label': 'One-Time Service'},
}

# ─── Discount Tiers ───────────────────────────────────────────────────────────

DISCOUNT_TIERS = {
    'daily': {
        'min_days': 1,
        'max_days': 6,
        'discount': Decimal('0'),
        'label': 'daily',
    },
    'weekly': {
        'min_days': 7,
        'max_days': 29,
        'discount': Decimal('0.10'),
        'label': 'weekly',
    },
    'monthly': {
        'min_days': 30,
        'max_days': None,  # No upper limit
        'discount': Decimal('0.25'),
        'label': 'monthly',
    },
}


def get_tier(days: int) -> dict:
    """
    Determine the pricing tier based on the number of days.

    >>> get_tier(5)['label']
    'daily'
    >>> get_tier(14)['label']
    'weekly'
    >>> get_tier(30)['label']
    'monthly'
    """
    if days >= 30:
        return DISCOUNT_TIERS['monthly']
    if days >= 7:
        return DISCOUNT_TIERS['weekly']
    return DISCOUNT_TIERS['daily']


def calculate_price(service_type: str, duration_days: int) -> Optional[dict]:
    """
    Calculate the full pricing breakdown for a booking.

    Args:
        service_type: One of 'nursing', 'homecare', 'onetime'
        duration_days: Number of days for the service

    Returns:
        Dict with base_rate, daily_rate, days, discount, discount_amount,
        subtotal, total, tier, service_name. Returns None if service_type
        is invalid.

    >>> result = calculate_price('nursing', 7)
    >>> result['tier']
    'weekly'
    >>> result['discount']
    Decimal('0.10')
    >>> result['total']
    Decimal('9450')
    """
    rate = SERVICE_RATES.get(service_type)
    if rate is None:
        return None

    # One-time services are always 1 day, no discount
    if service_type == 'onetime':
        return {
            'base_rate': rate['daily'],
            'daily_rate': rate['daily'],
            'days': 1,
            'discount': Decimal('0'),
            'discount_amount': Decimal('0'),
            'subtotal': rate['daily'],
            'total': rate['daily'],
            'tier': 'daily',
            'service_name': rate['label'],
        }

    tier = get_tier(duration_days)
    daily_rate = rate['daily'] * (1 - tier['discount'])
    subtotal = rate['daily'] * duration_days
    discount_amount = (subtotal * tier['discount']).quantize(
        Decimal('1'), rounding=ROUND_HALF_UP
    )
    total = subtotal - discount_amount

    return {
        'base_rate': rate['daily'],
        'daily_rate': daily_rate.quantize(Decimal('1'), rounding=ROUND_HALF_UP),
        'days': duration_days,
        'discount': tier['discount'],
        'discount_amount': discount_amount,
        'subtotal': subtotal,
        'total': total,
        'tier': tier['label'],
        'service_name': rate['label'],
    }


def format_currency(amount) -> str:
    """
    Format an amount as Indian Rupees.

    >>> format_currency(1500)
    '₹1,500'
    >>> format_currency(Decimal('9450'))
    '₹9,450'
    """
    amount = int(amount)
    return f'₹{amount:,}'
<<<<<<< HEAD


def get_tiered_prices(service_type: str) -> Optional[dict]:
    """
    Return daily, weekly, and monthly prices for a service type.

    Uses the actual discount tiers from DISCOUNT_TIERS so that pricing
    stays consistent across the codebase (no hardcoded multipliers).

    >>> result = get_tiered_prices('nursing')
    >>> result['daily']
    Decimal('1500')
    >>> result['weekly']
    1350
    >>> result['monthly']
    1125
    """
    rate = SERVICE_RATES.get(service_type)
    if not rate:
        return None
    daily = rate['daily']
    weekly_discount = DISCOUNT_TIERS['weekly']['discount']
    monthly_discount = DISCOUNT_TIERS['monthly']['discount']
    return {
        'daily': daily,
        'weekly': int(daily * (1 - weekly_discount)),
        'monthly': int(daily * (1 - monthly_discount)),
        'label': rate['label'],
    }
=======
>>>>>>> c33abf1 (Reworked the whole architecture with Django & PostgreSQL)
