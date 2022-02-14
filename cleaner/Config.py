

import os


conf = {
    "baseUrl": "https://code.siemens.com/api/v4/projects",
    "private_token": os.environ.get("private_token") or print("add private_token environment variable. Exiting...") and exit(1),
    "pipeline_url": "{}/{}/pipelines?updated_before=\"{}\"&order_by=updated_at&page={}&per_page=50", # GET methods
    "pipeline_url_v2": "{}/{}/pipelines?updated_before=\"{}\"&order_by=updated_at&page={}&updated_after=\"{}\"&per_page=50",
    "job_url": "{}/{}/pipelines/{}/jobs?include_retried=true&page={}&per_page=50", # GET method
    "artifact_delete_url": "{}/{}/jobs/{}/artifacts", # DELETE method
    "job_erase_url": "{}/{}/jobs/{}/erase",  # POST method
    "pipeline_delete_url": "{}/{}/pipelines/{}", # DELETE method

    "cooldown_seconds": 20
}

