const { App } = require('@slack/bolt');
const fs = require('fs');
const path = require('path');

// Load env vars
require('dotenv').config({ path: path.join(__dirname, 'config.env') });

const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  signingSecret: process.env.SLACK_SIGNING_SECRET,
  socketMode: true,
  appToken: process.env.SLACK_APP_TOKEN,
  port: process.env.PORT || 3000
});

// Helper function for system-event-logger
function logEvent(eventType, description, status) {
  const timestamp = new Date().toISOString().replace('T', ' ').substring(0, 19);
  const logEntry = `[${timestamp}] [SlackBridge] [${eventType}] [${status}]: ${description}\n`;
  const diaryPath = path.join(__dirname, 'logs', 'diary.log');
  
  fs.appendFileSync(diaryPath, logEntry);
  
  if (status === 'ERROR' || status === 'WARNING') {
    const alertsPath = path.join(__dirname, 'logs', 'ALERTS.log');
    fs.appendFileSync(alertsPath, logEntry);
  }
}

// Listen for mentions
app.event('app_mention', async ({ event, context, client, say }) => {
  const text = event.text.replace(/<@.*>/, '').trim();
  const userId = event.user;

  console.log(`Received mention from ${userId}: ${text}`);

  if (text.toLowerCase() === 'ping!') {
    const response = `pong! 🏓 The current system time is ${new Date().toLocaleString()}.`;
    await say(response);
    logEvent('USER_REQUEST', `Received ping! from ${userId}`, 'SUCCESS');
    return;
  }

  // Create a new task file for anything else
  const timestamp = Date.now();
  const taskFilename = `slack_${timestamp}.md`;
  const taskPath = path.join(__dirname, 'tasks', taskFilename);
  const taskContent = `# Task: Slack Instruction from ${userId}\n\n## Goal\n${text}\n\n## Status\nPending\n`;

  try {
    fs.writeFileSync(taskPath, taskContent);
    await say(`Acknowledged, <@${userId}>. Task created: ${taskFilename}`);
    logEvent('USER_REQUEST', `Created task ${taskFilename} from ${userId} message: "${text}"`, 'SUCCESS');
  } catch (err) {
    console.error(`Failed to create task file: ${err.message}`);
    logEvent('SYSTEM_ERROR', `Failed to create task file for ${userId}: ${err.message}`, 'ERROR');
  }
});

(async () => {
  try {
    await app.start();
    console.log('⚡️ Rover Slack Bridge is running in Socket Mode!');
    logEvent('AGENT_START', 'SlackBridge agent started successfully', 'SUCCESS');
  } catch (err) {
    console.error(`Failed to start app: ${err.message}`);
    logEvent('AGENT_START', `Failed to start SlackBridge: ${err.message}`, 'ERROR');
  }
})();
