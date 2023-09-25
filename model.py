import yfinance as yf
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import recommend
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error, r2_score

# Function to train a stock price predictor for a given stock symbol using polynomial regression
def train_stock_price_predictor(symbol, degree=2, period="max"):
    try:
        # Download the historical data for the given stock symbol
        stock = yf.Ticker(symbol)
        stock_data = stock.history(period=period)

        # Ensure that the stock data contains the necessary columns (Open, Close, High, Low, Volume)
        if 'Open' not in stock_data.columns or 'Close' not in stock_data.columns \
            or 'High' not in stock_data.columns or 'Low' not in stock_data.columns \
            or 'Volume' not in stock_data.columns:
            raise ValueError("Stock data is missing required columns (Open, Close, High, Low, Volume).")

        # Shift the opening price data to predict the future opening price (next day)
        stock_data['Future Open'] = stock_data['Open'].shift(-1)

        # Drop rows with NaN values (last rows with no future data)
        stock_data = stock_data.dropna()

        # Split the data into features (X) and target (y)
        X = stock_data[['Open', 'Close', 'High', 'Low', 'Volume']]
        y = stock_data['Future Open']

        # Create a polynomial regression model
        model = make_pipeline(PolynomialFeatures(degree), LinearRegression())

        # Fit the polynomial regression model to the data
        model.fit(X, y)
        return model

    except Exception as e:
        st.error(f"Error: INVALID TICKER")
        return None



# Function to predict the future opening price of a stock using a trained model
def predict_future_opening_price(model, symbol, historical_data):
    try:
        if historical_data.empty:
            st.error("ENTER A STOCK LISTED ON THE NASDAQ")
            return None

        # Extract the feature values (Open, Close, High, Low, Volume) for the last data point
        latest_features = historical_data[['Open', 'Close', 'High', 'Low', 'Volume']].iloc[-1].values

        # Reshape the features to have the shape (1, 5)
        latest_features = latest_features.reshape(1, -1)

        # Use the trained model to make predictions on the latest data
        predicted_opening_price = model.predict(latest_features)[0]

        return predicted_opening_price

    except Exception as e:
        st.error(f"ENTER A VALID STOCK TICKER")
        return None



def main():
    st.title("Stock Opening Price Predictor")

    # Prompt the user to enter a stock symbol
    stock_symbol = st.text_input("Enter the stock symbol (e.g., AAPL):").strip().upper()

    if stock_symbol:
        # Train the stock price predictor for the specified stock
        trained_model = train_stock_price_predictor(stock_symbol)

        # Fetch the historical data for the specified stock for a longer period (e.g., 1 year)
        stock = yf.Ticker(stock_symbol)
        historical_data = stock.history(period='5y')

        # Get the latest price from the last row of historical_data
        latest_open_price = historical_data['Open'].iloc[-1]
        latest_close_price = historical_data['Close'].iloc[-1]
        latest_volume = historical_data['Volume'].iloc[-1]
        latest_high_price = historical_data['High'].iloc[-1]
        latest_low_price = historical_data['Low'].iloc[-1]

        # Use the trained model to predict the future opening price for the next day
        predicted_opening_price = predict_future_opening_price(trained_model, stock_symbol, historical_data)

        # Round the predicted opening price to two decimal points
        rounded_predicted_opening_price = round(predicted_opening_price, 2)

        # Display the prediction
        st.subheader(f"Predicted future opening price for {stock_symbol} (next day): {rounded_predicted_opening_price}")
        # Calculate the R-squared score to evaluate model fit

        # Calculate the actual opening prices (y_true) by shifting the 'Open' prices
        y_true = historical_data['Open'].shift(-1)
        y_true = y_true.dropna()  # Remove NaN values

        # Calculate predictions using the model
        predictions = trained_model.predict(historical_data[['Open', 'Close', 'High', 'Low', 'Volume']])
        predictions = predictions[:-1]  # Exclude the last prediction, which has no corresponding y_true

        # Calculate the mean squared error (MSE)
        mse = mean_squared_error(y_true, predictions)
        r_squared = r2_score(y_true, predictions)
        # Provide a recommendation based on the prediction and latest price
        recommendation_html = recommend.make_recommendation(predicted_opening_price, latest_close_price)
        st.markdown(recommendation_html, unsafe_allow_html=True)
        st.markdown(f"""<div style="padding-left: 10px;"> Mean Squared Error (MSE): {mse:.2f} </div>""", unsafe_allow_html=True)
        st.markdown(f"""<div style="padding-left: 10px;"> R-squared (R²) Score: {r_squared:.2f} </div>""", unsafe_allow_html=True)


        # Plot the 'Open' and 'Close' columns from historical data for the entire period
        st.subheader(f"Price History for the Past Year:")
        plt.figure(figsize=(10, 6))

        plt.plot(historical_data.index, historical_data['Open'], label='Open Price', color='blue')
        plt.plot(historical_data.index, historical_data['Close'], label='Close Price', color='green')
        plt.xlabel('Date')
        plt.ylabel('Price')

        plt.title(f'Price History for {stock_symbol}')
        plt.legend()
        st.pyplot(plt)

        # Display current metrics in a table
        st.subheader("Current Metrics:")

        metrics_table = f"""
        | Metric          | Value             | Metric          | Value             |
        |-----------------|-------------------|-----------------|-------------------|
        | Latest OPEN Price   | {round(latest_open_price, 2)} | Latest CLOSING Price | {round(latest_close_price, 2)} |
        | Latest HIGH         | {round(latest_high_price, 2)} | Latest LOW          | {round(latest_low_price, 2)} 
        | Latest VOLUME       | {round(latest_volume, 2)} |
        """
        st.markdown(metrics_table, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
