# TODO: Display All Alerts in Scrollable Format

## Issues Identified
- Alerts section limited to last 10 alerts.
- No scrolling for more alerts.

## Plan
- [x] Edit dashboard/static/dashboard.js to show all alerts
- [x] Edit dashboard/templates/index.html to add scrollable CSS
- [ ] Test the changes

## Progress
- [x] Analyzed dashboard.js and index.html
- [x] Created plan and got approval
- [x] Modified dashboard.js to remove limit and show all alerts (newest first)
- [x] Modified index.html to add max-height and overflow-y: auto for scrolling
