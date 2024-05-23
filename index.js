const { Client, Events, GatewayIntentBits } = require('discord.js');
const { spawn } = require('child_process');
const { token } = require('./config.json');

// Create a new client instance
const client = new Client({ intents: [GatewayIntentBits.Guilds] });

// When the client is ready, run this code (only once).
client.once(Events.ClientReady, readyClient => {
    console.log(`Ready! Logged in as ${readyClient.user.tag}`);
    
    // Execute test.py using Python
    const pythonProcess = spawn('python', ['test.py']);
    
    // Log any output from the Python process
    pythonProcess.stdout.on('data', (data) => {
        console.log(`test.py stdout: ${data}`);
    });
    
    pythonProcess.stderr.on('data', (data) => {
        console.error(`test.py stderr: ${data}`);
    });
});

// Log in to Discord with your client's token
client.login(token);
