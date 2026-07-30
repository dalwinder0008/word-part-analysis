import os
import re
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS  # <-- 1. IMPORT CORS

app = Flask(__name__)
CORS(app)  # <-- 2. ALLOW CORS (LIVE SERVER ACCESSIBLE)

STOP_WORDS = {
    "how",
    "to",
    "a",
    "an",
    "the",
    "in",
    "of",
    "for",
    "on",
    "with",
    "is",
    "at",
    "by",
    "from",
    "and",
    "or",
    "what",
    "which",
    "best",
    "top",
    "small",
    "business",
    "ideas",
    "kaise",
    "kare",
    "me",
    "main",
    "ko",
    "se",
    "ke",
    "ki",
    "near",
    "near me",
   
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
        df = pd.read_csv(file)
        first_col = df.columns[0]

        result_df = pd.DataFrame()
        result_df["Main Word"] = df[first_col].apply(extract_one_word)

        temp_file_path = "temp_one_word_analysis.csv"
        result_df.to_csv(temp_file_path, index=False, encoding="utf-8-sig")

        words_list = result_df["Main Word"].tolist()
        return jsonify({"success": True, "words": words_list})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
