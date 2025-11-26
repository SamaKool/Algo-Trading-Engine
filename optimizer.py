from backtester import Backtester

engine = Backtester("AAPL", "2024-01-01", "2025-11-25")
engine.load_data()

fast_windows = [5, 10, 15, 20, 25, 30]
slow_windows = [35, 40, 45, 50, 55, 60]

best_return = -9999
best_pair = (0, 0)

print("Starting Optimization...")
print("-------------------------")

for fast in fast_windows:
    for slow in slow_windows:
        engine.reset_data()
        
        engine.add_moving_average(fast)
        engine.add_moving_average(slow)        
        engine.generate_signals(fast, slow)        
        cumulative_returns = engine.calculate_pnl(transaction_cost=0.001)
        
        if cumulative_returns.empty:
            continue
                    
        total_return = (cumulative_returns.iloc[-1] - 1) * 100
        
        if total_return > best_return:
            best_return = total_return
            best_pair = (fast, slow)
            print(f"New High Score! Fast:{fast} / Slow:{slow} -> Return: {total_return:.2f}%")

print("-------------------------")
print(f"OPTIMIZATION COMPLETE")
print(f"Best strategy: SMA {best_pair[0]} v/s SMA {best_pair[1]}")
print(f"Best Return: {best_return:.4f}%")