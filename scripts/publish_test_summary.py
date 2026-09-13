#!/usr/bin/env python3
"""Publish an Allure execution summary to Azure Cosmos DB."""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from azure.cosmos import CosmosClient


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Required environment variable is missing: {name}")
    return value


def publish_summary(summary_path: Path) -> None:
    with summary_path.open("r", encoding="utf-8") as summary_file:
        summary = json.load(summary_file)

    run_id = required_env("GITHUB_RUN_ID")
    project = os.getenv("PROJECT_NAME", "robot-framework-project")
    report_url = required_env("REPORT_URL")
    failed = int(summary.get("failed", 0))

    document = {
        "id": run_id,
        "run_id": run_id,
        "project": project,
        "total_tests": int(summary.get("total_tests", 0)),
        "passed_tests": int(summary.get("passed", 0)),
        "failed_tests": failed,
        "skipped_tests": int(summary.get("skipped", 0)),
        "execution_status": "passed" if failed == 0 else "failed",
        "report_url": report_url,
        "executed_at": summary.get("timestamp") or datetime.now(timezone.utc).isoformat(),
        "commit_sha": os.getenv("GITHUB_SHA", ""),
        "branch": os.getenv("GITHUB_REF_NAME", ""),
    }

    client = CosmosClient(required_env("COSMOS_ENDPOINT"), required_env("COSMOS_KEY"))
    container = client.get_database_client(
        required_env("COSMOS_DATABASE")
    ).get_container_client(required_env("COSMOS_CONTAINER"))
    container.upsert_item(document)
    print(
        "Published test summary to Cosmos DB: "
        f"total={document['total_tests']} passed={document['passed_tests']} "
        f"failed={document['failed_tests']} report_url={report_url}"
    )


def main() -> int:
    summary_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/allure_summary.json")
    try:
        publish_summary(summary_path)
    except Exception as error:
        print(f"Cosmos DB publish failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
