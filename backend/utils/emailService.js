const nodemailer = require('nodemailer');
require('dotenv').config();

// Create email transporter
const createTransporter = () => {
    // For development, use ethereal.email (fake SMTP service)
    // For production, use your actual email service (Gmail, SendGrid, etc.)
    
    if (process.env.EMAIL_HOST && process.env.EMAIL_USER && process.env.EMAIL_PASS) {
        // Production email configuration
        return nodemailer.createTransporter({
            host: process.env.EMAIL_HOST,
            port: process.env.EMAIL_PORT || 587,
            secure: false,
            auth: {
                user: process.env.EMAIL_USER,
                pass: process.env.EMAIL_PASS
            }
        });
    } else {
        // Development: Log to console instead of sending real emails
        console.log('⚠️  Email service not configured. Using console logging for development.');
        return null;
    }
};

// Send verification email
const sendVerificationEmail = async (email, verificationToken) => {
    const transporter = createTransporter();
    
    const verificationUrl = `${process.env.FRONTEND_URL || 'http://localhost:3000'}/verify-email.html?token=${verificationToken}`;
    
    const mailOptions = {
        from: process.env.EMAIL_FROM || 'SIGIRI <noreply@sigiri.com>',
        to: email,
        subject: 'Verify Your Email - SIGIRI',
        html: `
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                    .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
                    .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
                    .button { display: inline-block; padding: 12px 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }
                    .footer { text-align: center; margin-top: 20px; color: #666; font-size: 12px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Welcome to SIGIRI! 🎉</h1>
                    </div>
                    <div class="content">
                        <h2>Verify Your Email Address</h2>
                        <p>Thank you for registering with SIGIRI! To complete your registration, please verify your email address by clicking the button below:</p>
                        <center>
                            <a href="${verificationUrl}" class="button">Verify Email Address</a>
                        </center>
                        <p>Or copy and paste this link into your browser:</p>
                        <p style="word-break: break-all; color: #667eea;">${verificationUrl}</p>
                        <p>This link will expire in 24 hours.</p>
                        <p>If you didn't create an account with SIGIRI, please ignore this email.</p>
                    </div>
                    <div class="footer">
                        <p>© 2025 SIGIRI - Free Online File Converter</p>
                    </div>
                </div>
            </body>
            </html>
        `
    };
    
    if (transporter) {
        try {
            await transporter.sendMail(mailOptions);
            console.log(`✅ Verification email sent to ${email}`);
        } catch (error) {
            console.error('❌ Error sending verification email:', error);
        }
    } else {
        // Development mode: log email details
        console.log('\n📧 VERIFICATION EMAIL (Development Mode):');
        console.log('To:', email);
        console.log('Verification URL:', verificationUrl);
        console.log('Token:', verificationToken);
        console.log('\n');
    }
};

// Send password reset email
const sendPasswordResetEmail = async (email, resetToken) => {
    const transporter = createTransporter();
    
    const resetUrl = `${process.env.FRONTEND_URL || 'http://localhost:3000'}/reset-password.html?token=${resetToken}`;
    
    const mailOptions = {
        from: process.env.EMAIL_FROM || 'SIGIRI <noreply@sigiri.com>',
        to: email,
        subject: 'Reset Your Password - SIGIRI',
        html: `
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                    .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
                    .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
                    .button { display: inline-block; padding: 12px 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }
                    .footer { text-align: center; margin-top: 20px; color: #666; font-size: 12px; }
                    .warning { background: #fff3cd; border: 1px solid #ffc107; padding: 15px; border-radius: 5px; margin: 15px 0; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Password Reset Request 🔐</h1>
                    </div>
                    <div class="content">
                        <h2>Reset Your Password</h2>
                        <p>We received a request to reset your password for your SIGIRI account. Click the button below to reset your password:</p>
                        <center>
                            <a href="${resetUrl}" class="button">Reset Password</a>
                        </center>
                        <p>Or copy and paste this link into your browser:</p>
                        <p style="word-break: break-all; color: #667eea;">${resetUrl}</p>
                        <div class="warning">
                            <strong>⚠️ Security Note:</strong>
                            <ul>
                                <li>This link will expire in 1 hour</li>
                                <li>If you didn't request this, please ignore this email</li>
                                <li>Your password won't change until you create a new one</li>
                            </ul>
                        </div>
                    </div>
                    <div class="footer">
                        <p>© 2025 SIGIRI - Free Online File Converter</p>
                    </div>
                </div>
            </body>
            </html>
        `
    };
    
    if (transporter) {
        try {
            await transporter.sendMail(mailOptions);
            console.log(`✅ Password reset email sent to ${email}`);
        } catch (error) {
            console.error('❌ Error sending password reset email:', error);
        }
    } else {
        // Development mode: log email details
        console.log('\n📧 PASSWORD RESET EMAIL (Development Mode):');
        console.log('To:', email);
        console.log('Reset URL:', resetUrl);
        console.log('Token:', resetToken);
        console.log('\n');
    }
};

module.exports = {
    sendVerificationEmail,
    sendPasswordResetEmail
};
