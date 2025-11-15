const mongoose = require('mongoose');
require('dotenv').config();

// MongoDB connection
const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/sigiri';

// User Schema (matching your login system)
const userSchema = new mongoose.Schema({
    email: String,
    password: String,
    loginMethod: String,
    userName: String,
    createdAt: { type: Date, default: Date.now },
    lastLogin: Date
});

const User = mongoose.model('User', userSchema);

// Connect and fetch all users
async function viewAllUsers() {
    try {
        await mongoose.connect(MONGO_URI, {
            useNewUrlParser: true,
            useUnifiedTopology: true,
        });
        
        console.log('✅ Connected to MongoDB\n');
        
        // Get all users
        const users = await User.find({});
        
        if (users.length === 0) {
            console.log('📭 No users found in database');
        } else {
            console.log(`👥 Total Users: ${users.length}\n`);
            console.log('=' .repeat(80));
            
            users.forEach((user, index) => {
                console.log(`\n${index + 1}. User Account:`);
                console.log('   -'.repeat(40));
                console.log(`   📧 Email: ${user.email || 'N/A'}`);
                console.log(`   👤 Name: ${user.userName || 'N/A'}`);
                console.log(`   🔐 Login Method: ${user.loginMethod || 'N/A'}`);
                console.log(`   🆔 User ID: ${user._id}`);
                console.log(`   📅 Created: ${user.createdAt ? user.createdAt.toLocaleString() : 'N/A'}`);
                console.log(`   🕐 Last Login: ${user.lastLogin ? user.lastLogin.toLocaleString() : 'N/A'}`);
                console.log('   -'.repeat(40));
            });
            
            console.log('\n' + '='.repeat(80));
            
            // Show summary by login method
            const loginMethods = users.reduce((acc, user) => {
                const method = user.loginMethod || 'Unknown';
                acc[method] = (acc[method] || 0) + 1;
                return acc;
            }, {});
            
            console.log('\n📊 Summary by Login Method:');
            Object.entries(loginMethods).forEach(([method, count]) => {
                console.log(`   • ${method}: ${count} user(s)`);
            });
        }
        
    } catch (error) {
        console.error('❌ Error:', error.message);
    } finally {
        await mongoose.connection.close();
        console.log('\n✅ Database connection closed');
    }
}

// Run the script
viewAllUsers();
