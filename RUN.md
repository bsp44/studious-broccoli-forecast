# Running the Marketing Forecaster locally

On macOS, use `python3` and `pip3` (not `python`/`pip`).

**1. Install dependencies (once)**

```bash
cd "/Users/bsp/cursor V1/studious-broccoli-forecast"
pip3 install -r requirements-forecast.txt
```

**2. Start the app**

```bash
python3 marketing_forecast.py
```

**3. Open in browser**

- Original forecaster (spend %): http://localhost:5001/
- Incremental budget impact: http://localhost:5001/incremental

To stop the server: `Ctrl+C` in the terminal.
