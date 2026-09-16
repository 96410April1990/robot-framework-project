
import os
import sys
from pathlib import Path
from azure.identity import ManagedIdentityCredential
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

load_dotenv()

def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Required environment variable is missing: {name}")
    return value

credential = ManagedIdentityCredential()

STORAGE_ACCOUNT_NAME = required_env("STORAGE_ACCOUNT_NAME")
CONTAINER_NAME = required_env("CONTAINER_NAME")

account_url = f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net"
blob_service_client = BlobServiceClient(account_url=account_url, credential=credential)

### --- Upload a blob ---
if len(sys.argv) != 2:
    raise SystemExit("Usage: python scripts/upload_blob_artifacts.py <file-path>")

source_path = Path(sys.argv[1])
if not source_path.is_file():
    raise FileNotFoundError(f"File not found: {source_path}")

blob_name = source_path.name
blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob_name)
with source_path.open("rb") as source_file:
    blob_client.upload_blob(source_file, overwrite=True)
print(f"Uploaded {source_path} as {blob_name}")

### --- Download it back ---
downloaded = blob_client.download_blob().readall()
print(f"Downloaded {blob_name} ({len(downloaded)} bytes)")

### --- List all blobs in the container ---
container_client = blob_service_client.get_container_client(CONTAINER_NAME)
print("\nBlobs in container:")
for blob in container_client.list_blobs():
    print(f"- {blob.name}")