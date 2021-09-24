import pandas as pd
import requests
import json
import os
from dotenv import load_dotenv
from typing import Dict
import base64

load_dotenv()

df = pd.read_csv("files/demo.csv")
# api_url = "http://api.touchbase.report/api/"
api_url = "http://localhost:3030/api"


def get_headers() -> Dict[str, str]:
    access_key_id = os.getenv("ACCESS_KEY_ID")
    access_key = os.getenv("ACCESS_KEY")
    if access_key_id is not None and access_key is not None:
        headers = {"access_key_id": access_key_id, "access_key": access_key}
        return headers
    else:
        raise ValueError("Access key not defined")


def push_csv(df: pd.DataFrame):
    payload = {
        "id_headers": [],
        "table": df.to_json(orient="records"),
        "report_path": ["Demo"],
        "report_name": "Demo table",
    }
    endpoint = f"{api_url}/report/table"
    r = requests.post(endpoint, json=payload, headers=get_headers())
    print(
        "Report pushed to Touchbase with status: "
        + str(r.status_code)
        + "; "
        + str(r.text)
    )


def create_report(report_name: str, report_path: list, report_type: str) -> int:
    # create report first
    r = requests.post(
        url=f"{api_url}/report",
        data={
            "report_path": report_path,
            "report_name": report_name,
            "report_type": report_type,
        },
        headers=get_headers(),
    )
    if r.status_code == 200:
        response = json.loads(r.text)
        return response["reportId"]
    else:
        raise ValueError("Report not created", r.text)


def push_image():
    # create report first
    report_id = create_report(
        report_name="Demo img", report_path=["Demo"], report_type="image"
    )
    img_path = "files/plot.png"
    # ax = df.plot.bar(x="Description", y="Order")
    # fig = ax.get_figure()
    # fig.savefig(img_path)
    endpoint = f"{api_url}/report/{report_id}/image"
    files = {"file": open(img_path, "rb")}
    r = requests.put(endpoint, files=files, headers=get_headers(), timeout=5)
    print(
        "Image pushed to Touchbase with status: "
        + str(r.status_code)
        + "; "
        + str(r.text)
    )


def push_html():
    # create report first
    report_id = create_report(
        report_name="Folium", report_path=["Demo"], report_type="html"
    )
    endpoint = f"{api_url}/report/{report_id}/file"
    with open("files/folium.html", "rb") as f:
        html = f.read()
        file_base64 = base64.b64encode(html)
        r = requests.put(
            endpoint,
            data={"file": file_base64},
            headers=get_headers(),
            timeout=5,
        )
        print(
            "Html pushed to Touchbase with status: "
            + str(r.status_code)
            + "; "
            + str(r.text)
        )


push_html()

# push_csv(df)
# for x in range(5):
#     push_image()
# report_id = create_report(
#     report_name="Plotly", report_path=["Demo"], report_type="html"
# )
# print(report_id)