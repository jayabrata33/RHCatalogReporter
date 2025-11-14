# RHCatalogReporter

RHCatalogReporter is a Python tool that accesses the Red Hat Ecosystem Catalog and generates a report of the most recent container images for each content stream of a given repository. This project focuses on the rhbk/keycloak-rhel9 repository, but can be adapted for other Red Hat container repositories.

# Features

Fetches repository metadata from the Red Hat Ecosystem Catalog.

Extracts content streams and their latest container images.

Collects image information including:

contentStream – the content stream tag (e.g., 26.0)

vcsRef – the version control reference of the image

publishedDate – when the image was published

freshnessGrade – Red Hat's grade for the image freshness

Generates a JSON report suitable for further automation or analysis.

Example report entry:

{
    "contentStream": "26.0",
    "vcsRef": "84d4042f71c665c0636aa5ffda537f52c21aa06c",
    "publishedDate": "2024-11-13T14:10:23+00:00",
    "freshnessGrade": "A"
}


# Requirements

Python 3.9+

requests library

Install dependencies with:

pip3 install requests

Note: On macOS, Python may be compiled with LibreSSL instead of OpenSSL. The script suppresses related warnings, but upgrading to OpenSSL 1.1.1+ is recommended for full compatibility.

# Usage

Clone or download the repository.

Run the script:

python3.11 get_image_report.py > keycloak_report.json

The script will output a JSON report to keycloak_report.json.

Logs and warnings are printed to standard error, so only the JSON report is saved to the file.

# Output

The generated JSON contains an array of objects, one per content stream:

[
    {
        "contentStream": "26.0",
        "vcsRef": "84d4042f71c665c0636aa5ffda537f52c21aa06c",
        "publishedDate": "2024-11-13T14:10:23+00:00",
        "freshnessGrade": "A"
    },
    {
        "contentStream": "26.2",
        "vcsRef": "68efde1df015dac44fcd80f4",
        "publishedDate": "2024-12-01T12:00:00+00:00",
        "freshnessGrade": "B"
    }
]

References

Red Hat Ecosystem Catalog API: https://catalog.redhat.com/api/containers/docs/

API UI / Swagger: https://catalog.redhat.com/api/containers/v1/ui/