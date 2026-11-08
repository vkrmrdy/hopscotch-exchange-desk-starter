import os
import unittest
from unittest.mock import patch

from desk.gate import gate
from desk.graph import build_graph
from desk.tools import TOOLS, check_pickup, get_order, get_vendor_return_rate


class GateTests(unittest.TestCase):
    def test_rejects_short_messages(self):
        self.assertEqual(gate("hi"), "too short")

    def test_rejects_links(self):
        self.assertEqual(
            gate("Order HS2291 is too small, see https://example.com and exchange it"),
            "contains link",
        )

    def test_rejects_off_topic_messages(self):
        self.assertEqual(
            gate("Do you have any Diwali offers on party wear this week?"), "off-topic"
        )

    def test_accepts_exchange_requests_without_an_order_id(self):
        self.assertEqual(
            gate("The kurta I ordered is too small, please exchange it."), "accepted"
        )


class DemoToolTests(unittest.TestCase):
    def test_order_lookup(self):
        result = get_order.invoke({"order_id": "HS2291"})
        self.assertEqual(result["order_id"], "HS2291")
        self.assertEqual(result["days_since_delivery"], 4)

    def test_vendor_return_rate(self):
        result = get_vendor_return_rate.invoke({"vendor_id": "V5"})
        self.assertEqual(result["return_rate"], 28.0)

    def test_pickup_availability(self):
        response = unittest.mock.Mock()
        response.json.return_value = [
            {"Status": "Success", "PostOffice": [{"DeliveryStatus": "Delivery"}]}
        ]
        with patch("desk.tools.requests.get", return_value=response):
            result = check_pickup.invoke({"pincode": "122002"})
        self.assertIs(result["serviceable"], True)


class GraphTests(unittest.TestCase):
    def test_graph_compiles_with_configured_credentials(self):
        with patch.dict(os.environ, {"OPENROUTER_API_KEY": "test-key"}):
            app = build_graph(TOOLS)
        self.assertIn("investigator", app.get_graph().nodes)


if __name__ == "__main__":
    unittest.main()
