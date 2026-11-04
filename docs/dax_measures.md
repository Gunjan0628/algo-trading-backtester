# DAX Measures (table: `_Measures`)

What-If parameter measures used: `[Short MA Value]`, `[Long MA Value]`, `[Initial Capital Value]`, `[Risk Free Rate Value]`.

## Group 1: Helpers
```DAX
One Market = HASONEVALUE ( DimMarket[Market] )
Valid Combo = IF ( [Short MA Value] < [Long MA Value], 1, 0 )
Close Price = AVERAGE ( Prices[Close] )
BH Ret Day = SUM ( Prices[DailyReturn] )
BH DD Day = SUM ( Prices[BH_Drawdown] )

Strat Ret Day =
VAR S = [Short MA Value]
VAR L = [Long MA Value]
RETURN CALCULATE ( SUM ( Backtest[StratRet] ), Backtest[Short] = S, Backtest[Long] = L )

Strat DD Day =
VAR S = [Short MA Value]
VAR L = [Long MA Value]
RETURN CALCULATE ( SUM ( Backtest[Drawdown] ), Backtest[Short] = S, Backtest[Long] = L )

Position Day =
VAR S = [Short MA Value]
VAR L = [Long MA Value]
RETURN CALCULATE ( SUM ( Backtest[Position] ), Backtest[Short] = S, Backtest[Long] = L )
```

## Group 2: Equity curves
```DAX
Strategy Equity =
VAR S = [Short MA Value]
VAR L = [Long MA Value]
VAR d = MAX ( Backtest[Date] )
RETURN
IF ( S < L,
    [Initial Capital Value] *
    CALCULATE ( SUM ( Backtest[Growth] ), Backtest[Short] = S, Backtest[Long] = L, Backtest[Date] = d ) )

Buy & Hold Equity =
VAR d = MAX ( Prices[Date] )
RETURN [Initial Capital Value] * CALCULATE ( SUM ( Prices[BH_Growth] ), Prices[Date] = d )
```

## Group 3: Risk and return
```DAX
Strategy CAGR =
IF ( [One Market] && [Valid Combo] = 1,
    VAR yrs = DIVIDE ( DATEDIFF ( MIN ( Backtest[Date] ), MAX ( Backtest[Date] ), DAY ), 365.25 )
    RETURN DIVIDE ( [Strategy Equity], [Initial Capital Value] ) ^ DIVIDE ( 1, yrs ) - 1 )

BH CAGR =
VAR yrs = DIVIDE ( DATEDIFF ( MIN ( Prices[Date] ), MAX ( Prices[Date] ), DAY ), 365.25 )
RETURN DIVIDE ( [Buy & Hold Equity], [Initial Capital Value] ) ^ DIVIDE ( 1, yrs ) - 1

Annual Volatility = STDEVX.P ( VALUES ( DimDate[Date] ), [Strat Ret Day] ) * SQRT ( 252 )
BH Volatility = STDEVX.P ( VALUES ( DimDate[Date] ), [BH Ret Day] ) * SQRT ( 252 )
Sharpe Ratio = DIVIDE ( [Strategy CAGR] - [Risk Free Rate Value] / 100, [Annual Volatility] )
BH Sharpe = DIVIDE ( [BH CAGR] - [Risk Free Rate Value] / 100, [BH Volatility] )
Max Drawdown = MINX ( VALUES ( DimDate[Date] ), [Strat DD Day] )
BH Max Drawdown = MINX ( VALUES ( DimDate[Date] ), [BH DD Day] )
Calmar Ratio = DIVIDE ( [Strategy CAGR], ABS ( [Max Drawdown] ) )
Alpha vs Buy & Hold = [Strategy CAGR] - [BH CAGR]
```

## Group 4: Trades and win rate
```DAX
Total Trades =
VAR S = [Short MA Value]
VAR L = [Long MA Value]
RETURN CALCULATE ( SUM ( Backtest[Trade] ), Backtest[Short] = S, Backtest[Long] = L )

Win Rate (In-Market Days) =
VAR d = VALUES ( DimDate[Date] )
VAR wins  = COUNTROWS ( FILTER ( d, [Strat Ret Day] > 0 && [Position Day] = 1 ) )
VAR inMkt = COUNTROWS ( FILTER ( d, [Position Day] = 1 ) )
RETURN DIVIDE ( wins, inMkt )
```

## Group 5: Heatmap, markers, title
```DAX
Strategy Period Return =
VAR S = [Short MA Value]
VAR L = [Long MA Value]
VAR startD = MIN ( Backtest[Date] )
VAR endD   = MAX ( Backtest[Date] )
VAR prevD  = CALCULATE ( MAX ( Backtest[Date] ), REMOVEFILTERS ( DimDate ), Backtest[Date] < startD )
VAR gEnd   = CALCULATE ( SUM ( Backtest[Growth] ), Backtest[Short] = S, Backtest[Long] = L, Backtest[Date] = endD )
VAR gStart = IF ( ISBLANK ( prevD ), 1,
    CALCULATE ( SUM ( Backtest[Growth] ), REMOVEFILTERS ( DimDate ), Backtest[Short] = S, Backtest[Long] = L, Backtest[Date] = prevD ) )
RETURN IF ( S < L, DIVIDE ( gEnd, gStart ) - 1 )

Buy Marker =
VAR S = [Short MA Value]
VAR L = [Long MA Value]
VAR t = CALCULATE ( SUM ( Backtest[Trade] ), Backtest[Short] = S, Backtest[Long] = L )
RETURN IF ( t = 1 && [Position Day] = 1, [Close Price] )

Sell Marker =
VAR S = [Short MA Value]
VAR L = [Long MA Value]
VAR t = CALCULATE ( SUM ( Backtest[Trade] ), Backtest[Short] = S, Backtest[Long] = L )
RETURN IF ( t = 1 && [Position Day] = 0, [Close Price] )

Chart Title =
"MA Crossover (" & [Short MA Value] & "/" & [Long MA Value] & ") vs Buy & Hold: "
    & SELECTEDVALUE ( DimMarket[Market], "Select one market" )

Warning = IF ( [Valid Combo] = 0, "⚠ Short MA must be smaller than Long MA", "" )
```
