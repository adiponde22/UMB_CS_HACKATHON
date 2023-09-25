# Stock Opening Price Predictor

The Stock Opening Price Predictor is a Python-based web application built with Streamlit that allows users to predict the future opening price of a stock using historical stock price data and a polynomial regression model. This application provides insights into stock price trends and offers predictions for the next day's opening price.

## Features

- Predicts the future opening price of a stock based on historical data.
- Displays historical price charts for the past five years.
- Provides key metrics and recommendations for the specified stock.
- Calculates and displays the Mean Squared Error (MSE) and R-squared (R²) score to evaluate model accuracy.

## Getting Started

Follow these instructions to set up and run the Stock Opening Price Predictor on your local machine.

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/adiponde22/UMB_CS_HACKATHON.git
   ```

2. Navigate to the project directory:

   ```bash
   cd UMB_CS_HACKATHON
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. Run the Streamlit application:

   ```bash
   streamlit run model.py
   ```

2. Open a web browser and go to the provided URL (usually `http://localhost:8501`).

3. Enter the stock symbol (e.g., AAPL) in the input field and click "Predict."

4. View the predicted future opening price, historical price charts, metrics, and recommendations.

### Built With

- [Streamlit](https://www.streamlit.io/)
- [yfinance](https://pypi.org/project/yfinance/)
- [pandas](https://pandas.pydata.org/)
- [matplotlib](https://matplotlib.org/)
- [scikit-learn](https://scikit-learn.org/)

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Acknowledgments

- Data provided by Yahoo Finance via the `yfinance` library.
- Stock price predictions based on polynomial regression.

---

You can customize this README to include additional information or specific details about your project. Don't forget to replace the placeholders with your actual project details and URLs.
