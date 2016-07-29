import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from decimal import *
SHOW_PLOT = False
NUM_DAYS = 20
NUM_ITERATIONS = 10000
PRICE_FROM_LAST_ROW = 405
DEBUG_PRINT_PRICES_IN_LOOP = False
df = pd.read_csv('https://raw.githubusercontent.com/fandang/DA602/master/apple.2011.csv')
#df = pd.read_csv('apple.2011.csv')
df.columns = ['Date','Last','PctChange']
df.PctChange = pd.to_numeric(df.PctChange, errors='coerce')
df = df[df.PctChange * df.PctChange > 0]
df["PctChange"] = df["PctChange"].astype(float)
daily_changes = df["PctChange"].tolist()
daily_change_min = min(daily_changes)
daily_change_max = max(daily_changes)
daily_change_mean = np.mean(daily_changes)
daily_change_sum = sum(daily_changes)
daily_change_count = len(daily_changes)
daily_changes = df["PctChange"].tolist()
mu = (daily_change_sum / daily_change_count)
sigma = np.std(daily_changes)
end_prices = []
for i in range(0,NUM_ITERATIONS):
    daily_price = PRICE_FROM_LAST_ROW
    sample = np.random.normal(mu, sigma, NUM_DAYS)
    for next_change_pct in sample:
        daily_price = daily_price + (daily_price * next_change_pct)
    end_prices.append(daily_price)
end_prices_sorted = sorted(end_prices)
array_index_to_get = NUM_ITERATIONS / 100
r = end_prices_sorted[array_index_to_get]
