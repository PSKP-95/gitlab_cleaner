
import asyncio
import logging

import aiohttp
from cleaner.Config import conf
from cleaner.CleanupTask import task
from cleaner.CleanupTask import json_task
from cleaner.Project import Project
from cleaner.jobs import load_jobs


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('logs.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

headers = {
    'PRIVATE-TOKEN': conf.get("private_token")
}

def load_pipelines(result):
    response: aiohttp.ClientResponse = result.result()[0]
    pages = int(response.headers["X-Total-Pages"])
    context = result.result()[1]
    project: Project = context.get("project")
    logging.info("project: " + str(project.id))
    if context["load_all"] and pages > 1:
        for i in range(2, pages + 1):
            url = conf.get("pipeline_url").format(conf.get("baseUrl"), project.get_id(), project.get_pipelines_before(), i)
            if project.artifact_after != None:
                url = conf.get("pipeline_url_v2").format(conf.get("baseUrl"), project.get_id(), project.get_pipelines_before(), i, project.artifact_after)
            t = task(url, headers, "GET", {}, {"type": "pipeline", "load_all": False, "project": project})
            asyncio.create_task(t).add_done_callback(load_pipelines)

    asyncio.create_task(json_task(response, context)).add_done_callback(load_pipeline_json)

def load_pipeline_json(result):
    response = result.result()[0]
    context = result.result()[1]
    project: Project = context.get("project")
    logger.info("Project:" + str(project.id))
    for res in response:
        logger.info("Project: " + str(project.id) + " Pipeline: " + str(res["id"]))
        url = conf.get("job_url").format(conf.get("baseUrl"), res["project_id"], res["id"], 1)
        t = task(url, headers, "GET", {}, {"type": "job", "load_all": True, "project": project, "pipeline_id": res["id"]})
        asyncio.create_task(t).add_done_callback(load_jobs)

        project.increase_pipelines_scanned(1)