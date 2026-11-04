import warnings
warnings.filterwarnings("ignore")

import yfinance as yf
import pandas as pd
from itertools import product

import os
os.makedirs("data", exist_ok=True)

TICKERS = {"NIFTY 50": "^NSEI", "S&P 500": "^GSPC"}
DOWNLOAD_START = "2020-09-01"   # warm-up history for long moving averages
DISPLAY_START  = "2021-10-26"   # 5-year analysis window
DOWNLOAD_END   = "2026-10-26"   # yfinance end date is exclusive
SHORTS = list(range(5, 55, 5))      # 5, 10, ..., 50
LONGS  = list(range(50, 210, 10))   # 50, 60, ..., 200
COST   = 0.001                      # 0.1% per trade

frames = []
for name, tk in TICKERS.items():
    df = yf.download(tk, start=DOWNLOAD_START, end=DOWNLOAD_END,
                     auto_adjust=True, progress=False)
    df.columns = df.columns.get_level_values(0)
    df = df[["Close"]].dropna().reset_index()
    df["Market"] = name
    frames.append(df)
raw = pd.concat(frames, ignore_index=True)
raw["Date"] = pd.to_datetime(raw["Date"])

price_rows, grid_rows = [], []
for name, g in raw.groupby("Market"):
    g = g.sort_values("Date").reset_index(drop=True)
    g["Ret"] = g["Close"].pct_change()
    ma = {n: g["Close"].rolling(n).mean() for n in set(SHORTS + LONGS)}
    show = g["Date"] >= DISPLAY_START

    # Buy & Hold benchmark
    p = g[show].copy()
    p["DailyReturn"] = p["Ret"]
    p.iloc[0, p.columns.get_loc("DailyReturn")] = 0.0
    p["BH_Growth"] = (1 + p["DailyReturn"]).cumprod()
    p["BH_Drawdown"] = p["BH_Growth"] / p["BH_Growth"].cummax() - 1
    price_rows.append(p[["Market", "Date", "Close", "DailyReturn", "BH_Growth", "BH_Drawdown"]])

    # MA crossover grid
    for s, l in product(SHORTS, LONGS):
        if s >= l:
            continue
        signal   = (ma[s] > ma[l]).astype(int)               # 1 = invested
        position = signal.shift(1).fillna(0).astype(int)     # act NEXT day
        trade    = position.diff().abs().fillna(0).astype(int)
        sret     = position * g["Ret"].fillna(0) - trade * COST
        d = pd.DataFrame({"Market": name, "Date": g["Date"], "Short": s, "Long": l,
                          "Position": position, "Trade": trade, "StratRet": sret})[show].copy()
        d.iloc[0, d.columns.get_loc("StratRet")] = 0.0
        d["Growth"]   = (1 + d["StratRet"]).cumprod()
        d["Drawdown"] = d["Growth"] / d["Growth"].cummax() - 1
        grid_rows.append(d)

prices   = pd.concat(price_rows)
backtest = pd.concat(grid_rows)
for df in (prices, backtest):
    df["Date"] = df["Date"].dt.date
prices.round(6).to_csv("data/prices.csv", index=False)
backtest.round(6).to_csv("data/backtest.csv", index=False)

# Validation numbers to compare with Power BI later (Short=10, Long=50)
v = backtest[(backtest.Short == 10) & (backtest.Long == 50)]
for m, x in v.groupby("Market"):
    print(m, "final growth:", round(x["Growth"].iloc[-1], 4),
          "| max drawdown:", round(x["Drawdown"].min(), 4),
          "| trades:", int(x["Trade"].sum()))
print(prices.groupby("Market").size(), len(backtest))