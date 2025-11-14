#!/usr/bin/env python3
import requests
import json
import re
import sys
from urllib3.exceptions import NotOpenSSLWarning
import warnings

warnings.simplefilter('ignore', NotOpenSSLWarning)

BASE_URL = "https://catalog.redhat.com/api/containers/v1"
REPO_PATH = "rhbk/keycloak-rhel9"
STREAM_REGEX = re.compile(r"^\d+\.\d+$")

def get_repository(repo_path):
    url = f"{BASE_URL}/repositories/registry/registry.access.redhat.com/repository/{repo_path}"
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        data = r.json()
    except requests.RequestException as e:
        print(f"HTTP error fetching repository: {e}", file=sys.stderr)
        return None
    except ValueError:
        print(f"Error: Response is not JSON: {r.text}", file=sys.stderr)
        return None
    if not data or "_id" not in data:
        print(f"Error: Unexpected repository response: {json.dumps(data, indent=2)}", file=sys.stderr)
        return None
    return data

def get_images(repo):
    report = []
    streams_seen = set()
    for stream in repo.get("content_stream_grades", []):
        tag = stream.get("tag")
        if not tag or not STREAM_REGEX.match(tag):
            continue
        if tag in streams_seen:
            continue
        image_ids = stream.get("image_ids", [])
        if not image_ids:
            continue
        vcs_ref = None
        published_date = None
        image_id = image_ids[0]["id"]
        image_url = f"{BASE_URL}/images/id/{image_id}"
        try:
            r = requests.get(image_url, timeout=20)
            r.raise_for_status()
            image_data = r.json().get("data", {})
            vcs_ref = image_data.get("vcs_ref")
            published_date = image_data.get("published_date")
        except Exception as e:
            print(f"Warning: Failed to fetch image {image_id}: {e}", file=sys.stderr)
        report.append({
            "contentStream": tag,
            "vcsRef": vcs_ref or "",
            "publishedDate": published_date or "",
            "freshnessGrade": stream.get("grade", "")
        })
        streams_seen.add(tag)
    return report

def main():
    repo = get_repository(REPO_PATH)
    if not repo:
        print("Failed to fetch repository metadata. Exiting.", file=sys.stderr)
        sys.exit(1)
    report = get_images(repo)
    print(json.dumps(report, indent=4))

if __name__ == "__main__":
    main()
