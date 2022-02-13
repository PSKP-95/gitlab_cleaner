
import asyncio
import logging

import aiohttp
from cleaner.Config import conf
from cleaner.CleanupTask import task, json_task
from cleaner.Project import Project


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('logs.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

headers = {
    'PRIVATE-TOKEN': conf.get("private_token")
}

def load_jobs(result):
    response: aiohttp.ClientResponse = result.result()[0]
    pages = int(response.headers["X-Total-Pages"])
    context = result.result()[1]
    project: Project = context.get("project")
    if context["load_all"] and pages > 1:
        for i in range(2, pages + 1):
            url = conf.get("job_url").format(conf.get("baseUrl"), project.id, context.get("pipeline_id"), i)
            t = task(url, headers, "GET", {}, {"type": "job", "load_all": False, "project": project, "pipeline_id": context.get("pipeline_id")})
            asyncio.create_task(t).add_done_callback(load_jobs)

    asyncio.create_task(json_task(response, context)).add_done_callback(load_job_json)

def load_job_json(result):
    response = result.result()[0]
    context = result.result()[1]
    project: Project = context.get("project")
    logging.info("Project: " + str(project.id) + " pipeline: " + str(context["pipeline_id"]))
    
    for res in response:

        logger.info("Project: " + str(project.id) + " Pipeline: " + str(context.get("pipeline_id")) + " Job: " + str(res["id"]))
        if len(res["artifacts"]) > 1:
            # deleting artifact
            for artifact in res["artifacts"]:
                if artifact["file_type"] != "trace":
                    project.add_artifact_space(artifact["size"])
            url = conf.get("artifact_delete_url").format(conf.get("baseUrl"), res["pipeline"]["project_id"], res["id"])
            t = task(url, headers, "DELETE", {}, {"type": "delete_job", "project": context.get("project"), "pipeline_id": res["pipeline"]["id"]})
            asyncio.create_task(t).add_done_callback(delete_artifact)
        
        project.increase_jobs_scanned(1)

def delete_artifact(result):
    logger.info(result.result())
