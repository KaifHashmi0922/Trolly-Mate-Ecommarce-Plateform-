"""
admins/models.py - Trolley Mate E-commerce Admin Models

Core models for company/brand management and product catalog.
Used exclusively in the admin panel for CRUD operations.
"""

from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


class Companys(models.Model):
    """
    Company/Brand model representing suppliers on the platform.

    Each company serves as a "brand" that products belong to.
    Used in admin panel for organizing product catalog.
    """
    
    name = models.CharField(
        max_length=100,
        unique=False,
        help_text=_("Company name as shown to customers."),
    )
    
    category = models.CharField(
        max_length=50,
        help_text=_("High-level category (Electronics, Fashion, Grocery, etc.)."),
    )
    
    des = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        help_text=_("Optional company description or tagline."),
    )
    
    image = models.ImageField(
        upload_to="companies/%Y/%m/",
        blank=True,
        null=True,
        help_text=_("Company logo or brand image (recommended: 200x200px)."),
    )
    
    status = models.BooleanField(
        default=True,
        help_text=_("Active companies appear in product dropdowns."),
    )
    
    created_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_("Timestamp of company creation."),
    )

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")
        ordering = ['-created_at', 'name']
        indexes = [
            models.Index(fields=['name', 'category']),
            models.Index(fields=['status']),
        ]

    def save(self, *args, **kwargs):
        """
        Override save to set created_at only on first save.
        """
        if not self.created_at:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.name} ({self.category})"

    def product_count(self) -> int:
        """Return number of products under this company."""
        return self.products.count()


class Products(models.Model):
    """
    Product model for e-commerce catalog.

    Each product belongs to one Company (brand) and has full inventory tracking.
    Supports soft-delete via status field.
    """
    
    name = models.CharField(
        max_length=100,
        help_text=_("Product name visible to customers."),
    )
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text=_("Current selling price in ₹."),
    )
    
    category = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_("Product category (auto-copied from company)."),
    )
    
    company = models.ForeignKey(
        Companys,
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True,
        help_text=_("Brand/manufacturer of this product."),
    )
    
    des = models.TextField(
        max_length=500,
        blank=True,
        help_text=_("Product description or specifications."),
    )
    
    image = models.ImageField(
        upload_to="products/%Y/%m/%d/",
        help_text=_("Main product image (recommended: 400x400px)."),
    )
    
    quantity = models.PositiveIntegerField(
        default=0,
        blank=True,
        null=True,
        help_text=_("Current stock quantity (0 = out of stock)."),
    )
    
    status = models.BooleanField(
        default=True,
        help_text=_("False = hidden from customers (soft delete)."),
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("Product creation timestamp.")
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_("Last modification timestamp."),
    )

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'quantity']),
            models.Index(fields=['company', 'status']),
            models.Index(fields=['name']),
        ]

    def __str__(self) -> str:
        company_name = self.company.name if self.company else "No Company"
        return f"{self.name} - ₹{self.price} ({company_name})"

    @property
    def is_in_stock(self) -> bool:
        """Check if product has available stock."""
        return self.status and (self.quantity or 0) > 0

    @property
    def stock_status(self) -> str:
        """Return human-readable stock status."""
        if not self.status:
            return "Inactive"
        if self.quantity == 0:
            return "Out of Stock"
        if self.quantity <= 10:
            return "Low Stock"
        return "In Stock"

    def get_absolute_url(self):
        """Future URL for product detail page."""
        return f"/products/{self.id}/"
