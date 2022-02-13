


class Project:

    def __init__(self, id, name, artifact_expire_timestamp, logs_expire_timestamp, pipeline_expire_timestamp, artifacts_after = None):
        self.id = id
        self.name = name
        self.artifact_expire_timestamp = artifact_expire_timestamp
        self.artifact_after = artifacts_after
        self.logs_expire_timestamp = logs_expire_timestamp
        self.pipeline_expire_timestamp = pipeline_expire_timestamp

        self.artifact_space: float = 0
        self.logs_space: float = 0
        self.calls = {}
        self.pipelines_scanned: int = 0
        self.jobs_scanned: int = 0


    def increase_pipelines_scanned(self, num: int):
        self.pipelines_scanned = self.pipelines_scanned + num
    
    def increase_jobs_scanned(self, num: int):
        self.jobs_scanned = self.jobs_scanned + num
    
    def add_artifact_space(self, space: float):
        self.artifact_space = self.artifact_space + space

    def add_logs_space(self, space: float):
        self.logs_space = self.logs_space + space

    def __str__(self):
        print(self.__dict__)
        return ""

    def get_id(self):
        return self.id

    def get_pipelines_before(self):
        return self.artifact_expire_timestamp
    