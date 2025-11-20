const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
require('dotenv').config();

// User Schema (same as in models/User.js)
const userSchema = new mongoose.Schema({
  email: { type: String, required: true, unique: true, lowercase: true },
  password: { type: String, required: true },
  userName: { type: String, required: true },
  isVerified: { type: Boolean, default: false },
  verificationToken: String,
  resetPasswordToken: String,
  resetPasswordExpires: Date,
  createdAt: { type: Date, default: Date.now },
  lastLogin: Date
});

const User = mongoose.model('User', userSchema);

async function createTestUser() {
  try {
    // Connect to MongoDB
    const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/sigiri';
    console.log('🔄 Connecting to MongoDB...');
    await mongoose.connect(MONGO_URI, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    console.log('✅ Connected to MongoDB');

    // Check if user already exists
    const existingUser = await User.findOne({ email: 'test@sigiri.com' });
    if (existingUser) {
      console.log('⚠️  User test@sigiri.com already exists!');
      console.log('   Deleting old user and creating new one...');
      await User.deleteOne({ email: 'test@sigiri.com' });
    }

    // Hash password
    const hashedPassword = await bcrypt.hash('654321', 10);

    // Create new user
    const testUser = new User({
      email: 'test@sigiri.com',
      password: hashedPassword,
      userName: 'Test User',
      isVerified: true, // Auto-verify for testing
      createdAt: new Date()
    });

    await testUser.save();
    console.log('✅ Test user created successfully!');
    console.log('');
    console.log('📋 User Details:');
    console.log('   Email: test@sigiri.com');
    console.log('   Password: 654321');
    console.log('   Verified: Yes');
    console.log('   Username: Test User');
    console.log('');
    console.log('🎉 You can now login at https://sigiri.io/login.html');

  } catch (error) {
    console.error('❌ Error creating test user:', error.message);
  } finally {
    await mongoose.connection.close();
    console.log('🔌 MongoDB connection closed');
    process.exit(0);
  }
}

createTestUser();
