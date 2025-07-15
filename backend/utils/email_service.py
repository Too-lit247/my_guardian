"""
Email service using Brevo (SendinBlue) API
"""
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        # Configure API key authorization
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = getattr(settings, 'BREVO_API_KEY', '')
        self.api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
        
    def send_welcome_email(self, user_email, user_name, password):
        """
        Send welcome email to new field officer with login credentials
        """
        try:
            # Email content
            subject = "Welcome to MyGuardian+ - Your Account Has Been Created"
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Welcome to MyGuardian+</title>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #2563eb; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
                    .content {{ background-color: #f8fafc; padding: 30px; border-radius: 0 0 8px 8px; }}
                    .credentials {{ background-color: #e0f2fe; padding: 20px; border-radius: 8px; margin: 20px 0; }}
                    .button {{ display: inline-block; background-color: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; margin: 20px 0; }}
                    .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
                    .warning {{ background-color: #fef3c7; padding: 15px; border-radius: 6px; margin: 20px 0; border-left: 4px solid #f59e0b; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🛡️ Welcome to MyGuardian+</h1>
                        <p>Emergency Response Management System</p>
                    </div>
                    
                    <div class="content">
                        <h2>Hello {user_name},</h2>
                        
                        <p>Your MyGuardian+ field officer account has been successfully created! You can now access the emergency response management system to coordinate and respond to alerts in your area.</p>
                        
                        <div class="credentials">
                            <h3>🔐 Your Login Credentials</h3>
                            <p><strong>Email:</strong> {user_email}</p>
                            <p><strong>Temporary Password:</strong> <code style="background-color: #fff; padding: 4px 8px; border-radius: 4px; font-family: monospace;">{password}</code></p>
                        </div>
                        
                        <div class="warning">
                            <h4>⚠️ Important Security Notice</h4>
                            <p>For your security, please change your password immediately after your first login. This temporary password should not be shared with anyone.</p>
                        </div>
                        
                        <a href="http://localhost:3000" class="button">Access MyGuardian+ Dashboard</a>
                        
                        <h3>🚀 Getting Started</h3>
                        <ol>
                            <li>Click the link above to access the MyGuardian+ dashboard</li>
                            <li>Log in using your email and temporary password</li>
                            <li>Change your password in your profile settings</li>
                            <li>Complete your profile information</li>
                            <li>Start monitoring and responding to emergency alerts</li>
                        </ol>
                        
                        <h3>📱 Key Features</h3>
                        <ul>
                            <li><strong>Real-time Alerts:</strong> Receive and respond to emergency alerts instantly</li>
                            <li><strong>Location Tracking:</strong> View alert locations and navigate efficiently</li>
                            <li><strong>Status Updates:</strong> Update alert status and provide real-time feedback</li>
                            <li><strong>Communication:</strong> Coordinate with your team and station manager</li>
                            <li><strong>History:</strong> Access your response history and performance metrics</li>
                        </ul>
                        
                        <p>If you have any questions or need assistance, please contact your station manager or system administrator.</p>
                        
                        <p>Welcome to the team!</p>
                        
                        <p><strong>The MyGuardian+ Team</strong></p>
                    </div>
                    
                    <div class="footer">
                        <p>This is an automated message from MyGuardian+ Emergency Response System.</p>
                        <p>Please do not reply to this email.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Plain text version
            text_content = f"""
            Welcome to MyGuardian+ - Emergency Response Management System
            
            Hello {user_name},
            
            Your MyGuardian+ field officer account has been successfully created!
            
            LOGIN CREDENTIALS:
            Email: {user_email}
            Temporary Password: {password}
            
            IMPORTANT: Please change your password immediately after your first login.
            
            Access the dashboard at: http://localhost:3000
            
            Getting Started:
            1. Log in using your email and temporary password
            2. Change your password in your profile settings
            3. Complete your profile information
            4. Start monitoring and responding to emergency alerts
            
            If you have any questions, please contact your station manager or system administrator.
            
            Welcome to the team!
            The MyGuardian+ Team
            """
            
            # Create email object
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=[{"email": user_email, "name": user_name}],
                sender={
                    "email": getattr(settings, 'SENDER_EMAIL', 'thomhuwa066@gmail.com'),
                    "name": getattr(settings, 'SENDER_NAME', 'Skills Sync')
                },
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
            
            # Send email
            api_response = self.api_instance.send_transac_email(send_smtp_email)
            logger.info(f"Welcome email sent successfully to {user_email}. Message ID: {api_response.message_id}")
            return True, api_response.message_id
            
        except ApiException as e:
            logger.error(f"Failed to send welcome email to {user_email}: {e}")
            return False, str(e)
        except Exception as e:
            logger.error(f"Unexpected error sending welcome email to {user_email}: {e}")
            return False, str(e)
    
    def send_password_reset_email(self, user_email, user_name, reset_token):
        """
        Send password reset email
        """
        try:
            subject = "MyGuardian+ - Password Reset Request"
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Password Reset - MyGuardian+</title>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #dc2626; color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
                    .content {{ background-color: #f8fafc; padding: 30px; border-radius: 0 0 8px 8px; }}
                    .button {{ display: inline-block; background-color: #dc2626; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; margin: 20px 0; }}
                    .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
                    .warning {{ background-color: #fef3c7; padding: 15px; border-radius: 6px; margin: 20px 0; border-left: 4px solid #f59e0b; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🔒 Password Reset Request</h1>
                        <p>MyGuardian+ Emergency Response System</p>
                    </div>
                    
                    <div class="content">
                        <h2>Hello {user_name},</h2>
                        
                        <p>We received a request to reset your MyGuardian+ account password. If you made this request, click the button below to reset your password:</p>
                        
                        <a href="http://localhost:3000/reset-password?token={reset_token}" class="button">Reset Password</a>
                        
                        <div class="warning">
                            <h4>⚠️ Security Notice</h4>
                            <p>If you did not request this password reset, please ignore this email. Your password will remain unchanged.</p>
                            <p>This reset link will expire in 24 hours for security reasons.</p>
                        </div>
                        
                        <p>If you're having trouble clicking the button, copy and paste this link into your browser:</p>
                        <p style="word-break: break-all; background-color: #e5e7eb; padding: 10px; border-radius: 4px;">
                            http://localhost:3000/reset-password?token={reset_token}
                        </p>
                        
                        <p>If you continue to have issues, please contact your system administrator.</p>
                        
                        <p><strong>The MyGuardian+ Team</strong></p>
                    </div>
                    
                    <div class="footer">
                        <p>This is an automated message from MyGuardian+ Emergency Response System.</p>
                        <p>Please do not reply to this email.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            text_content = f"""
            Password Reset Request - MyGuardian+
            
            Hello {user_name},
            
            We received a request to reset your MyGuardian+ account password.
            
            Reset your password by visiting this link:
            http://localhost:3000/reset-password?token={reset_token}
            
            If you did not request this password reset, please ignore this email.
            This reset link will expire in 24 hours.
            
            The MyGuardian+ Team
            """
            
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=[{"email": user_email, "name": user_name}],
                sender={
                    "email": getattr(settings, 'SENDER_EMAIL', 'thomhuwa066@gmail.com'),
                    "name": getattr(settings, 'SENDER_NAME', 'Skills Sync')
                },
                subject=subject,
                html_content=html_content,
                text_content=text_content
            )
            
            api_response = self.api_instance.send_transac_email(send_smtp_email)
            logger.info(f"Password reset email sent successfully to {user_email}. Message ID: {api_response.message_id}")
            return True, api_response.message_id
            
        except ApiException as e:
            logger.error(f"Failed to send password reset email to {user_email}: {e}")
            return False, str(e)
        except Exception as e:
            logger.error(f"Unexpected error sending password reset email to {user_email}: {e}")
            return False, str(e)
