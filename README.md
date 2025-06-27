# EventElf 🧙‍♂️

## About

EventElf was a project submitted to the [HackKnight 2025 hackathon](https://devpost.com/software/eventelf) (our first hackathon).
Adding events to your Google Calendar is tedious and annoying. You have to find the correct month, select the correct date, write the title, and select a time. What EventElf does is speeds up this process. Watch the demo to see it in action!

## Demo

[![Watch the demo](https://img.youtube.com/vi/93ZifA7hrtQ/0.jpg)](https://www.youtube.com/watch?v=93ZifA7hrtQ)

## How it Works

User types a message (ex: Schedule a team meeting tomorrow at 11am) and sends it. This message, along with today's date, gets sent to OpenAI API's gpt-4o-mini model for processing. Once processed, the program receives a structured output like {Title: "Team Meeting", Date: [tomorrow's date], Start Time: 11:00, End Time: 12:00, Reminder: 30} and prompts the user whether or not the information is correct. If it is, then the user can type "yes" and the structured outputs get sent as arguments to Google Calendar API, adding the event to the user's Google Calendar.

## 🧙‍♂️ Get Started

### 🚀 Clone This Repo
```bash
git clone https://github.com/your-username/eventelf.git
cd eventelf
```
### 🔑 Get Your OpenAI API Key

* Go to https://platform.openai.com/account/api-keys.

* Log in and generate a new API key.

* Save the key in config/config.py.

* If this is your first time, you can often receive free API credits just by signing up.

### 📆 Set Up Google Login (to Add Events to Google Calendar)

#### Sign in & pick a project
Visit https://console.cloud.google.com/ and log in.
Use the top-left Project dropdown to select your existing project, or click New Project → give it a name → Create.

#### Enable the Google Calendar API
In the left menu go to APIs & Services ▸ Library.
Search for Google Calendar API → click it → Enable.

#### Configure the OAuth consent screen
In the left menu, under APIs & Services, click OAuth consent screen.
Choose External (if your users have personal Google accounts) or Internal (if everyone is in your Google Workspace), then Create.
Fill in the App name, Support email, and any other required fields (e.g., Logo, Homepage URL).
Save and continue through the summary screens.

#### Create Desktop‑app OAuth client ID
Still under APIs & Services, go to Credentials → + CREATE CREDENTIALS → OAuth client ID.
For Application type, choose Desktop app, give it a name like “EventElf Desktop Client,” and click Create.

#### Download your OAuth client secret JSON
After creation, click Download JSON.
Rename the file to credentials.json and move it into the project’s config folder (You can delete example.credentials.json).

#### Add test users
Back in the OAuth consent screen, scroll to Test users.
Click Add users and enter each Google account email that you want to authorize (i.e., the email addresses that EventElf will use to add events).

