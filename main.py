from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

# Load the CSV file into a pandas DataFrame
csv_file_path = 'Quarterly_Deal_Size_Age_and_Returning_Client_Combined_Table_Updated_File.csv'  # Path to your CSV file
df = pd.read_csv(csv_file_path)

# Define a route for fetching CSV data as JSON
@app.route('/api/v1/csv-data', methods=['GET'])
def get_csv_data():
    # Convert the DataFrame to a dictionary and return as JSON
    data = df.to_dict(orient='records')
    return jsonify(data)

# Optionally, filter the CSV data based on a query parameter (e.g., by quarter)
@app.route('/api/v1/csv-data/filter', methods=['GET'])
def filter_csv_data():
    quarter = request.args.get('quarter')  # Get the 'quarter' query parameter

    if not quarter:
        return jsonify({"error": "No quarter parameter provided"}), 400

    # Check if the quarter value is in the expected format
    if not isinstance(quarter, str) or not any(quarter.endswith(q) for q in ['Q1', 'Q2', 'Q3', 'Q4']):
        return jsonify({"error": "Invalid quarter format"}), 400

    try:
        # Filter the data based on the 'quarter' parameter
        filtered_data = df[df['Quarter'] == quarter]
        
        # Convert the filtered data to a dictionary and then to JSON
        result = filtered_data.to_dict(orient='records')
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Main entry point for local development
if __name__ == '__main__':
    app.run(debug=True)
