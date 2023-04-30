const dotenv = require('dotenv');
const { Client, Events, GatewayIntentBits } = require('discord.js');
const axios = require('axios');
const FormData = require('form-data');

dotenv.config();
const TOKEN = process.env.TOKEN;
const CHANNELS = process.env.CHANNELS.split(',');

const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages,
                                      GatewayIntentBits.MessageContent] });

client.once(Events.ClientReady, c => {
        console.log(`Ready! Logged in as ${c.user.tag}`);
});

client.on('messageCreate', async (message) => {
    if (message.author.bot || !message.attachments.size) return;

    const mentioned = message.mentions.users.has(client.user.id);
    const food_channel = CHANNELS.includes(message.channel.id);

    if (!mentioned && !food_channel) return;

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
        const result = await axios.post('http://classifier:8000/predict', formData, {
            headers: {
                'Content-Type': `multipart/form-data; boundary=${formData._boundary}`,
            },
        });

        if (result.data.class == 'bread') {
            message.reply(`This image is bread!\n\n` +
                          `Bread Confidence:\t${result.data.bread_confidence}\n` +
                          `Not-Bread Confidence:\t${result.data.not_bread_confidence}`);
        } else {
            message.reply(`This image is not bread!\n\n` +
                          `Bread Confidence:\t${result.data.bread_confidence}\n` +
                          `Not-Bread Confidence:\t${result.data.not_bread_confidence}`);
        }
    } catch (error) {
        console.error(error);
        message.reply('An error occurred while processing the image.');
    }
});

client.login(TOKEN);
