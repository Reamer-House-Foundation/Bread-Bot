const dotenv = require('dotenv');
const { Client, Events, GatewayIntentBits } = require('discord.js');
const axios = require('axios');
const FormData = require('form-data');

dotenv.config();
const TOKEN = process.env.TOKEN;

const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages] });

client.once(Events.ClientReady, c => {
        console.log(`Ready! Logged in as ${c.user.tag}`);
});

client.on('messageCreate', async (message) => {
    if (message.author.bot || !message.attachments.size) return;

    const mentioned = message.mentions.users.has(client.user.id);
    if (!mentioned) return;

    const imageUrl = message.attachments.first().url;

    try {
        // Get the first image attachment
        const attachment = message.attachments.first();
        
        // Download the image and convert it to a Buffer
        const response = await axios.get(attachment.url, { responseType: 'arraybuffer' });
        const imageBuffer = Buffer.from(response.data, 'binary');
        
        // Create a FormData object and append the image
        const formData = new FormData();
        formData.append('image', imageBuffer, attachment.name);
        

        // TODO: Make this settable using env variables
        // Send a POST request with the image using axios
        const result = await axios.post('http://web:8000/predict', formData, {
            headers: {
                'Content-Type': `multipart/form-data; boundary=${formData._boundary}`,
            },
        });
        
        if (result.data.class == 'bread') {
            message.reply('This image is bread!');
        } else {
            message.reply('This image is not bread!');
        }
    } catch (error) {
        console.error(error);
        message.reply('An error occurred while processing the image.');
    }
});

client.login(TOKEN);
