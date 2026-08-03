import os
import re
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
    "कौन",
    "सा",
    "है",
    "कम",
    "क्या",
    "का",
    "की",
    "के",
    "में",
    "से",
    "को",
    "पर",
    "और",
    "या",
    "वाले",
    "वाला",
    "वाली",
    "होता",
    "होती",
    "करें",
    "कैसे",
    "बिजनेस",
    "आइडिया",
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
        # CSV Load karein
        df = pd.read_csv(file)

        if df.empty:
            return jsonify({"error": "CSV File is empty"}), 400

        # Pehla column keyword/query hoga
        keyword_col = df.columns[0]

        # One Word Extract karke naya column banayein
        df["Main Word"] = df[keyword_col].apply(extract_one_word)

        # Clicks, Impressions, Cost columns ko detect karein (case-insensitive check)
        metrics = {}
        for col in df.columns:
            col_lower = col.strip().lower()
            if "click" in col_lower:
                metrics["Clicks"] = col
            elif "impr" in col_lower:
                metrics["Impressions"] = col
            elif "cost" in col_lower or "spend" in col_lower:
                metrics["Cost"] = col

        # Metrics values ko float/int me convert karein (agar comma ',' vagairah ho to saaf karein)
        for metric_name, col_name in metrics.items():
            df[col_name] = (
                df[col_name]
                .astype(str)
                .str.replace(",", "")
                .str.replace("$", "")
                .str.replace("₹", "")
            )
            df[col_name] = pd.to_numeric(df[col_name], errors="coerce").fillna(0)

        # 'Main Word' ke hisab se Group By (Sum) karein
        group_cols = [metrics[m] for m in metrics]

        if group_cols:
            summary_df = (
                df.groupby("Main Word")[group_cols].sum().reset_index()
            )
        else:
            # Agar koi Clicks/Impressions/Cost column na mile to sirf unique Main Words bhej do
            summary_df = df[["Main Word"]].drop_duplicates()

        # Rename columns to standard names for JSON output
        rename_dict = {
            col_name: m_name for m_name, col_name in metrics.items()
        }
        summary_df.rename(columns=rename_dict, inplace=True)

        # Temporary CSV Save karein
        temp_file_path = "temp_one_word_analysis.csv"
        summary_df.to_csv(temp_file_path, index=False, encoding="utf-8-sig")

        # Result JSON format me bhej do (Array of Objects)
        result_data = summary_df.to_dict(orient="records")

        return jsonify({"success": True, "data": result_data})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
