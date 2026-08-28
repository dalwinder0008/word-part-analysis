import re
import pandas as pd


# ==============================================================================
input_csv_path = r"input_search_terms.csv"

stop_words = {
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

        if clean_word and clean_word not in stop_words:
            return clean_word

    return re.sub(r"[^\w]", "", words[0], flags=re.UNICODE) if words else ""


def process_csv():
    try:
        #
        df = pd.read_csv(input_csv_path)

        first_column_name = df.columns[0]
        df["Main Word"] = df[first_column_name].apply(extract_one_word)

        selected_columns = [
            "Main Word",
            df.columns[5],  # Column F (Impr.)
            df.columns[6],  # Column G (Clicks)
            df.columns[8],  # Column I (Cost)
            df.columns[11],  # Column L (Conv. rate)
        ]

        result_df = df[selected_columns]

     
        output_csv_path = "temp_one_word_analysis.csv"
        result_df.to_csv(output_csv_path, index=False, encoding="utf-8-sig")

        print(f" Success! Temporary CSV file generated")
        print(f" Path: {output_csv_path}")

    except Exception as e:
        print(f" Error occurred: {e}")


if __name__ == "__main__":
    process_csv()
