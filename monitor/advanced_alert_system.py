import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import logging
from datetime import datetime

class AdvancedAlertSystem:
    def __init__(self, config_file='config/alert_config.json'):
        self.config = self.load_config(config_file)
        self.setup_logging()
    
    def load_config(self, config_file):
        """Load alert configuration"""
        default_config = {
            "email": {
                "enabled": False,
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "sender_email": "",
                "sender_password": "",
                "recipient_emails": []
            },
            "webhook": {
                "enabled": False,
                "slack_webhook": "",
                "discord_webhook": ""
            },
            "sms": {
                "enabled": False,
                "twilio_sid": "",
                "twilio_token": "",
                "twilio_number": "",
                "recipient_numbers": []
            }
        }
        
        try:
            with open(config_file, 'r') as f:
                user_config = json.load(f)
                # Merge with default config
                for key in default_config:
                    if key in user_config:
                        default_config[key].update(user_config[key])
                return default_config
        except FileNotFoundError:
            print(f"Config file {config_file} not found. Using default config.")
            return default_config
    
    def setup_logging(self):
        """Setup logging for alert system"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/alert_system.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def send_alert(self, alert_data):
        """Send alert through all enabled channels"""
        self.logger.info(f"Sending alert: {alert_data['message']}")
        
        # Send via email
        if self.config['email']['enabled']:
            self.send_email_alert(alert_data)
        
        # Send via webhook
        if self.config['webhook']['enabled']:
            self.send_webhook_alert(alert_data)
        
        # Send via SMS
        if self.config['sms']['enabled']:
            self.send_sms_alert(alert_data)
    
    def send_email_alert(self, alert_data):
        """Send email alert"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config['email']['sender_email']
            msg['To'] = ', '.join(self.config['email']['recipient_emails'])
            msg['Subject'] = f"🚨 Ransomware Alert - {alert_data['severity'].upper()}"

            # Create email body
            body = f"""
            RANSOMWARE DETECTION ALERT

            Severity: {alert_data['severity'].upper()}
            Time: {alert_data['timestamp']}
            Message: {alert_data['message']}
            File: {alert_data['file_path']}
            Confidence: {alert_data['confidence']:.1%}

            Recommended Action: {alert_data.get('action', 'Investigate immediately')}

            --
            Ransomware Detection System
            Smart Home Security
            """

            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(self.config['email']['smtp_server'], self.config['email']['smtp_port'])
            server.starttls()
            server.login(self.config['email']['sender_email'], self.config['email']['sender_password'])
            text = msg.as_string()
            server.sendmail(self.config['email']['sender_email'], self.config['email']['recipient_emails'], text)
            server.quit()
            
            self.logger.info("Email alert sent successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to send email alert: {e}")
    
    def send_webhook_alert(self, alert_data):
        """Send alert to Slack/Discord webhook"""
        try:
            # Slack webhook
            if self.config['webhook']['slack_webhook']:
                slack_data = {
                    "text": f"🚨 Ransomware Detection Alert",
                    "blocks": [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": "🚨 Ransomware Detection Alert"
                            }
                        },
                        {
                            "type": "section",
                            "fields": [
                                {
                                    "type": "mrkdwn",
                                    "text": f"*Severity:*\n{alert_data['severity'].upper()}"
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": f"*Confidence:*\n{alert_data['confidence']:.1%}"
                                }
                            ]
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"*Message:* {alert_data['message']}\n*File:* `{alert_data['file_path']}`"
                            }
                        }
                    ]
                }
                
                response = requests.post(
                    self.config['webhook']['slack_webhook'],
                    json=slack_data,
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code == 200:
                    self.logger.info("Slack alert sent successfully")
                else:
                    self.logger.error(f"Slack webhook failed: {response.status_code}")
            
            # Discord webhook
            if self.config['webhook']['discord_webhook']:
                discord_data = {
                    "embeds": [{
                        "title": "🚨 Ransomware Detection Alert",
                        "color": 0xff0000 if alert_data['severity'] == 'high' else 0xffa500,
                        "fields": [
                            {
                                "name": "Severity",
                                "value": alert_data['severity'].upper(),
                                "inline": True
                            },
                            {
                                "name": "Confidence",
                                "value": f"{alert_data['confidence']:.1%}",
                                "inline": True
                            },
                            {
                                "name": "Message",
                                "value": alert_data['message']
                            },
                            {
                                "name": "File",
                                "value": f"`{alert_data['file_path']}`"
                            }
                        ],
                        "timestamp": alert_data['timestamp']
                    }]
                }
                
                response = requests.post(
                    self.config['webhook']['discord_webhook'],
                    json=discord_data,
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code == 204:
                    self.logger.info("Discord alert sent successfully")
                else:
                    self.logger.error(f"Discord webhook failed: {response.status_code}")
                    
        except Exception as e:
            self.logger.error(f"Webhook alert failed: {e}")
    
    def send_sms_alert(self, alert_data):
        """Send SMS alert via Twilio"""
        try:
            # This would require twilio package: pip install twilio
            # from twilio.rest import Client
            
            # client = Client(self.config['sms']['twilio_sid'], self.config['sms']['twilio_token'])
            
            # for number in self.config['sms']['recipient_numbers']:
            #     message = client.messages.create(
            #         body=f"🚨 RANSOMWARE ALERT: {alert_data['message']} - {alert_data['file_path']}",
            #         from_=self.config['sms']['twilio_number'],
            #         to=number
            #     )
            
            self.logger.info("SMS alert functionality ready (requires Twilio configuration)")
            
        except Exception as e:
            self.logger.error(f"SMS alert failed: {e}")

# Configuration file template
def create_alert_config():
    """Create a template configuration file"""
    config_template = {
        "email": {
            "enabled": True,
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender_email": "your_email@gmail.com",
            "sender_password": "your_app_password",
            "recipient_emails": ["admin@yourdomain.com"]
        },
        "webhook": {
            "enabled": True,
            "slack_webhook": "https://hooks.slack.com/services/XXX/XXX/XXX",
            "discord_webhook": "https://discord.com/api/webhooks/XXX/XXX"
        },
        "sms": {
            "enabled": False,
            "twilio_sid": "your_twilio_sid",
            "twilio_token": "your_twilio_token",
            "twilio_number": "+1234567890",
            "recipient_numbers": ["+1234567890"]
        }
    }
    
    with open('config/alert_config.json', 'w') as f:
        json.dump(config_template, f, indent=2)
    
    print("Alert configuration template created at config/alert_config.json")
    print("Please update with your actual credentials.")

if __name__ == "__main__":
    # Create config template
    create_alert_config()
    
    # Test the alert system
    alert_system = AdvancedAlertSystem()
    
    test_alert = {
        "severity": "high",
        "timestamp": datetime.now().isoformat(),
        "message": "Test ransomware pattern detected",
        "file_path": "/iot_test_files/test.encrypted",
        "confidence": 0.95,
        "action": "investigate"
    }
    
    alert_system.send_alert(test_alert)