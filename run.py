import pandas as pd
import requests
import json
import os
from dotenv import load_dotenv
from typing import Dict

load_dotenv()

df = pd.read_csv("files/demo.csv")
api_url = "http://api.touchbase.report/api/"


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


def create_report(report_name: str, report_path: list) -> int:
    # create report first
    r = requests.post(
        url=f"{api_url}/report",
        data={
            "report_path": report_path,
            "report_name": report_name,
            "report_type": "image",
        },
        headers=get_headers(),
    )
    response = json.loads(r.text)
    if r.status_code == 200:
        return response["reportId"]
    else:
        raise ValueError("Report not created", response)


def push_image(df: pd.DataFrame):
    # create report first
    report_id = create_report(report_name="Demo img", report_path=["Demo"])
    ax = df.plot.bar(x="Description", y="Order")
    fig = ax.get_figure()
    img_path = "img/plot.png"
    fig.savefig(img_path)
    endpoint = f"{api_url}/report/{report_id}/image"
    files = {"file": open(img_path, "rb")}
    r = requests.put(endpoint, files=files, headers=get_headers(), timeout=5)
    print(
        "Image pushed to Touchbase with status: "
        + str(r.status_code)
        + "; "
        + str(r.text)
    )


push_csv(df)
push_image(df)
