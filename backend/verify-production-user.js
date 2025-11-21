const mongoose = require('mongoose');
require('dotenv').config();

// MongoDB connection
const MONGO_URI = process.env.MONGO_URI;

// User Schema
const userSchema = new mongoose.Schema({
    email: String,
    password: String,
    userName: String,
    loginMethod: String,
    isVerified: Boolean,
    verificationToken: String,
    resetPasswordToken: String,
    resetPasswordExpires: Date,
    createdAt: Date,
    lastLogin: Date
});

const User = mongoose.model('User', userSchema);

// Verify users
async function verifyUsers() {
    try {
        await mongoose.connect(MONGO_URI, {
            useNewUrlParser: true,
            useUnifiedTopology: true,
        });
        
        console.log('✅ Connected to MongoDB\n');
        
        // List of emails to verify
        const emailsToVerify = ['demo@sigiri.com', 'test@sigiri.com'];
        
        for (const email of emailsToVerify) {
            const user = await User.findOne({ email });
            
            if (user) {
                user.isVerified = true;
                user.verificationToken = null;
                await user.save();
                console.log(`✅ Verified: ${email}`);
            } else {
                console.log(`❌ Not found: ${email}`);
            }
        }
        
        console.log('\n📋 All users in database:');
        const allUsers = await User.find({});
        allUsers.forEach(user => {
            console.log(`  • ${user.email} - Verified: ${user.isVerified}`);
        });
        
    } catch (error) {
        console.error('❌ Error:', error.message);
    } finally {
        await mongoose.connection.close();
        console.log('\n✅ Database connection closed');
    }
}

// Run the script
verifyUsers();
