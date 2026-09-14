#!/usr/bin/env python3
"""Upload Allure results and generated report artifacts to Azure File Share."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from azure.storage.fileshare import ShareDirectoryClient, ShareFileClient


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Required environment variable is missing: {name}")
    return value


def ensure_directory(connection_string: str, share_name: str, directory_path: str) -> None:
    directory = ShareDirectoryClient.from_connection_string(
        conn_str=connection_string,
        share_name=share_name,
        directory_path="",
    )
    for part in (segment for segment in directory_path.split("/") if segment):
        directory = directory.get_subdirectory_client(part)
        try:
            directory.create_directory()
        except ResourceExistsError:
            pass


def upload_file(
    connection_string: str,
    share_name: str,
    remote_path: str,
    local_path: Path,
) -> None:
    parent = remote_path.rsplit("/", 1)[0] if "/" in remote_path else ""
    ensure_directory(connection_string, share_name, parent)
    client = ShareFileClient.from_connection_string(
        conn_str=connection_string,
        share_name=share_name,
        file_path=remote_path,
    )
    try:
        client.delete_file()
    except ResourceNotFoundError:
        pass
    with local_path.open("rb") as file_handle:
        client.upload_file(file_handle)


def upload_tree(
    connection_string: str,
    share_name: str,
    local_root: Path,
    remote_root: str,
) -> int:
    if not local_root.is_dir():
        raise FileNotFoundError(f"Artifact directory does not exist: {local_root}")

    uploaded = 0
    for local_path in local_root.rglob("*"):
        if local_path.is_file():
            relative_path = local_path.relative_to(local_root).as_posix()
            upload_file(
                connection_string,
                share_name,
                f"{remote_root}/{relative_path}",
                local_path,
            )
            uploaded += 1
    return uploaded


def main() -> int:
    results_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("playwright/allure-results")
    report_root = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("playwright/allure-report")
    videos_root = Path(sys.argv[3]) if len(sys.argv) > 3 else Path("playwright/videos")
    connection_string = required_env("AZURE_STORAGE_CONNECTION_STRING")
    share_name = required_env("AZURE_FILE_SHARE_NAME")
    execution_date = required_env("EXECUTION_DATE")
    run_id = required_env("GITHUB_RUN_ID")
    remote_root = os.getenv("AZURE_FILE_SHARE_ROOT", "allure-artifacts").strip("/")
    remote_run_root = f"{remote_root}/{execution_date}/{run_id}"

    uploaded = upload_tree(
        connection_string,
        share_name,
        results_root,
        f"{remote_run_root}/allure-results",
    )
    uploaded += upload_tree(
        connection_string,
        share_name,
        report_root,
        f"{remote_run_root}/allure-report",
    )
    if videos_root.is_dir():
        uploaded += upload_tree(
            connection_string,
            share_name,
            videos_root,
            f"{remote_run_root}/videos",
        )
    print(f"Uploaded {uploaded} Allure artifact files to {share_name}/{remote_run_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
