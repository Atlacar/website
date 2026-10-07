# Copyright 2025 Studio73 - Eugenio Micó <eugenio@studio73.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import tagged

from odoo.addons.base.tests.common import BaseCommon


# post_install: at_install, partners created in setUpClass miss defaults of
# modules loaded later (e.g. purchase_stock's NOT NULL res_partner.group_rfq).
@tagged("post_install", "-at_install")
class TestResConfigSettings(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env["website"].create({"name": "Test Website"})
        cls.config = cls.env["res.config.settings"].create(
            {
                "website_id": cls.website.id,
            }
        )

    def _as_admin(self, record):
        # Website records are only writable by website editors/admins in 20
        return record.with_user(self.env.ref("base.user_admin"))

    def test_compute_whatsapp_enabled(self):
        config = self._as_admin(self.config)
        website = self._as_admin(self.website)
        self.assertFalse(config.whatsapp_enabled)
        website.update({"whatsapp_number": "123456789"})
        config.invalidate_recordset()
        self.assertTrue(config.whatsapp_enabled)
        website.update({"whatsapp_number": False})
        config.invalidate_recordset()
        self.assertFalse(config.whatsapp_enabled)

    def test_inverse_whatsapp_enabled(self):
        config = self._as_admin(self.config)
        website = self._as_admin(self.website)
        website.invalidate_recordset()
        config.invalidate_recordset()
        config.whatsapp_enabled = False
        self.assertFalse(website.whatsapp_number)
