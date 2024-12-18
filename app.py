from flask import Flask, render_template, request, jsonify
from api_handler import fetch_stock_ratios

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/comparestocks', methods=['GET', 'POST'])
def compare_stocks():
    if request.method == 'GET':
        # Render the compare stocks page
        return render_template('compare.html')

    if request.method == 'POST':
        selectedStocks = request.get_json().get('stocks', [])
        print(selectedStocks)
        try:
            stock_data = fetch_stock_ratios(selectedStocks)
            transformed_data = [
        {
            'symbol': symbol,
            'pe_ratio': details.get('P/E Ratio', 'N/A'),
            'eps': details.get('EPS', 'N/A'),
            'roa': details.get('ROE', 'N/A'),  # Rename as 'ROA' for consistency
            'earnings_to_growth_ratio': details.get('Earnings To Growth Ratio', 'N/A')
        }
        for symbol, details in stock_data.items()
    ]
            return jsonify(transformed_data), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
