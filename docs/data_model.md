# Data Model and What-If Parameters

## Tables
- **Prices** (fact, 2,488 rows): Market, Date, Close, DailyReturn, BH_Growth, BH_Drawdown
- **Backtest** (fact, 395,592 rows): Market, Date, Short, Long, Position, Trade, StratRet, Growth, Drawdown
- **DimDate** (calculated): Date, Year, MonthNo, Month (sorted by MonthNo), marked as date table
- **DimMarket** = DISTINCT(Prices[Market])
- **_Measures**: holds all measures

## Relationships (all one-to-many, single direction)
DimDate[Date] -> Prices[Date], Backtest[Date]
DimMarket[Market] -> Prices[Market], Backtest[Market]

## What-If parameters
| Name | Type | Min | Max | Increment | Default |
|---|---|---|---|---|---|
| Short MA | Whole | 5 | 50 | 5 | 10 |
| Long MA | Whole | 50 | 200 | 10 | 50 |
| Initial Capital | Whole | 100000 | 1000000 | 50000 | 100000 |
| Risk Free Rate | Decimal | 0 | 10 | 0.25 | 6 |

Increments for Short/Long must match the Python grid.

## Design decision
Pure-DAX path-dependent backtests (moving averages, signals, running peaks) nest iterators and scale badly. Python pre-computes the backtest for 159 (Short, Long) pairs x 2 markets; What-If parameters select the pair; DAX handles all analytics (CAGR, volatility, Sharpe, drawdown, Calmar, win rate).

## Method notes
- Next-day execution (signal.shift(1)) to avoid look-ahead bias
- 0.1% transaction cost per trade, long-only, no slippage or taxes
- Extra history downloaded so long MAs are valid on day one
