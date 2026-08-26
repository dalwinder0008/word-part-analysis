import os
import re
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

STOP_WORDS = {
    "how", "to", "a", "an", "the", "in", "of", "for", "on", "with", "is", "at", "by", 
    "from", "and", "or", "what", "which", "best", "top", "small", "business", "ideas", 
    "kaise", "kare", "me", "main", "ko", "se", "ke", "ki", "near", "near me"
}

def extract_one_word(phrase):
    if not isinstance(phrase, str):
        return ""
    words = phrase.lower().strip().split()
    for word in words:
        clean_word = re.sub(r"[^\w]", "", word, flags=re.UNICODE)
        if clean_word and clean_word not in STOP_WORDS:
            return clean_word
    return re.sub(r"[^\w]", "", words[0], flags=re.UNICODE) if words else ""

@app.route("/analyze", methods=["POST"])
def analyze_csv():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    try:
        try:
            df = pd.read_csv(file)
        except pd.errors.EmptyDataError:
            return jsonify({"error": "CSV File is empty"}), 400

        if df.empty:
            return jsonify({"error": "CSV File is empty"}), 400

        result_df = pd.DataFrame()

        first_col = df.columns[0]
        result_df["Main Word"] = df[first_col].apply(extract_one_word)

     
        def get_col_data(keywords, default_val=0):
            for col in df.columns:
                col_lower = col.strip().lower()
                if any(kw in col_lower for kw in keywords):
                    # Clean numeric strings (remove commas, quotes, currency symbols, %, etc.)
                    clean_series = df[col].astype(str).str.replace(r"[^\d.-]", "", regex=True)
                    return pd.to_numeric(clean_series, errors='coerce').fillna(default_val)
            return pd.Series([default_val] * len(df))

        result_df["Impr."] = get_col_data(["impr", "impression"])
        result_df["Clicks"] = get_col_data(["click"])
        result_df["Cost"] = get_col_data(["cost", "spend"])
        result_df["Conv. rate"] = get_col_data(["conv. rate", "conversion rate", "conv rate", "conv"])


        return jsonify({"success": True, "data": result_df.to_dict(orient="records")})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
