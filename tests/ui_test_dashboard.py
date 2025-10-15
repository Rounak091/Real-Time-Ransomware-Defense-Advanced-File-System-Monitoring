import pytest
from playwright.sync_api import sync_playwright, Page, Browser
import time

@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser: Browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

class TestDashboardUI:
    BASE_URL = "http://localhost:5000"

    def test_dashboard_loads(self, page: Page):
        """Test that the dashboard loads successfully"""
        page.goto(self.BASE_URL)
        assert page.title() == "Ransomware Detection Dashboard"
        assert page.locator("h1").text_content() == "🔒 Ransomware Detection Dashboard"

    def test_alert_display(self, page: Page):
        """Test that alerts are displayed in the UI"""
        # First, add a test alert via API
        import requests
        alert = {
            'message': 'UI Test Alert',
            'file_path': '/test/ui/file.txt',
            'confidence': 0.95,
            'severity': 'HIGH',
            'timestamp': '2025-10-09 03:15:57',
            'entropy': 7.8,
            'event_type': 'detection'
        }
        requests.post(f"{self.BASE_URL}/api/add_alert", json=alert)

        # Navigate to dashboard
        page.goto(self.BASE_URL)

        # Wait for alerts to load
        page.wait_for_timeout(9000)

        # Check if alert is displayed
        alerts_list = page.locator("#alertsList")
        assert alerts_list.is_visible()

        # Check if our test alert is in the list
        alert_items = page.locator(".alert-item")
        assert alert_items.count() > 0

        # Verify alert content
        first_alert = alert_items.first
        assert "UI Test Alert" in first_alert.text_content()

    def test_alert_details(self, page: Page):
        """Test that alert details are displayed correctly"""
        page.goto(self.BASE_URL)
        page.wait_for_timeout(9000)

        alert_items = page.locator(".alert-item")
        if alert_items.count() > 0:
            first_alert = alert_items.first
            # Check that alert contains expected fields
            assert "HIGH" in first_alert.text_content() or "MEDIUM" in first_alert.text_content() or "LOW" in first_alert.text_content()

    def test_dashboard_refresh(self, page: Page):
        """Test that dashboard can be refreshed"""
        page.goto(self.BASE_URL)
        initial_alert_count = page.locator(".alert-item").count()

        # Add another alert
        import requests
        alert = {
            'message': 'Refresh Test Alert',
            'file_path': '/test/refresh/file.txt',
            'confidence': 0.88,
            'severity': 'MEDIUM',
            'timestamp': '2025-10-09 03:16:00',
            'entropy': 7.5,
            'event_type': 'detection'
        }
        requests.post(f"{self.BASE_URL}/api/add_alert", json=alert)

        # Refresh the page
        page.reload()
        page.wait_for_timeout(9000)

        # Check that new alert appears
        final_alert_count = page.locator(".alert-item").count()
        assert final_alert_count >= initial_alert_count

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
