const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken');
const User = require('../models/User');
const { sendVerificationEmail, sendPasswordResetEmail } = require('../utils/emailService');

// JWT Secret
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-this-in-production';

// @route   POST /api/auth/register
// @desc    Register a new user
// @access  Public
router.post('/register', async (req, res) => {
    try {
        const { email, password, userName } = req.body;

        // Validation
        if (!email || !password) {
            return res.status(400).json({ 
                success: false, 
                message: 'Please provide email and password' 
            });
        }

        if (password.length < 6) {
            return res.status(400).json({ 
                success: false, 
                message: 'Password must be at least 6 characters' 
            });
        }

        // Check if user already exists
        const existingUser = await User.findOne({ email });
        if (existingUser) {
            return res.status(400).json({ 
                success: false, 
                message: 'Email already registered' 
            });
        }

        // Create new user
        const user = new User({
            email,
            password,
            userName: userName || email.split('@')[0],
            loginMethod: 'email'
        });

        // Generate verification token
        const verificationToken = user.generateVerificationToken();
        await user.save();

        // Send verification email
        await sendVerificationEmail(user.email, verificationToken);

        res.status(201).json({
            success: true,
            message: 'Registration successful! Please check your email to verify your account.',
            userId: user._id
        });

    } catch (error) {
        console.error('Register error:', error);
        res.status(500).json({ 
            success: false, 
            message: 'Server error during registration' 
        });
    }
});

// @route   POST /api/auth/login
// @desc    Login user
// @access  Public
router.post('/login', async (req, res) => {
    try {
        const { email, password } = req.body;

        // Validation
        if (!email || !password) {
            return res.status(400).json({ 
                success: false, 
                message: 'Please provide email and password' 
            });
        }

        // Check if user exists
        const user = await User.findOne({ email });
        if (!user) {
            return res.status(401).json({ 
                success: false, 
                message: 'Invalid email or password' 
            });
        }

        // Check if email is verified (TEMPORARILY DISABLED FOR TESTING)
        // if (!user.isVerified) {
        //     return res.status(403).json({ 
        //         success: false, 
        //         message: 'Please verify your email before logging in',
        //         needsVerification: true
        //     });
        // }

        // Verify password
        const isMatch = await user.comparePassword(password);
        if (!isMatch) {
            return res.status(401).json({ 
                success: false, 
                message: 'Invalid email or password' 
            });
        }

        // Update last login
        user.lastLogin = new Date();
        await user.save();

        // Generate JWT token
        const token = jwt.sign(
            { userId: user._id, email: user.email },
            JWT_SECRET,
            { expiresIn: '7d' }
        );

        res.json({
            success: true,
            message: 'Login successful!',
            token,
            user: {
                id: user._id,
                email: user.email,
                userName: user.userName,
                loginMethod: user.loginMethod
            }
        });

    } catch (error) {
        console.error('Login error:', error);
        res.status(500).json({ 
            success: false, 
            message: 'Server error during login' 
        });
    }
});

// @route   GET /api/auth/verify-email/:token
// @desc    Verify user email
// @access  Public
router.get('/verify-email/:token', async (req, res) => {
    try {
        const { token } = req.params;

        // Find user with this verification token
        const user = await User.findOne({ verificationToken: token });
        
        if (!user) {
            return res.status(400).json({ 
                success: false, 
                message: 'Invalid or expired verification token' 
            });
        }

        // Mark user as verified
        user.isVerified = true;
        user.verificationToken = null;
        await user.save();

        res.json({
            success: true,
            message: 'Email verified successfully! You can now login.'
        });

    } catch (error) {
        console.error('Verify email error:', error);
        res.status(500).json({ 
            success: false, 
            message: 'Server error during verification' 
        });
    }
});

// @route   POST /api/auth/resend-verification
// @desc    Resend verification email
// @access  Public
router.post('/resend-verification', async (req, res) => {
    try {
        const { email } = req.body;

        const user = await User.findOne({ email });
        if (!user) {
            return res.status(404).json({ 
                success: false, 
                message: 'User not found' 
            });
        }

        if (user.isVerified) {
            return res.status(400).json({ 
                success: false, 
                message: 'Email is already verified' 
            });
        }

        // Generate new verification token
        const verificationToken = user.generateVerificationToken();
        await user.save();

        // Send verification email
        await sendVerificationEmail(user.email, verificationToken);

        res.json({
            success: true,
            message: 'Verification email sent! Please check your inbox.'
        });

    } catch (error) {
        console.error('Resend verification error:', error);
        res.status(500).json({ 
            success: false, 
            message: 'Server error' 
        });
    }
});

// @route   POST /api/auth/forgot-password
// @desc    Send password reset email
// @access  Public
router.post('/forgot-password', async (req, res) => {
    try {
        const { email } = req.body;

        const user = await User.findOne({ email });
        if (!user) {
            // Don't reveal if email exists
            return res.json({
                success: true,
                message: 'If the email exists, a password reset link has been sent.'
            });
        }

        // Generate reset token
        const resetToken = user.generateResetToken();
        await user.save();

        // Send password reset email
        await sendPasswordResetEmail(user.email, resetToken);

        res.json({
            success: true,
            message: 'Password reset link has been sent to your email.'
        });

    } catch (error) {
        console.error('Forgot password error:', error);
        res.status(500).json({ 
            success: false, 
            message: 'Server error' 
        });
    }
});

// @route   POST /api/auth/reset-password/:token
// @desc    Reset password
// @access  Public
router.post('/reset-password/:token', async (req, res) => {
    try {
        const { token } = req.params;
        const { password } = req.body;

        if (!password || password.length < 6) {
            return res.status(400).json({ 
                success: false, 
                message: 'Password must be at least 6 characters' 
            });
        }

        // Find user with valid reset token
        const user = await User.findOne({
            resetPasswordToken: token,
            resetPasswordExpires: { $gt: Date.now() }
        });

        if (!user) {
            return res.status(400).json({ 
                success: false, 
                message: 'Invalid or expired reset token' 
            });
        }

        // Update password
        user.password = password;
        user.resetPasswordToken = null;
        user.resetPasswordExpires = null;
        await user.save();

        res.json({
            success: true,
            message: 'Password reset successful! You can now login with your new password.'
        });

    } catch (error) {
        console.error('Reset password error:', error);
        res.status(500).json({ 
            success: false, 
            message: 'Server error' 
        });
    }
});

// @route   POST /api/auth/create-test-user
// @desc    Create a test user (for development/testing only)
// @access  Public (should be protected in production!)
router.post('/create-test-user', async (req, res) => {
    try {
        const { email, password, userName } = req.body;

        // Default values
        const testEmail = email || 'test@sigiri.com';
        const testPassword = password || '654321';
        const testUserName = userName || 'Test User';

        // Check if user already exists
        const existingUser = await User.findOne({ email: testEmail });
        if (existingUser) {
            // Delete and recreate
            await User.deleteOne({ email: testEmail });
        }

        // Create new user with hashed password
        const user = new User({
            email: testEmail,
            password: testPassword, // Will be hashed by the pre-save hook
            userName: testUserName,
            isVerified: true // Auto-verify for testing
        });

        await user.save();

        res.json({
            success: true,
            message: 'Test user created successfully',
            user: {
                email: testEmail,
                password: testPassword, // Only showing this for testing
                userName: testUserName,
                isVerified: true
            }
        });

    } catch (error) {
        console.error('Create test user error:', error);
        res.status(500).json({
            success: false,
            message: 'Error creating test user',
            error: error.message
        });
    }
});

module.exports = router;
