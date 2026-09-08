# ShadowNet Public Deployment Guide

## 1. Local test

### Linux/macOS
```bash
cd shadownet
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Open `http://127.0.0.1:5000`.

### Windows PowerShell
```powershell
cd shadownet
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python app.py
```

## 2. Put the project on GitHub

1. Create a new GitHub repository, for example `shadownet`.
2. Extract this package.
3. Open a terminal inside the `shadownet` folder.
4. Run:

```bash
git init
git add .
git commit -m "Initial ShadowNet release"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/shadownet.git
git push -u origin main
```

Never commit `.env`, API keys, passwords, or production database files.

## 3. Deploy to Render

1. Create a Render account.
2. Choose **New > Web Service**.
3. Connect the GitHub repository.
4. Use these settings:

```text
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

5. Add these environment variables in Render:

```text
SECRET_KEY=<generate-a-long-random-secret>
COOKIE_SECURE=1
OPENAI_API_KEY=<your-server-side-openai-api-key>
OPENAI_MODEL=gpt-5.0
OPENAI_API_URL=https://api.openai.com/v1/responses
```

6. Deploy the service.
7. Open the generated `https://<service-name>.onrender.com` URL.

Render provides HTTPS for public web services and supports automatic redeployment when the connected branch receives new commits.

## 4. ShadowBot

The browser sends the user's message to `/api/assistant`. Flask sends the request to the OpenAI Responses API. The API key stays on the server.

If your OpenAI API project does not accept `gpt-5.0`, change `OPENAI_MODEL` to a model ID enabled for your project. The website reads the model from the environment variable, so no source-code change is required.

## 5. Database persistence

This package uses SQLite by default. That is suitable for local testing and a prototype.

For a real public service with persistent accounts, move the user database to PostgreSQL or attach appropriate persistent storage. A standard Render web service filesystem should not be treated as permanent application storage.

## 6. Production checklist

- Set a strong `SECRET_KEY`.
- Keep `OPENAI_API_KEY` server-side.
- Use HTTPS.
- Keep `COOKIE_SECURE=1`.
- Add rate limiting to `/api/assistant` before public launch.
- Add email verification and password reset before production use.
- Use PostgreSQL for persistent user data.
- Add a real payment provider for Premium access and verify webhooks server-side.
- Review the Privacy Policy and Terms for your actual business and jurisdiction.
- Do not store payment card details in ShadowNet.
