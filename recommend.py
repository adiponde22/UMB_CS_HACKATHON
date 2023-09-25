## Makes recommendation based on predicted opening and current closing
def make_recommendation(predicted_opening_price, latest_price):
    if predicted_opening_price > latest_price:
        recommendation = "Recommendation: Buy"
        style = "background-color: #16915a; padding: 10px; border-radius: 5px;"
    else:
        recommendation = "Recommendation: Do Not Buy"
        style = "background-color: #a11516; padding: 10px; border-radius: 5px;"

    return f'<div style="{style}">{recommendation}</div>'