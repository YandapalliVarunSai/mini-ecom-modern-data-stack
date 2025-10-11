# upload_to_azure.py
import os
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from azure.storage.blob import BlobServiceClient

# ====== CONFIG ======
# Full container SAS URL you shared (keep the leading '?...' in token)
AZURE_CONTAINER_SAS_URL = os.getenv(
    "AZURE_CONTAINER_SAS_URL",
    "https://ecomdatastack.blob.core.windows.net/landing?sp=rwl&st=2025-10-05T16:20:08Z&se=2026-02-11T01:35:08Z&spr=https&sv=2024-11-04&sr=c&sig=mosLnzfS8212w66qxjj8ALxV5afHOucIXWqapZo0sVY%3D"
)

DATA_DIR = Path("../data_csv")
FILES = ["customers.csv", "products.csv", "orders.csv", "order_items.csv"]

def main():
    parsed = urlparse(AZURE_CONTAINER_SAS_URL)
    account_url = f"https://{parsed.netloc}"
    container_name = parsed.path.strip("/")

    # Build credential from query string (include leading '?')
    qs = f"?{parsed.query}"

    print(f"[INFO] Uploading to container: {container_name} @ {account_url}")
    bsc = BlobServiceClient(account_url=account_url, credential=qs)
    container = bsc.get_container_client(container_name)

    for fname in FILES:
        fpath = DATA_DIR / fname
        if not fpath.exists():
            print(f"[SKIP] {fname} not found")
            continue
        with open(fpath, "rb") as f:
            print(f"[UP] {fname} ...")
            container.upload_blob(name=fname, data=f, overwrite=True)
            print(f"[OK] {fname} uploaded")

if __name__ == "__main__":
    main()
