import asyncio

import json

from rich.console import Console
from rich.table import Table

from cleaner.CleanupTask import close_session
from cleaner.Project import Project
from cleaner.start import starter
from cleaner.Config import conf
from datetime import datetime, timedelta
import argparse

projects: Project = []
task_file = None

def load_tasks():
    '''
    Load user provided task file into Project
    '''
    global projects, task_file

    if task_file == None:
        print("provide task file. Exiting...")
        exit(1)
    
    with open(task_file) as f:
        data = json.load(f)

    for t in data:
        artifact_expire = str((datetime.utcnow() - timedelta(days=t["artifacts"]["older_than"])).strftime('%Y-%m-%dT%H:%M:%SZ'))
        artficts_after = None
        if t.get("artifacts").get("newer_than") != None:
            artficts_after = str((datetime.utcnow() - timedelta(days=(t.get("artifacts").get("newer_than")))).strftime('%Y-%m-%dT%H:%M:%SZ'))
        log_expire = str((datetime.utcnow() - timedelta(days=t["logs"]["older_than"])).strftime('%Y-%m-%dT%H:%M:%SZ'))
        pipeline_expire = str((datetime.utcnow() - timedelta(days=t["pipelines"]["older_than"])).strftime('%Y-%m-%dT%H:%M:%SZ'))
        
        p = Project(t.get("id"), t.get("name"), artifact_expire, log_expire, pipeline_expire, artficts_after)

        projects.append(p)

async def checker():
    '''
    Checking if all tasks are done or not
    '''
    global projects
    while True:
        tasks = len(asyncio.all_tasks())
        if tasks != 1:
            await asyncio.sleep(2)
        else:
            break
    
    for p in projects:
        # print(p)
        visualize_results(p)

    await close_session()
    end =  datetime.now()

    print("Time taken: " + str(end - start) )

def parsing():
    '''
    Parsing user input task file
    '''
    global task_file
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file", help = "Provide configuration file", required=True)
    parser.add_argument("-c", "--cooldown-seconds", help = "each request randomly select 0 to x seconds as cooldown", required=False, default=20)
    args = parser.parse_args()

    task_file = args.file

    conf["cooldown_seconds"] = int(args.cooldown_seconds)

def visualize_results(project: Project):
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")

    table.add_column("Attribute")
    table.add_column("Value")

    table.add_row("Name", project.name)
    table.add_row("Id", str(project.id))
    table.add_row("Pipelines Scanned", str(project.pipelines_scanned))
    table.add_row("Jobs Scanned", str(project.jobs_scanned))
    table.add_row("Artifacts cleaned", str(project.artifact_space))
    table.add_row("Logs cleaned", str(project.logs_space))

    for key, values in project.calls.items():
        table.add_row("HTTP/" + str(key), str(values))
    console.print(table)
start = datetime.now()

parsing()

load_tasks()

event_loop = asyncio.get_event_loop()

for p in projects:
    event_loop.run_until_complete(starter(p))
    
event_loop.run_until_complete(checker())

