import io
import pandas as pd
import pytest
from Backend.script2 import app, extract_one_word


def test_extract_one_word():
    assert extract_one_word("how to start a coding business") == "start"
    assert extract_one_word("best python online course") == "python"
    assert extract_one_word("the an of in") == "the"
    assert extract_one_word("") == ""


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_analyze_endpoint_no_file(client):
    response = client.post("/analyze")
    assert response.status_code == 400
    assert response.json["error"] == "No file uploaded"


def test_analyze_endpoint_empty_csv(client):
    data = {"file": (io.BytesIO(b""), "empty.csv")}
    response = client.post("/analyze", data=data, content_type="multipart/form-data")
    assert response.status_code == 400
    assert response.json["error"] == "CSV File is empty"


def test_analyze_endpoint_valid_csv(client):
    csv_content = (
        "Search term,Campaign,Ad Group,Match type,Added/Excluded,Impressions,Clicks,CTR,Cost,Avg CPM,Avg CPC,Conversion rate\n"
        "best python tutorial,Campaign 1,AdGroup 1,Exact,Added,100,10,10%,$5.50,$55,$0.55,2.5%\n"
        "how to code in java,Campaign 1,AdGroup 1,Exact,Added,200,20,10%,$10.00,$50,$0.50,5.0%\n"
    )
    data = {"file": (io.BytesIO(csv_content.encode("utf-8")), "test.csv")}
    response = client.post("/analyze", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    res_data = response.json
    assert res_data["success"] is True
    assert len(res_data["data"]) == 2
    assert res_data["data"][0]["Main Word"] == "python"
    assert res_data["data"][0]["Impr."] == 100
    assert res_data["data"][0]["Clicks"] == 10
    assert res_data["data"][0]["Cost"] == 5.5
    assert res_data["data"][0]["Conv. rate"] == 2.5
