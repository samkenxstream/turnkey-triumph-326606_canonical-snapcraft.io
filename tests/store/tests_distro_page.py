import responses
from urllib.parse import urlencode
from flask_testing import TestCase
from webapp.app import create_app


class GetDistroPageTest(TestCase):
    render_templates = False

    snap_payload = {
        "snap-id": "id",
        "name": "snapName",
        "default-track": None,
        "snap": {
            "title": "Snap Title",
            "summary": "This is a summary",
            "description": "this is a description",
            "media": [],
            "license": "license",
            "prices": 0,
            "publisher": {
                "display-name": "Toto",
                "username": "toto",
                "validation": True,
            },
            "categories": [{"name": "test"}],
            "trending": False,
            "unlisted": False,
        },
        "channel-map": [
            {
                "channel": {
                    "architecture": "amd64",
                    "name": "stable",
                    "risk": "stable",
                    "track": "latest",
                    "released-at": "2018-09-18T14:45:28.064633+00:00",
                },
                "created-at": "2018-09-18T14:45:28.064633+00:00",
                "version": "1.0",
                "confinement": "conf",
                "download": {"size": 100000},
            }
        ],
    }

    def setUp(self):
        self.snap_name = "toto"
        self.api_url = "".join(
            [
                "https://api.snapcraft.io/v2/",
                "snaps/info/",
                self.snap_name,
                "?",
                urlencode(
                    {
                        "fields": ",".join(
                            [
                                "title",
                                "summary",
                                "description",
                                "license",
                                "contact",
                                "website",
                                "publisher",
                                "prices",
                                "media",
                                "download",
                                "version",
                                "created-at",
                                "confinement",
                                "categories",
                                "trending",
                                "unlisted",
                            ]
                        )
                    }
                ),
            ]
        )
        self.featured_snaps_api_url = "".join(
            [
                "https://api.snapcraft.io/api/v1/",
                "snaps/search",
                "?",
                urlencode(
                    {
                        "q": "",
                        "size": "13",
                        "page": "1",
                        "scope": "wide",
                        "confinement": "strict,classic",
                        "fields": "package_name,title,summary,"
                        "architecture,media,developer_name,developer_id,"
                        "developer_validation,origin,apps,sections",
                        "arch": "wide",
                        "section": "featured",
                    }
                ),
            ]
        )
        self.endpoint_url = "/install/" + self.snap_name + "/debian"

    def create_app(self):
        app = create_app(testing=True)
        app.secret_key = "secret_key"
        app.config["WTF_CSRF_METHODS"] = []

        return app

    @responses.activate
    def test_api_404(self):
        payload = {"error-list": []}
        responses.add(
            responses.Response(
                method="GET", url=self.api_url, json=payload, status=404
            )
        )

        response = self.client.get(self.endpoint_url)

        self.assertEqual(len(responses.calls), 1)
        called = responses.calls[0]
        self.assertEqual(called.request.url, self.api_url)

        self.assert404(response)

    @responses.activate
    def test_api_500(self):
        payload = {"error-list": []}
        responses.add(
            responses.Response(
                method="GET", url=self.api_url, json=payload, status=500
            )
        )

        response = self.client.get(self.endpoint_url)

        self.assertEqual(len(responses.calls), 1)
        called = responses.calls[0]
        self.assertEqual(called.request.url, self.api_url)

        self.assertStatus(response, 502)

    def test_no_distro_data(self):
        response = self.client.get("/install/" + self.snap_name + "/noname")

        self.assert404(response)

    @responses.activate
    def test_get_page(self):
        payload = self.snap_payload

        responses.add(
            responses.Response(
                method="GET", url=self.api_url, json=payload, status=200
            )
        )

        responses.add(
            responses.Response(
                method="GET",
                url=self.featured_snaps_api_url,
                json={},
                status=200,
            )
        )

        response = self.client.get(self.endpoint_url)

        self.assert200(response)
        self.assert_context("snap_title", "Snap Title")
