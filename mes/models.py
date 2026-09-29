
from django.db import models


class Plant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class SegmentType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class StateMachine(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class State(models.Model):
    state_machine = models.ForeignKey(
        StateMachine,
        on_delete=models.CASCADE,
        related_name="states",
    )
    number = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    action = models.CharField(max_length=100, blank=True)
    flags = models.CharField(max_length=255, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["state_machine", "number"],
                name="unique_state_number_per_machine",
            )
        ]
        ordering = ["state_machine", "number"]

    def __str__(self):
        return f"{self.state_machine.code} - {self.number} - {self.name}"


class Segment(models.Model):
    plant = models.ForeignKey(
        Plant,
        on_delete=models.PROTECT,
        related_name="segments",
    )
    segment_type = models.ForeignKey(
        SegmentType,
        on_delete=models.PROTECT,
        related_name="segments",
    )
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    state_machine = models.ForeignKey(
        StateMachine,
        on_delete=models.PROTECT,
        related_name="segments",
    )
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class OdooProduct(models.Model):
    odoo_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=255)
    default_code = models.CharField(
        max_length=100,
        blank=True,
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.odoo_id})"


class OdooVariant(models.Model):
    odoo_id = models.PositiveIntegerField(unique=True)
    product = models.ForeignKey(
        OdooProduct,
        on_delete=models.PROTECT,
        related_name="variants",
    )
    name = models.CharField(max_length=255)
    default_code = models.CharField(
        max_length=100,
        blank=True,
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.odoo_id})"


class BOMReference(models.Model):
    odoo_bom_id = models.PositiveIntegerField(unique=True)
    product = models.ForeignKey(
        OdooProduct,
        on_delete=models.PROTECT,
        related_name="bom_references",
    )
    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        default=1,
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"BOM {self.odoo_bom_id} - {self.product.name}"


class ItemType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Item(models.Model):
    item_type = models.ForeignKey(
        ItemType,
        on_delete=models.PROTECT,
        related_name="items",
    )
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=0)
    reserved_quantity = models.PositiveIntegerField(default=0)
    enabled = models.BooleanField(default=True)

    @property
    def available_quantity(self):
        return self.quantity - self.reserved_quantity

    def __str__(self):
        return f"{self.code} - {self.name}"


class OperationMapping(models.Model):
    variant = models.ForeignKey(
        OdooVariant,
        on_delete=models.PROTECT,
        related_name="operation_mappings",
    )
    segment = models.ForeignKey(
        Segment,
        on_delete=models.PROTECT,
        related_name="operation_mappings",
    )
    step = models.PositiveIntegerField()
    item = models.ForeignKey(
        Item,
        on_delete=models.PROTECT,
        related_name="operation_mappings",
        null=True,
        blank=True,
    )
    quantity = models.PositiveIntegerField(default=1)
    action_key = models.CharField(max_length=100)
    enabled = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["variant", "segment", "step"],
                name="unique_operation_mapping",
            )
        ]
        ordering = ["variant", "step"]

    def __str__(self):
        return (
            f"{self.variant.name} - "
            f"{self.segment.code} - "
            f"step {self.step}"
        )


class Carrier(models.Model):
    code = models.CharField(max_length=100, unique=True)
    current_segment = models.ForeignKey(
        Segment,
        on_delete=models.PROTECT,
        related_name="current_carriers",
        null=True,
        blank=True,
    )
    target_segment = models.ForeignKey(
        Segment,
        on_delete=models.PROTECT,
        related_name="target_carriers",
        null=True,
        blank=True,
    )
    production_order = models.ForeignKey(
        "ProductionOrder",
        on_delete=models.SET_NULL,
        related_name="carriers",
        null=True,
        blank=True,
    )
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class Stock(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.PROTECT,
        related_name="stock_records",
    )
    segment = models.ForeignKey(
        Segment,
        on_delete=models.PROTECT,
        related_name="stock_records",
    )
    quantity = models.PositiveIntegerField(default=0)
    reserved_quantity = models.PositiveIntegerField(default=0)

    @property
    def available_quantity(self):
        return self.quantity - self.reserved_quantity

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["item", "segment"],
                name="unique_stock_item_segment",
            )
        ]

    def __str__(self):
        return f"{self.item.code} @ {self.segment.code}"


class StockReservation(models.Model):
    production_order = models.ForeignKey(
        "ProductionOrder",
        on_delete=models.CASCADE,
        related_name="stock_reservations",
    )
    stock = models.ForeignKey(
        Stock,
        on_delete=models.PROTECT,
        related_name="reservations",
    )
    quantity = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.production_order.order_number} - "
            f"{self.stock.item.code} - "
            f"{self.quantity}"
        )


class ProductionOrder(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("planned", "Planned"),
        ("reserved", "Reserved"),
        ("released", "Released"),
        ("running", "Running"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("error", "Error"),
    ]

    odoo_mo_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        unique=True,
    )
    order_number = models.CharField(
        max_length=100,
        unique=True,
    )
    variant = models.ForeignKey(
        OdooVariant,
        on_delete=models.PROTECT,
        related_name="production_orders",
    )
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order_number} - {self.variant.name}"


class ProductionStep(models.Model):
    production_order = models.ForeignKey(
        ProductionOrder,
        on_delete=models.CASCADE,
        related_name="steps",
    )
    sequence = models.PositiveIntegerField()
    segment = models.ForeignKey(
        Segment,
        on_delete=models.PROTECT,
        related_name="production_steps",
    )
    state_machine = models.ForeignKey(
        StateMachine,
        on_delete=models.PROTECT,
        related_name="production_steps",
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("ready", "Ready"),
            ("running", "Running"),
            ("completed", "Completed"),
            ("error", "Error"),
        ],
        default="pending",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["production_order", "sequence"],
                name="unique_production_step_sequence",
            )
        ]
        ordering = ["production_order", "sequence"]

    def __str__(self):
        return (
            f"{self.production_order.order_number} - "
            f"step {self.sequence}"
        )


class ProductionAction(models.Model):
    production_step = models.ForeignKey(
        ProductionStep,
        on_delete=models.CASCADE,
        related_name="actions",
    )
    sequence = models.PositiveIntegerField()
    action_key = models.CharField(max_length=100)
    segment_code = models.CharField(max_length=50)
    item_code = models.CharField(
        max_length=100,
        blank=True,
    )
    quantity = models.PositiveIntegerField(default=1)

    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("sent", "Sent"),
            ("acknowledged", "Acknowledged"),
            ("completed", "Completed"),
            ("error", "Error"),
        ],
        default="pending",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["production_step", "sequence"],
                name="unique_action_sequence",
            )
        ]
        ordering = ["production_step", "sequence"]

    def __str__(self):
        return (
            f"{self.production_step} - "
            f"{self.sequence} - {self.action_key}"
        )


class ProductionEvent(models.Model):
    production_order = models.ForeignKey(
        ProductionOrder,
        on_delete=models.CASCADE,
        related_name="events",
    )
    event_type = models.CharField(max_length=100)
    message = models.TextField(blank=True)
    data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.production_order.order_number} - "
            f"{self.event_type}"
        )


class PLCEvent(models.Model):
    segment = models.ForeignKey(
        Segment,
        on_delete=models.SET_NULL,
        related_name="plc_events",
        null=True,
        blank=True,
    )
    source_address = models.CharField(
        max_length=100,
        blank=True,
    )
    event_type = models.CharField(max_length=100)
    payload = models.BinaryField(
        null=True,
        blank=True,
    )
    metadata = models.JSONField(
        default=dict,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.event_type} - {self.source_address}"
