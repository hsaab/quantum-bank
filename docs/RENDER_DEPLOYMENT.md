# Render.com Deployment Guide for Quantum Bank

## Prerequisites

1. GitHub account with QuantumBank repo pushed
2. Render.com account (free, no credit card required)

## Deployment Steps

### 1. Sign up for Render.com
Go to https://render.com and sign up with your GitHub account.

### 2. Create New Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub account if not already connected
3. Select the **quantum-bank** repository
4. Configure:
   - **Name**: `quantum-bank`
   - **Region**: Oregon (or closest to you)
   - **Branch**: `main`
   - **Runtime**: Docker
   - **Instance Type**: Free

### 3. Set Environment Variables

In the "Environment" section, add these variables:

| Key | Value |
|-----|-------|
| `SPLIT_API_KEY` | Your production Split.io server-side key |
| `SECRET_KEY` | Your Flask secret key |

**Important**: Get these from your `.env` file locally.

### 4. Deploy

Click **"Create Web Service"**

Render will:
- Build your Docker image
- Deploy your app
- Give you a URL like: `https://quantum-bank.onrender.com`

First deploy takes 2-3 minutes.

## Custom Domain Setup (qbank.dev)

### 1. Add Custom Domain in Render

1. Go to your service dashboard
2. Click **"Settings"** → **"Custom Domains"**
3. Click **"Add Custom Domain"**
4. Enter: `qbank.dev`
5. Also add: `www.qbank.dev`

### 2. Get DNS Records

Render will show you the DNS records needed. You'll see something like:
- **A Record**: Points to Render's IP
- **CNAME**: For www subdomain

### 3. Configure DNS in Porkbun

1. Login to Porkbun
2. Go to your domain DNS settings
3. Add the records Render gave you:
   - **Type**: `A` or `CNAME` (as shown by Render)
   - **Host**: `@` (for root domain)
   - **Answer**: The value from Render
   - **Type**: `CNAME`
   - **Host**: `www`
   - **Answer**: Your Render URL or the CNAME target

4. Wait 5-10 minutes for DNS propagation

Render will automatically provision SSL certificates (https) for your custom domain.

## Important: Database Persistence

**Note**: Render's free tier has ephemeral storage - your SQLite database will reset on:
- App restarts
- Deployments
- Inactivity sleep/wake

### Options:

**Option 1: Accept resets (fine for demos)**
- Database will reinitialize with demo data each time
- Good enough for testing/demos

**Option 2: Upgrade to persistent disk ($7/month)**
- Settings → Disks → Add Disk
- Mount path: `/data`
- Update `models.py` to use `/data/quantum_bank.db` in production

**Option 3: Use external database (free)**
- Switch to PostgreSQL using a free service like:
  - Supabase (2GB free)
  - ElephantSQL (20MB free)
  - Render's own PostgreSQL (90 days free)

For now, **Option 1** is fine - your database will reset but reinitialize automatically.

## Auto-Deploy on Push

Render automatically deploys when you push to the `main` branch on GitHub. No extra setup needed!

## Monitoring & Logs

- **View Logs**: Dashboard → "Logs" tab
- **Check Status**: Dashboard shows deploy status
- **Metrics**: Free tier includes basic metrics

## Useful Commands

Since Render auto-deploys from GitHub, just push your changes:
```bash
git add .
git commit -m "Your changes"
git push
```

Render detects the push and deploys automatically (takes ~2 mins).

## Sleep Mode (Free Tier)

Free tier apps sleep after 15 minutes of inactivity:
- First request after sleep takes ~30 seconds to wake up
- Subsequent requests are instant
- To prevent sleep: Upgrade to paid tier ($7/month)

## Costs

- **Free tier**: Includes 750 hours/month, 100GB bandwidth
- Your single app = **FREE**
- Custom domain = **FREE**
- SSL certificate = **FREE**

## Troubleshooting

### App won't start
Check logs in dashboard for errors. Common issues:
- Missing environment variables
- Port binding (should use `$PORT` env var)

### Database resets
This is expected on free tier. Upgrade to persistent disk or use external DB.

### Custom domain not working
- Verify DNS records in Porkbun match Render's instructions
- Wait up to 24 hours for DNS propagation (usually 5-10 mins)
- Check Render dashboard for SSL certificate status

## Split.io Client-Side Key

Don't forget your client-side key in `static/js/split-client.js` should match your production environment (not staging).

## Next Steps After Deployment

1. Visit your app at `https://quantum-bank.onrender.com`
2. Test login with the seeded demo user (username: `demo`, no password — demo only)
3. Verify Split.io feature flags work
4. Once DNS propagates, access via `https://qbank.dev`
