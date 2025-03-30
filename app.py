from flask import Flask, request, jsonify, send_file
import os
from converter import convert_joor_to_shopify
import pandas as pd

app = Flask(__name__)

# Environment variable for the folder where JOOR input files are stored.
# For testing on Render, these can be set via environment variables.
JOOR_FOLDER = os.environ.get("GOOGLE_DRIVE_JOOR_FOLDER_ID", "joor_input")
SHOPIFY_OUTPUT_FOLDER = os.environ.get("GOOGLE_DRIVE_SHOPIFY_OUTPUT_FOLDER_ID", "shopify_output")

# Ensure the output folder exists.
os.makedirs(SHOPIFY_OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return "JOOR to Shopify Converter is running!"

@app.route("/convert", methods=["POST"])
def convert_file():
    # Check if the POST request has the file part.
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Save the uploaded file locally.
    input_path = os.path.join(JOOR_FOLDER, file.filename)
    os.makedirs(JOOR_FOLDER, exist_ok=True)
    file.save(input_path)
    
    # Convert the file using the conversion function.
    try:
        shopify_df = convert_joor_to_shopify(input_path)
    except Exception as e:
        return jsonify({"error": f"Conversion failed: {str(e)}"}), 500

    # Create an output filename and save the Shopify CSV.
    output_filename = file.filename.replace(".xlsx", "_shopify.csv")
    output_path = os.path.join(SHOPIFY_OUTPUT_FOLDER, output_filename)
    shopify_df.to_csv(output_path, index=False)
    
    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
