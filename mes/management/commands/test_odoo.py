from django.core.management.base import BaseCommand

from mes.services.odoo import OdooClient, OdooError


class Command(BaseCommand):
    help = "Test read-only connectivity to Odoo."

    def handle(self, *args, **options):
        self.stdout.write("Testing Odoo connection...")

        try:
            client = OdooClient()

            version = client.version()

            self.stdout.write(
                self.style.SUCCESS(
                    "Odoo connection successful."
                )
            )

            self.stdout.write(
                f"Odoo version: {version.get('server_version')}"
            )

            products = client.products(limit=5)

            self.stdout.write(
                f"Products returned: {len(products)}"
            )

            for product in products:
                self.stdout.write(
                    f"  {product['id']}: "
                    f"{product['name']} "
                    f"({product.get('default_code') or 'no code'})"
                )

        except OdooError as exc:
            self.stdout.write(
                self.style.ERROR(str(exc))
            )
