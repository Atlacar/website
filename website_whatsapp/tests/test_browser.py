# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestBrowser(HttpCase):
    """Real browser checks; no WhatsApp message is ever sent (link only)."""

    def test_settings_page(self):
        self.browser_js(
            "/odoo/action-website.action_website_configuration",
            """
            const start = Date.now();
            const poll = setInterval(() => {
                const el = document.querySelector("#website_whatsapp_setting");
                if (el) {
                    clearInterval(poll);
                    if (!el.querySelector("[name='whatsapp_enabled']")) {
                        console.error("whatsapp_enabled field missing");
                        return;
                    }
                    console.log("test successful");
                } else if (Date.now() - start > 40000) {
                    clearInterval(poll);
                    console.error("whatsapp setting block not found");
                }
            }, 250);
            """,
            login="admin",
        )

    def test_floating_link(self):
        website = self.env["website"].with_user(self.env.ref("base.user_admin"))
        website = website.search([], limit=1)
        website.write(
            {
                "whatsapp_number": "5215512345678",
                "whatsapp_text": "Hello",
                "whatsapp_track_url": False,
            }
        )
        self.browser_js(
            "/",
            """
            const start = Date.now();
            const poll = setInterval(() => {
                const a = document.querySelector("a#whatsapp_icon");
                if (a) {
                    clearInterval(poll);
                    if (a.getAttribute("href") !== "https://wa.me/5215512345678/?text=Hello") {
                        console.error("unexpected href " + a.getAttribute("href"));
                    } else if (!a.querySelector("i.fa-whatsapp")) {
                        console.error("icon missing");
                    } else {
                        console.log("test successful");
                    }
                } else if (Date.now() - start > 20000) {
                    clearInterval(poll);
                    console.error("floating icon not found");
                }
            }, 250);
            """,
        )
