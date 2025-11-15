const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 8080;
const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/sigiri';

// Middleware
app.use(cors({
  origin: [
    'https://sigiri.io',
    'http://sigiri.io',
    'https://www.sigiri.io',
    'http://localhost:3000',
    'http://localhost:8080'
  ],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// MongoDB Connection
mongoose.connect(MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
  .then(() => console.log('✅ Connected to MongoDB'))
  .catch((err) => console.error('❌ MongoDB connection error:', err));

// Routes
app.get('/', (req, res) => {
  res.json({ 
    message: 'SIGIRI Backend API',
    status: 'running',
    endpoints: {
      auth: '/api/auth',
      register: 'POST /api/auth/register',
      login: 'POST /api/auth/login',
      verifyEmail: 'GET /api/auth/verify-email/:token',
      forgotPassword: 'POST /api/auth/forgot-password',
      resetPassword: 'POST /api/auth/reset-password/:token'
    }
  });
});

// Auth routes
const authRoutes = require('./routes/auth');
app.use('/api/auth', authRoutes);

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Error:', err);
  res.status(500).json({ 
    success: false, 
    message: 'Internal server error' 
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Server is running on port ${PORT}`);
  console.log(`📡 API available at http://localhost:${PORT}`);
});
