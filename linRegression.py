import pandas as pd, numpy as np, matplotlib.pyplot as plt
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

df = pd.read_csv('auctions.csv')

for i in range(1,7):
    x = df.iloc[:, i].values
    y = df.iloc[:, 0].values
    print(df.columns[i])
    x = np.reshape(x,(163,1))
    y = np.reshape(y,(163,1))
    reg = LinearRegression()
    reg.fit(x,y)
    print("Coefficient ", reg.coef_, "Intercept ", reg.intercept_)
    Y = reg.predict(x)
    print("Mean squared error: ",mean_squared_error(y, Y))
    print("Coefficient of determination (R squared): ",r2_score(y, Y))