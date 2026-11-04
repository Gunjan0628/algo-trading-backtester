# Build Steps (condensed)

| Phase | Work | Platform |
|---|---|---|
| 1 | Download data, build backtest grid (`python/data.py`) | Python / VS Code |
| 2 | Validate in Excel (daily return, first row = 0 / growth = 1) | Excel |
| 3 | Load prices.csv and backtest.csv, set types | Power BI Desktop (Power Query) |
| 4 | DimDate, DimMarket, relationships, hide FK columns, Don't summarize | Power BI Model/Table view |
| 5 | Four What-If parameters | Power BI Modeling tab |
| 6 | DAX measures in `_Measures` (see dax_measures.md), format as % / currency | Power BI |
| 7 | Dashboard pages | Power BI Report view |
| 8 | Validation tests | Power BI vs Python output |
| 9 | GitHub, demo video, LinkedIn | GitHub / Loom |

## Dashboard pages
1. Executive Summary: Market tile slicer (single select), 4 What-If sliders, warning card, 6 KPI cards, line chart (Strategy vs Buy & Hold, dynamic title), comparison table (Market slicer interaction turned off so both markets show)
2. Risk Analysis: drawdown area chart, risk matrix with conditional formatting
3. Strategy Insights: Year x Month heatmap, buy/sell markers on price, insights text
4. Methodology: data source, rules, assumptions, limitations

## Validation (Short=10, Long=50, capital 100,000)
| Market | Python final growth | Power BI Strategy Equity | Max DD | Trades |
|---|---|---|---|---|
| NIFTY 50 | 1.0783 | 107.83K (matched) | -13.75% (matched) | 35 |
| S&P 500 | 1.3697 | 136.97K (expected, verify) | -13.54% | 30 |
