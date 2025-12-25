"""
admins/templatetags/admin_tags.py - Trolley Mate Admin Template Filters

Custom Django template filters for e-commerce admin panel.
Handles currency formatting, cart operations, order filtering, and math utilities.
"""

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# =============================================================================
# CURRENCY & FORMATTING
# =============================================================================

@register.filter
def Currency(value):
    """
    Format numeric value as Indian Rupee currency.

    Args:
        value: Numeric price value

    Returns:
        str: "₹1,234" format
    """
    try:
        return mark_safe(f"₹{int(float(value)):,.0f}")
    except (ValueError, TypeError):
        return mark_safe("₹0")


# =============================================================================
# CART OPERATIONS
# =============================================================================

@register.filter
def cart_status(product, cart):
    """
    Check if product exists in cart.

    Args:
        product: Product instance
        cart: Cart dictionary (session)

    Returns:
        bool: True if product in cart
    """
    if not isinstance(cart, dict):
        return False
    return str(product.id) in cart


@register.filter
def cart_quantity(product, cart):
    """
    Get quantity of product in cart.

    Args:
        product: Product instance
        cart: Cart dictionary

    Returns:
        int: Cart quantity (0 if not in cart)
    """
    try:
        if not isinstance(cart, dict):
            return 0
        return int(cart.get(str(product.id), 0))
    except (TypeError, ValueError):
        return 0


@register.filter
def total_price(product, cart):
    """
    Calculate total price for single product in cart.

    Args:
        product: Product instance
        cart: Cart dictionary

    Returns:
        float: product.price * cart_quantity
    """
    qty = cart_quantity(product, cart)
    try:
        return float(product.price) * qty
    except (TypeError, ValueError):
        return 0


@register.filter
def grand_total(products, cart):
    """
    Calculate grand total for all products in cart.

    Args:
        products: Product queryset/list
        cart: Cart dictionary

    Returns:
        float: Sum of all cart item totals
    """
    if not isinstance(cart, dict):
        return 0
    total = 0
    for product in products:
        qty = cart_quantity(product, cart)
        try:
            total += float(product.price) * qty
        except (TypeError, ValueError):
            continue
    return total


# =============================================================================
# QUANTITY HELPERS
# =============================================================================

@register.filter
def quantity(product, cart):
    """
    Get cart quantity (for display in templates).

    Usage:
        {{ product|quantity:request.session.cart }}

    Returns:
        int: Quantity (0 if not in cart)
    """
    return cart_quantity(product, cart)


@register.filter
def p_quantity(product, cart):
    """
    Alias for cart_quantity, kept for backwards compatibility.

    Returns:
        int: Cart quantity
    """
    return cart_quantity(product, cart)


# =============================================================================
# MATH UTILITIES
# =============================================================================

@register.filter
def mul(value, arg):
    """
    Safe multiplication of two values.

    Args:
        value: First number
        arg: Second number

    Returns:
        int: value * arg or 0 on error
    """
    try:
        return int(float(value or 0)) * int(float(arg or 0))
    except (ValueError, TypeError, OverflowError):
        return 0


# =============================================================================
# ORDER FILTERING
# =============================================================================

@register.filter
def filter_status_active(orders):
    """
    Filter orders by active status (status=True).

    Args:
        orders: Order queryset/list

    Returns:
        list: Active orders only
    """
    return [order for order in orders if getattr(order, "status", False)]


@register.filter
def filter_status_pending(orders):
    """
    Filter orders by pending/inactive status.

    Args:
        orders: Order queryset/list

    Returns:
        list: Pending orders only
    """
    return [order for order in orders if not getattr(order, "status", True)]


# =============================================================================
# STOCK STATUS
# =============================================================================

@register.filter
def stock_status(product):
    """
    Get human-readable stock status with Bootstrap badge.

    Args:
        product: Product instance

    Returns:
        str: HTML badge with stock status
    """
    quantity = getattr(product, "quantity", 0)

    if not getattr(product, "status", True):
        return mark_safe('<span class="badge bg-secondary">Inactive</span>')
    elif quantity == 0:
        return mark_safe('<span class="badge bg-danger">Out of Stock</span>')
    elif quantity <= 10:
        return mark_safe('<span class="badge bg-warning text-dark">Low Stock</span>')
    else:
        return mark_safe('<span class="badge bg-success">In Stock</span>')


@register.filter
def is_in_stock(product):
    """
    Check if product is available for purchase.

    Args:
        product: Product instance

    Returns:
        bool: True if in stock and active
    """
    return getattr(product, "status", False) and getattr(product, "quantity", 0) > 0


# =============================================================================
# GENERIC HELPERS
# =============================================================================

@register.filter
def get_item(value, arg):
    """
    Get value from dict using key.

    Usage:
        {{ some_dict|get_item:key }}
    """
    try:
        if isinstance(value, dict):
            return value.get(arg)
        return None
    except (KeyError, TypeError, ValueError):
        return None
