import yfinance as yf
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error

# Function to train a stock price predictor for a given stock symbol using polynomial regression
def train_stock_price_predictor(symbol, degree=2, period="max"):
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
# Function to predict the future opening price of a stock using a trained model
def predict_future_opening_price(model, symbol, historical_data):
    # Extract the feature values (Open, Close, High, Low, Volume) for the last data point
    latest_features = historical_data[['Open', 'Close', 'High', 'Low', 'Volume']].iloc[-1].values

    # Reshape the features to have the shape (1, 5)
    latest_features = latest_features.reshape(1, -1)

    # Use the trained model to make predictions on the latest data
    predicted_opening_price = model.predict(latest_features)[0]

    return predicted_opening_price


def make_recommendation(predicted_opening_price, current_closing_price):
    if predicted_opening_price > current_closing_price:
        recommendation = "Recommendation: Buy"
        style = "background-color: #16915a; padding: 10px; border-radius: 5px;"
    else:
        recommendation = "Recommendation: Do Not Buy"
        style = "background-color: #a11516; padding: 10px; border-radius: 5px;"

    return f'<div style="{style}">{recommendation}</div>'


# Streamlit app
def main():
    st.title("Stock Opening Price Predictor")

    # Prompt the user to enter a stock symbol
    stock_symbol = st.text_input("Enter the stock symbol (e.g., AAPL):").strip().upper()

    if stock_symbol:
        # Train the stock price predictor for the specified stock
        trained_model = train_stock_price_predictor(stock_symbol)

        # Fetch the historical data for the specified stock for the past week (5 trading days)
        stock = yf.Ticker(stock_symbol)
        start_date = pd.Timestamp.now() - pd.DateOffset(days=5)
        end_date = pd.Timestamp.now()
        historical_data = stock.history(period="1d", start=start_date, end=end_date)

        # Use the trained model to predict the future opening price for the next day
        predicted_opening_price = predict_future_opening_price(trained_model, stock_symbol, historical_data)

        # Round the predicted opening price to two decimal points
        rounded_predicted_opening_price = round(predicted_opening_price, 2)

        # Display the prediction
        st.subheader(f"Predicted future opening price for {stock_symbol} (next day): {rounded_predicted_opening_price}")


        current_opening_price = historical_data['Open'].iloc[-1]
        current_closing_price = historical_data['Close'].iloc[-1]
        current_volume = historical_data['Volume'].iloc[-1]

        # Provide a recommendation based on the prediction
        recommendation_html = make_recommendation(predicted_opening_price, current_closing_price)
        st.markdown(recommendation_html, unsafe_allow_html=True)

        # Plot only the 'Open' and 'Close' columns from historical data
        st.subheader(f"Price History for the Past Week ({start_date.date()} to {end_date.date()}):")
        plt.figure(figsize=(10, 6))
        plt.plot(historical_data['Open'], label='Open Price', color='blue')
        plt.plot(historical_data['Close'], label='Close Price', color='green')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title(f'Price History for {stock_symbol}')
        plt.legend()
        st.pyplot(plt)

        # Calculate and display current metrics
        st.subheader("Current Metrics:")
        st.write(f"- Latest Opening Price: {round(current_opening_price, 2)}")
        st.write(f"- Latest Closing Price: {round(current_closing_price, 2)}")
        st.write(f"- Latest Volume Price: {round(current_volume, 2)}")
if __name__ == "__main__":
    main()
