from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# List to store all received trading signals
signals = []

@app.route('/webhook', methods=['POST'])
def webhook():
    # Get the JSON data from the request
    data = request.json

    if not data:
        return jsonify({"error": "No data received"}), 400

    # Log the entire data content
    app.logger.info(f"Received data: {data}")

    # Extract action and other details (assuming TradingView sends a JSON formatted message)
    action = data.get('action')
    symbol = data.get('symbol', 'EURUSD')  # Default to EURUSD if not provided
    lots = float(data.get('lots', 0.1))    # Default to 0.1 lots if not provided

    # Log the received data and add to signals list
    print(f"Received Signal: Action={action}, Symbol={symbol}, Lots={lots}")
    signals.append({"action": action, "symbol": symbol, "lots": lots})

    # Respond to TradingView
    return jsonify({"status": "success", "message": "Signal received"}), 200

# New endpoint to get the last received trading signal
@app.route('/get_signal', methods=['GET'])
def get_signal():
    if not signals:
        return jsonify({"error": "No signal received yet"}), 404
    
    # Pop the oldest signal to ensure processing in FIFO order
    return jsonify(signals.pop(0)), 200

if __name__ == '__main__':
    # Run the Flask server
    app.run(host='0.0.0.0', port=5000)
