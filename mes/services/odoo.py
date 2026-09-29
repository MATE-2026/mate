import xmlrpc.client

from django.conf import settings


class OdooError(Exception):
    """Raised when communication with Odoo fails."""


class OdooClient:
    """
    Read-only Odoo client.

    This class is intentionally limited to reading data from Odoo.
    It must not perform create/write/unlink operations.
    """

    def __init__(self):
        self.url = settings.ODOO_URL.rstrip("/")
        self.database = settings.ODOO_DB
        self.username = settings.ODOO_USER
        self.api_key = settings.ODOO_API_KEY

        if not self.username:
            raise OdooError(
                "ODOO_USER is not configured."
            )

        if not self.api_key:
            raise OdooError(
                "ODOO_API_KEY is not configured."
            )

        self.common = xmlrpc.client.ServerProxy(
            f"{self.url}/xmlrpc/2/common"
        )

        self.models = xmlrpc.client.ServerProxy(
            f"{self.url}/xmlrpc/2/object"
        )

        try:
            self.uid = self.common.authenticate(
                self.database,
                self.username,
                self.api_key,
                {},
            )
        except Exception as exc:
            raise OdooError(
                f"Could not connect to Odoo: {exc}"
            ) from exc

        if not self.uid:
            raise OdooError(
                "Odoo authentication failed."
            )

    def version(self):
        """Return Odoo server version information."""
        try:
            return self.common.version()
        except Exception as exc:
            raise OdooError(
                f"Could not retrieve Odoo version: {exc}"
            ) from exc

    def search_read(
        self,
        model,
        domain=None,
        fields=None,
        limit=None,
        offset=0,
        order=None,
    ):
        """
        Read records from Odoo.

        This method intentionally exposes only search_read.
        """

        kwargs = {
            "fields": fields or [],
            "offset": offset,
        }

        if limit is not None:
            kwargs["limit"] = limit

        if order:
            kwargs["order"] = order

        try:
            return self.models.execute_kw(
                self.database,
                self.uid,
                self.api_key,
                model,
                "search_read",
                [domain or []],
                kwargs,
            )
        except Exception as exc:
            raise OdooError(
                f"Odoo read failed for {model}: {exc}"
            ) from exc

    def products(self, limit=None):
        """Read Odoo product templates."""
        return self.search_read(
            "product.template",
            fields=[
                "id",
                "name",
                "default_code",
                "active",
            ],
            limit=limit,
            order="id",
        )

    def variants(self, limit=None):
        """Read Odoo product variants."""
        return self.search_read(
            "product.product",
            fields=[
                "id",
                "name",
                "default_code",
                "active",
                "product_tmpl_id",
            ],
            limit=limit,
            order="id",
        )

    def boms(self, limit=None):
        """Read Odoo BOM headers."""
        return self.search_read(
            "mrp.bom",
            fields=[
                "id",
                "product_tmpl_id",
                "product_id",
                "product_qty",
                "active",
            ],
            limit=limit,
            order="id",
        )

    def bom_lines(self, limit=None):
        """Read Odoo BOM lines."""
        return self.search_read(
            "mrp.bom.line",
            fields=[
                "id",
                "bom_id",
                "product_id",
                "product_qty",
            ],
            limit=limit,
            order="id",
        )

    def manufacturing_orders(self, limit=None):
        """Read Odoo manufacturing orders."""
        return self.search_read(
            "mrp.production",
            fields=[
                "id",
                "name",
                "product_id",
                "product_qty",
                "state",
            ],
            limit=limit,
            order="id",
        )

