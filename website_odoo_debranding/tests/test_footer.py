# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestFooter(HttpCase):
    def test_promotion_message_removed(self):
        view = self.env.ref("website_odoo_debranding.layout_footer_copyright")
        # post_init_hook only disables the view when the module is installed in
        # test mode; set the starting state explicitly so the test also holds
        # when the module was installed first and tested on update.
        view.active = False
        html = self.url_open("/").text
        self.assertIn("Powered by", html)
        view.active = True
        html = self.url_open("/").text
        self.assertNotIn("Powered by", html)
        self.assertNotIn("odoo.com?utm_source=db", html)
        self.assertNotIn("Create a", html.split("o_footer_copyright")[-1][:600])
