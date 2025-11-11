import json
from pathlib import Path
from typing import Optional

import httpx
import typer

API_URL = typer.Option("http://localhost:8000/api/v1", "--api-url", help="Base API URL")

app = typer.Typer(help="Document pipeline CLI")


def _request(method: str, url: str, **kwargs):
    with httpx.Client() as client:
        response = client.request(method, url, **kwargs)
    response.raise_for_status()
    payload = response.json()
    if not payload.get("success", False):
        raise typer.Exit(code=1)
    return payload["data"]


@app.command()
def pipelines_list(api_url: str = API_URL, use_case: Optional[str] = None, active_only: bool = True):
    data = _request("GET", f"{api_url}/pipelines", params={"use_case": use_case, "active_only": active_only})
    typer.echo(json.dumps(data, indent=2))


@app.command()
def pipelines_show(pipeline_id: str, api_url: str = API_URL):
    data = _request("GET", f"{api_url}/pipelines/{pipeline_id}")
    typer.echo(json.dumps(data, indent=2))


@app.command()
def pipelines_create(from_file: Path, api_url: str = API_URL):
    payload = json.loads(from_file.read_text())
    data = _request("POST", f"{api_url}/pipelines", json=payload)
    typer.echo(json.dumps(data, indent=2))


@app.command()
def pipelines_run(
    pipeline_id: str,
    document_id: Optional[str] = typer.Option(None),
    file_path: Optional[str] = typer.Option(None),
    text: Optional[str] = typer.Option(None, "--text"),
    api_url: str = API_URL,
):
    body = {
        "document_id": document_id,
        "file_path": file_path,
        "text_payload": text,
    }
    data = _request("POST", f"{api_url}/pipelines/{pipeline_id}/run", json=body)
    typer.echo(json.dumps(data, indent=2))


@app.command()
def runs_status(run_id: str, api_url: str = API_URL):
    data = _request("GET", f"{api_url}/runs/{run_id}")
    typer.echo(json.dumps(data, indent=2))


@app.command()
def runs_list(api_url: str = API_URL, pipeline_id: Optional[str] = None):
    params = {"pipeline_id": pipeline_id}
    data = _request("GET", f"{api_url}/runs", params=params)
    typer.echo(json.dumps(data, indent=2))


@app.command()
def documents_register(file_path: str, mime_type: Optional[str] = None, api_url: str = API_URL):
    payload = {
        "source_type": "file_path",
        "file_name": Path(file_path).name,
        "mime_type": mime_type,
        "storage_uri": file_path,
    }
    data = _request("POST", f"{api_url}/documents", json=payload)
    typer.echo(json.dumps(data, indent=2))


if __name__ == "__main__":
    app()
