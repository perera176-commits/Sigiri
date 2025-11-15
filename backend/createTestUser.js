const mongoose = require('mongoose');
require('dotenv').config();

// MongoDB connection
const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/sigiri';

// User Schema
const userSchema = new mongoose.Schema({
    email: String,
    password: String,
    loginMethod: String,
    userName: String,
    createdAt: { type: Date, default: Date.now },
    lastLogin: Date
});

const User = mongoose.model('User', userSchema);

// Create test user
async function createTestUser() {
    try {
        await mongoose.connect(MONGO_URI, {
            useNewUrlParser: true,
            useUnifiedTopology: true,
        });
        
        console.log('✅ Connected to MongoDB\n');
        
        // Check if user already exists
        const existingUser = await User.findOne({ email: 'test@sigiri.com' });
        
        if (existingUser) {
            console.log('⚠️  User already exists!');
            console.log('\n📧 Email:', existingUser.email);
            console.log('🆔 User ID:', existingUser._id);
            console.log('📅 Created:', existingUser.createdAt.toLocaleString());
            console.log('\n💡 User already in database. No action needed.');
        } else {
            // Create new user
            const newUser = new User({
                email: 'test@sigiri.com',
                password: '123', // Note: In production, passwords should be hashed!
                loginMethod: 'email',
                userName: 'Test User',
                createdAt: new Date(),
                lastLogin: null
            });
            
            await newUser.save();
            
            console.log('✅ Test user created successfully!\n');
            console.log('=' .repeat(60));
            console.log('📧 Email: test@sigiri.com');
            console.log('🔐 Password: 123');
            console.log('👤 Name: Test User');
            console.log('🔐 Login Method: email');
            console.log('🆔 User ID:', newUser._id);
            console.log('📅 Created:', newUser.createdAt.toLocaleString());
            console.log('=' .repeat(60));
            console.log('\n💡 You can now login with these credentials!');
        }
        
    } catch (error) {
        console.error('❌ Error:', error.message);
    } finally {
        await mongoose.connection.close();
        console.log('\n✅ Database connection closed');
    }
}

// Run the script
createTestUser();
