# Algorithmic Trading Backtesting and Risk Analytics (Power BI)

Interactive dashboard that backtests Moving Average crossover strategies on NIFTY 50 and S&P 500 over 5 years, with live What-If controls.

## Architecture
Python (yfinance, pandas) -> prices.csv + backtest.csv (159 MA pairs x 2 markets) -> Power BI (star schema, What-If parameters, DAX analytics)

## Folder
- `python/data.py`: data download and backtest grid
- `docs/data_model.md`: tables, relationships, parameters, design decisions
- `docs/dax_measures.md`: all DAX measures
- `docs/build_steps.md`: build phases and validation results
- `docs/resume_and_linkedin.md`: resume bullets and post template
- `CHAT_HANDOFF.md`: context to paste into a new Claude chat
- `powerbi/` and `screenshots/`: add your .pbix and dashboard screenshots here

## Assumptions and limitations
Long-only, next-day execution, 0.1% cost per trade, no slippage or taxes. In-sample test, no walk-forward validation. Past performance does not guarantee future results.
