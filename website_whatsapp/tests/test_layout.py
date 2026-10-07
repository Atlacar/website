# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestLayout(HttpCase):
    def test_floating_icon_rendered(self):
        website = (
            self.env["website"]
            .with_user(self.env.ref("base.user_admin"))
            .search([], limit=1)
        )
        website.write(
            {
                "whatsapp_number": "5215512345678",
                "whatsapp_text": "Hello",
                "whatsapp_track_url": True,
            }
        )
        html = self.url_open("/").text
        self.assertIn('id="whatsapp_icon"', html)
        self.assertIn("https://wa.me/5215512345678/?text=Hello", html)
        self.assertIn("Sent from:", html)

    def test_no_icon_without_number(self):
        website = (
            self.env["website"]
            .with_user(self.env.ref("base.user_admin"))
            .search([], limit=1)
        )
        website.whatsapp_number = False
        html = self.url_open("/").text
        self.assertNotIn('id="whatsapp_icon"', html)
