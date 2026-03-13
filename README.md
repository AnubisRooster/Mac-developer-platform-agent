# Claw Agent — Developer Automation Platform

## What Is This?

Claw Agent is a personal AI assistant that lives in your **Slack** workspace and can talk to your engineering tools for you. Instead of switching between GitHub, Jira, Jenkins, Gmail, and Confluence all day, you type a message in Slack and the agent handles it.

**Example — you type in Slack:**

> @claw summarize today's PRs

**What happens behind the scenes:**

1. Your message goes from Slack to the Claw Agent backend (a small server running on your Mac).
2. The backend asks **IronClaw** (a separate AI brain written in Rust) to figure out what to do.
3. IronClaw says "use the GitHub tool to fetch today's pull requests."
4. The backend calls GitHub, gets the data, and sends a summary back to your Slack channel.

You also get a **web dashboard** in your browser where you can see everything the agent is doing — events coming in, workflows running, tools being called, and full conversation history.

---

## How the Pieces Fit Together

Think of it like a restaurant:

| Piece | Restaurant Analogy | What It Actually Is |
|-------|-------------------|---------------------|
| **Slack** | The customer placing an order | Where you talk to the agent |
| **Python Backend** | The waiter taking your order to the kitchen | A server on your Mac that receives your messages and coordinates everything |
| **IronClaw** | The chef deciding how to prepare the dish | An AI engine (written in Rust) that reads your message and decides which tools to use |
| **Integrations** | The kitchen's ingredients and equipment | Connections to GitHub, Jira, Jenkins, Gmail, Confluence, and Slack |
| **PostgreSQL** | The restaurant's record book | A database that stores events, conversations, and workflow history |
| **Web Dashboard** | The kitchen's order display screen | A web page on your Mac showing what the agent is doing |

```
  You (in Slack)
       |
       v
  Python Backend (runs on your Mac, port 8080)
       |
       v
  IronClaw AI Engine (runs on your Mac, port 9090)
       |
       v
  Tools: GitHub, Jira, Jenkins, Gmail, Confluence, Slack
       |
       v
  PostgreSQL Database (stores everything)
       |
       v
  Web Dashboard (viewable at localhost:3000)
```

---

## What You'll Need to Install First

Before setting up Claw Agent, you need four programs on your Mac. If you already have any of these, you can skip that step.

### 1. Homebrew (a Mac package manager)

Homebrew is a tool that makes it easy to install other programs. Open **Terminal** (search for "Terminal" in Spotlight, or find it in Applications > Utilities) and paste this:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

It will ask for your Mac password (the one you use to log in). You won't see the characters as you type — that's normal. Press Enter when done and wait for it to finish.

### 2. Python (the programming language the backend uses)

```bash
brew install python@3.13
```

**Verify it worked** — type this and you should see a version number like `Python 3.13.x`:

```bash
python3 --version
```

### 3. Node.js (the runtime the web dashboard uses)

```bash
brew install node
```

**Verify it worked:**

```bash
node --version
```

You should see something like `v20.x.x` or higher.

### 4. PostgreSQL (the database)

```bash
brew install postgresql@15
brew services start postgresql@15
```

The second command starts the database in the background so it's always running.

**Verify it worked:**

```bash
psql --version
```

---

## Setting Up the Project

Now that the prerequisites are installed, let's set up Claw Agent itself. All commands below are typed into **Terminal**.

### Step 1: Create the Database

The agent needs a database to store events and conversations. Run these two commands one at a time:

```bash
psql postgres -c "CREATE USER claw WITH PASSWORD 'claw';"
```

```bash
psql postgres -c "CREATE DATABASE clawagent OWNER claw;"
```

> **What this does:** Creates a database called `clawagent` and a user called `claw` with the password `claw`. These are just local credentials on your Mac — not exposed to the internet.

### Step 2: Set Up Your Credentials

The agent needs API keys to talk to Slack, GitHub, Jira, etc. There's a template file called `.env.example` with all the fields you need to fill in.

```bash
cd ~/Documents/Mac-developer-platform-agent
cp .env.example .env
```

> **What `cp` does:** It copies the example file to a new file called `.env`. The `.env` file is where your real passwords/tokens go. It's ignored by Git so your secrets never get shared.

Now open the `.env` file in any text editor and fill in the values you have. You don't need all of them — the agent will simply skip integrations you haven't configured. At minimum, you'll want:

