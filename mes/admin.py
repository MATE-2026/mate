from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import (
    BOMReference,
    Carrier,
    Item,
    ItemType,
    OdooProduct,
    OdooVariant,
    OperationMapping,
    PLCEvent,
    Plant,
    ProductionAction,
    ProductionEvent,
    ProductionOrder,
    ProductionStep,
    Segment,
    SegmentType,
    State,
    StateMachine,
    Stock,
    StockReservation,
)


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "enabled")
    search_fields = ("code", "name")
    list_filter = ("enabled",)


@admin.register(SegmentType)
class SegmentTypeAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "enabled")
    search_fields = ("code", "name")
    list_filter = ("enabled",)


@admin.register(StateMachine)
class StateMachineAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "enabled")
    search_fields = ("code", "name")
    list_filter = ("enabled",)


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = (
        "state_machine",
        "number",
        "name",
        "action",
    )
    list_filter = ("state_machine",)
    search_fields = ("name", "action")


@admin.register(Segment)
class SegmentAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "plant",
        "segment_type",
        "state_machine",
        "enabled",
    )
    list_filter = (
        "plant",
        "segment_type",
        "state_machine",
        "enabled",
    )
    search_fields = ("code", "name")


@admin.register(OdooProduct)
class OdooProductAdmin(admin.ModelAdmin):
    list_display = (
        "odoo_id",
        "name",
        "default_code",
        "active",
    )
    search_fields = (
        "name",
        "default_code",
    )
    list_filter = ("active",)


@admin.register(OdooVariant)
class OdooVariantAdmin(admin.ModelAdmin):
    list_display = (
        "odoo_id",
        "name",
        "default_code",
        "product",
        "active",
    )
    search_fields = (
        "name",
        "default_code",
    )
    list_filter = ("active",)


@admin.register(BOMReference)
class BOMReferenceAdmin(admin.ModelAdmin):
    list_display = (
        "odoo_bom_id",
        "product",
        "quantity",
        "active",
    )
    search_fields = ("odoo_bom_id",)
    list_filter = ("active",)


@admin.register(ItemType)
class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "item_type",
        "quantity",
        "reserved_quantity",
        "available_quantity",
        "enabled",
    )
    list_filter = ("item_type", "enabled")
    search_fields = ("code", "name")


@admin.register(OperationMapping)
class OperationMappingAdmin(admin.ModelAdmin):
    list_display = (
        "variant",
        "segment",
        "step",
        "action_key",
        "item",
        "quantity",
        "enabled",
    )
    list_filter = (
        "segment",
        "enabled",
    )
    search_fields = (
        "action_key",
        "variant__name",
        "variant__default_code",
    )


@admin.register(Carrier)
class CarrierAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "current_segment",
        "target_segment",
        "production_order",
        "enabled",
    )
    list_filter = ("enabled",)
    search_fields = ("code",)


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = (
        "item",
        "segment",
        "quantity",
        "reserved_quantity",
        "available_quantity",
    )
    list_filter = ("segment",)
    search_fields = (
        "item__code",
        "item__name",
    )


@admin.register(StockReservation)
class StockReservationAdmin(admin.ModelAdmin):
    list_display = (
        "production_order",
        "stock",
        "quantity",
        "created_at",
    )
    list_filter = ("stock",)


@admin.register(ProductionOrder)
class ProductionOrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number",
        "odoo_mo_id",
        "variant",
        "quantity",
        "status",
        "created_at",
    )
    list_filter = ("status",)
    search_fields = (
        "order_number",
        "variant__name",
        "variant__default_code",
    )


@admin.register(ProductionStep)
class ProductionStepAdmin(admin.ModelAdmin):
    list_display = (
        "production_order",
        "sequence",
        "segment",
        "state_machine",
        "status",
    )
    list_filter = (
        "status",
        "segment",
    )


@admin.register(ProductionAction)
class ProductionActionAdmin(admin.ModelAdmin):
    list_display = (
        "production_step",
        "sequence",
        "action_key",
        "segment_code",
        "item_code",
        "quantity",
        "status",
        "created_at",
    )
    list_filter = ("status",)
    search_fields = (
        "action_key",
        "segment_code",
        "item_code",
    )


@admin.register(ProductionEvent)
class ProductionEventAdmin(admin.ModelAdmin):
    list_display = (
        "production_order",
        "event_type",
        "created_at",
    )
    list_filter = ("event_type",)
    search_fields = (
        "production_order__order_number",
        "event_type",
        "message",
    )


@admin.register(PLCEvent)
class PLCEventAdmin(admin.ModelAdmin):
    list_display = (
        "event_type",
        "source_address",
        "segment",
        "created_at",
    )
    list_filter = ("event_type", "segment")
    search_fields = (
        "source_address",
        "event_type",
    )

