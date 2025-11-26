from backtester import Backtester

if __name__ == "__main__":
    engine = Backtester("AAPL", "2024-01-01", "2025-11-26") 
    engine.load_data()

    engine.add_moving_average(25)
    engine.add_moving_average(55) 
    engine.generate_signals(25, 55)
    
    engine.calculate_pnl(transaction_cost=0.001)
    engine.plot_results()