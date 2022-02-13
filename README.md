# Gitlab Cleaner

Small utility to clean artifacts, logs & pipelines in gitlab. This is asynchronous program to make it faster.

## How to use?

Just clone repo & create configuration file as below. Set environment variable `private_token` (for accessing gitlab projects). 

```sh
python main.py --file <conf_file>
```

## To Do

- [x] Load pipelines & jobs
- [x] Clean artifacts
- [ ] Erase jobs
- [ ] Delete pipeline

## Conf

All numbers are in days. `older_than` means all objects older than x days while `newer_than` means all objects updated after current time minus y days.

```json
[
    {
        "id": 12345,
        "name": "Project 1",
        "artifacts": {
            "older_than": 1,
            "newer_than": 7  // newer_than > older_than
        },
        "logs": {
            "older_than": 300
        },
        "pipelines": {
            "older_than": 1000
        }
    },
    {
        "id": 987654,
        "name": "project2",
        "artifacts": {
            "older_than": 1 // all pipelines will be scanned
        },
        "logs": {
            "older_than": 300
        },
        "pipelines": {
            "older_than": 1000
        }
    }
]
```