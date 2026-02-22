# Publishing changes to the live site

The app is set up to run on **Render** (see the Dockerfile). To publish your local changes:

## 1. Commit your changes

```bash
cd "/Users/bsp/cursor V1/studious-broccoli-forecast"
git status
git add .
git commit -m "Describe your changes (e.g. Add incremental tool, ROAS, conv rate label)"
```

## 2. Push to the remote

```bash
git push origin main
```

(Use your usual branch name if you don’t use `main`.)

## 3. Let Render deploy

- If the Render service is connected to this repo, it will detect the push and start a new deploy.
- In the [Render dashboard](https://dashboard.render.com), open your **Web Service** and check the **Events** or **Logs** tab for deploy progress.
- The live site will update once the deploy finishes (usually 1–3 minutes).

---

**If you use a different host** (e.g. Heroku, Railway, Fly.io, or your own server):

- **Git-based:** Push to the branch that triggers deploys (often `main`).
- **Docker:** Build and run the image using the repo’s `Dockerfile`, then deploy that image with your provider’s instructions.
- **Manual:** Copy the project (or pull the repo) on the server, install deps, and restart the app (e.g. restart the process or container).

Need a one-line recap: **commit → push to `main` (or your deploy branch) → Render redeploys automatically.**