- `SLACK_BOT_TOKEN` and `SLACK_SIGNING_SECRET` — so the agent can read and respond in Slack
- `GITHUB_TOKEN` — so the agent can access your repositories

> **Where to get these:** Each service has its own developer settings page. For example, Slack tokens come from [api.slack.com/apps](https://api.slack.com/apps), and GitHub tokens come from [github.com/settings/tokens](https://github.com/settings/tokens).

### Step 3: Install Python Dependencies

```bash
cd ~/Documents/Mac-developer-platform-agent
pip3 install -r requirements.txt
```

> **What `pip3 install` does:** It downloads and installs all the Python libraries the backend needs (like the Slack SDK, GitHub API client, database driver, etc.). The list of libraries is in `requirements.txt`.

### Step 4: Start the Backend Server

```bash
cd ~/Documents/Mac-developer-platform-agent/backend
python3 main.py run
```

> **What this does:** Starts the backend server on your Mac at `http://localhost:8080`. It will keep running in this Terminal window — don't close it. You'll see log messages as events come in.

You should see output like:

```
Starting Claw Agent on 0.0.0.0:8080
INFO:     Uvicorn running on http://0.0.0.0:8080
```

### Step 5: Start the Web Dashboard

Open a **new Terminal window** (Cmd+N) and run:

```bash
cd ~/Documents/Mac-developer-platform-agent/frontend
npm install
npm run dev
```

> **What `npm install` does:** Downloads all the JavaScript libraries the dashboard needs. You only need to do this once.
>
> **What `npm run dev` does:** Starts the dashboard web server. Keep this Terminal window open too.

Now open your browser and go to:

**[http://localhost:3000](http://localhost:3000)**

You should see the Claw Agent dashboard with a dark theme and a sidebar on the left.

### Step 6: Start the IronClaw Runtime

Open another **new Terminal window** and start the IronClaw runtime on port 9090. See the IronClaw documentation for instructions specific to your setup.

---

## Using the Agent

### Talking to It in Slack

Once everything is running and your Slack bot is configured, you can mention `@claw` in any channel where the bot has been added:

| What You Type | What Happens |
|---------------|-------------|
| `@claw summarize today's PRs` | The agent pulls recent pull requests from GitHub and posts a summary |
| `@claw investigate Jenkins build 1234` | The agent fetches the build logs, analyzes the failure, and explains what went wrong |
| `@claw create Jira ticket from this email` | The agent reads the email thread and creates a Jira ticket with the relevant details |

The agent replies in a **thread** under your message so it doesn't clutter the channel.

### Using the Web Dashboard

The dashboard at [localhost:3000](http://localhost:3000) has six pages (accessible from the sidebar):

| Page | What It Shows |
|------|---------------|
| **Status** | Whether IronClaw, the database, and each integration are connected and healthy |
| **Events** | A live feed of everything happening — webhooks from GitHub, Jira, Jenkins, Slack commands |
| **Workflows** | The automation rules you've set up (defined in YAML files) |
| **Runs** | History of every time a workflow ran, whether it succeeded or failed |
| **Tools** | Every tool the agent can use, with its parameters |
| **Conversations** | Full history of every Slack conversation with the agent |

---

## How Automations Work (Workflows)

Workflows are automatic actions that trigger when something happens. They're defined in simple YAML files (a human-readable format) in the `backend/workflows/` folder.

**Example — when someone opens a pull request on GitHub:**

```yaml
name: pr_opened
trigger: github.pull_request.opened

actions:
  - tool: github.summarize_pr
    description: Summarize the pull request

  - tool: slack.send_message
    args:
      channel: "#dev-notifications"
      text: "New PR opened: {{ title }}"
    description: Notify Slack channel
```

**In plain English:** When GitHub sends a "pull request opened" event, the agent automatically summarizes the PR and posts a notification to the `#dev-notifications` Slack channel.

Three workflows come pre-built:

| File | Trigger | What It Does |
|------|---------|-------------|
| `pr_opened.yaml` | New pull request on GitHub | Summarizes the PR and posts to Slack |
| `build_failed.yaml` | Jenkins build fails | Fetches logs, summarizes the failure, and alerts Slack |
| `jira_created.yaml` | New Jira ticket created | Creates a matching GitHub issue and notifies Slack |

---

## Running the Tests

The project includes a full test suite. To run it:

```bash
cd ~/Documents/Mac-developer-platform-agent/backend
pip3 install -r requirements-dev.txt
python3 -m pytest
```

> **What this does:** The first command installs testing libraries. The second runs all 89 tests. You should see a green "89 passed" message at the end.

---

## Project Structure (What's in Each Folder)

```
Mac-developer-platform-agent/
│
├── backend/                ← The Python server (the "brain")
│   ├── main.py             ← The file you run to start the server
│   ├── agent/              ← Core logic: talks to IronClaw, manages conversations
│   ├── integrations/       ← Code that talks to Slack, GitHub, Jira, etc.
│   ├── tools/              ← Registry of everything the agent can do
│   ├── database/           ← Database table definitions
│   ├── events/             ← Event system (receives and routes webhooks)
│   ├── workflows/          ← Automation engine + YAML workflow files
│   ├── webhooks/           ← Web server (receives incoming requests)
│   ├── security/           ← Handles passwords/tokens safely
│   └── tests/              ← Automated tests (89 total)
│
├── frontend/               ← The web dashboard (what you see in your browser)
│   ├── src/app/            ← The six dashboard pages
│   ├── src/components/     ← Reusable UI pieces (sidebar, status cards)
│   └── src/lib/api.ts      ← Code that fetches data from the backend
│
├── config/                 ← Configuration files
├── docs/                   ← Architecture and creation process documentation
├── logs/                   ← Log files (auto-created when the server runs)
├── .env.example            ← Template for your secret credentials
├── requirements.txt        ← List of Python libraries needed
├── requirements-dev.txt    ← Extra libraries needed only for testing
└── README.md               ← This file
```

---

## Stopping the Agent

To stop any of the running servers, go to the Terminal window where it's running and press **Ctrl+C**. This safely shuts it down.

---

## Troubleshooting

### "command not found: python3"

Homebrew may have installed Python but your Terminal doesn't know where it is. Try:

```bash
brew link python@3.13
```

Then close and reopen Terminal.

### "command not found: pip3"

Same issue. Try:

```bash
python3 -m ensurepip
```

### "connection refused" errors in the dashboard

Make sure the backend is running (Step 4). The dashboard needs the backend to be active at `localhost:8080` to fetch data.

### "no such table" database errors

The database tables are created automatically when the backend starts. Make sure PostgreSQL is running:

```bash
brew services start postgresql@15
```

### The dashboard page is blank

Make sure you ran `npm install` in the `frontend/` folder before `npm run dev`.

### Slack bot isn't responding

1. Check that your `SLACK_BOT_TOKEN` is set in `.env`
2. Make sure the bot has been added to the Slack channel you're messaging in
3. Make sure the backend server is running
4. Check the Terminal window running the backend for error messages

---

## Security Notes

- Your API keys and tokens are stored only in the `.env` file on your Mac — never in the code.
- The `.env` file is listed in `.gitignore`, so it won't accidentally get shared if you push the code to GitHub.
- All webhook requests are verified with cryptographic signatures so outsiders can't send fake events.
- Secrets are automatically scrubbed from log files so they never appear in `logs/agent.log`.

---

## Glossary

| Term | What It Means |
|------|---------------|
| **API** | A way for programs to talk to each other over the internet (like a menu a restaurant provides for delivery apps) |
| **Backend** | The server part of an application that runs behind the scenes — you don't see it directly |
| **Frontend** | The part you see in your browser (the dashboard) |
| **Webhook** | A notification sent from one service to another when something happens (e.g., GitHub telling our server "a PR was opened") |
| **Database** | A structured way to store data permanently (like a spreadsheet that programs can read/write) |
| **PostgreSQL** | The specific database software we use — it's free and widely used |
| **FastAPI** | The Python library that powers our backend web server |
| **Next.js** | The JavaScript framework that powers the dashboard |
| **Tailwind CSS** | A styling system that makes the dashboard look nice |
| **YAML** | A simple text format for configuration files — uses indentation instead of curly braces |
| **Token** | A password-like string that lets a program access a service on your behalf |
| **localhost** | Your own computer — `localhost:3000` means "port 3000 on this machine" |
| **Port** | A numbered channel on your computer — different servers use different ports so they don't conflict |
| **Runtime** | A program that runs other programs — IronClaw is a runtime that runs AI reasoning |
