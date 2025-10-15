import unittest
import requests
import time

class TestDashboardIntegration(unittest.TestCase):
    BASE_URL = "http://localhost:5000"

    def test_alert_flow(self):
        # Step 1: Send a test alert to the API
        alert = {
            'message': 'Integration test alert',
            'file_path': '/test/integration/file.txt',
            'confidence': 0.99,
            'severity': 'HIGH',
            'timestamp': '2025-10-09 03:15:57',
            'entropy': 7.9,
            'event_type': 'detection'
        }
        response = requests.post(f"{self.BASE_URL}/api/add_alert", json=alert)
        self.assertEqual(response.status_code, 200, "Failed to add alert")

        # Step 2: Wait briefly to allow alert processing
        time.sleep(1)

        # Step 3: Fetch alerts from the API
        response = requests.get(f"{self.BASE_URL}/api/alerts")
        self.assertEqual(response.status_code, 200, "Failed to fetch alerts")
        alerts = response.json()
        self.assertTrue(any(a['message'] == alert['message'] for a in alerts), "Alert not found in API response")

        # Step 4: (Optional) Further UI testing would require browser automation tools

if __name__ == "__main__":
    unittest.main()
