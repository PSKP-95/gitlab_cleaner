
import asyncio
from cleaner.pipelines import load_pipelines
from cleaner.Config import conf
from cleaner.CleanupTask import task
from cleaner.Project import Project

headers = {
    'PRIVATE-TOKEN': conf.get("private_token")
}

async def starter(project: Project):
    url = conf.get("pipeline_url").format(conf.get("baseUrl"), project.get_id(), project.get_pipelines_before(), 1)
    if project.artifact_after != None:
        url = conf.get("pipeline_url_v2").format(conf.get("baseUrl"), project.get_id(), project.get_pipelines_before(), 1, project.artifact_after)
    t = task(url, headers, "GET", {}, {"type": "pipeline", "load_all": True, "project": project})
    asyncio.create_task(t).add_done_callback(load_pipelines)