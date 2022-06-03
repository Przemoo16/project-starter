import enum
import io
import logging
import pathlib
import shutil
import time
import typing
import zipfile

import boto3
from botocore import exceptions
from generate_tag import generate_tag, get_branch_id

log = logging.getLogger(__name__)

AWS_REGION = "eu-central-1"

DOCKER_REPO = "059132655198.dkr.ecr.eu-central-1.amazonaws.com/project-starter"
PROXY_CONTAINER_NAME = "proxy"
PROXY_DOCKER_IMAGE = PROXY_CONTAINER_NAME
BACKEND_CONTAINER_NAME = "backend"
BACKEND_DOCKER_IMAGE = BACKEND_CONTAINER_NAME
CELERY_CONTAINER_NAME = "celery"
CELERY_BEAT_CONTAINER_NAME = "celery-beat"

EBS_APP_NAME = "project-starter-{}-web"
EBS_ENV_NAME = "project-starter-{}-web"
APP_BUCKET = "elasticbeanstalk-eu-central-1-059132655198"

WORKSPACE_DIR = pathlib.Path("tmp/package")
CONFIG_DIR = pathlib.Path(__file__).parent.parent
DOCKERRUN_FILE = "Dockerrun.aws.json"

ALREADY_EXISTS_MESSAGE = "already exists"
UPDATE_WAIT_SECS = 5


class Status(enum.Enum):
    PROCESSED = "PROCESSED"
    READY = "Ready"


def get_ebs_application() -> tuple[str, str]:
    branch = get_branch_id()
    return EBS_APP_NAME.format(branch), EBS_ENV_NAME.format(branch)


def prepare_dockerrun(
    workspace_dir: pathlib.Path, config_dir: pathlib.Path, tag: str
) -> None:
    prepare_workspace(workspace_dir)
    replace_file_content(
        config_dir / DOCKERRUN_FILE,
        workspace_dir / DOCKERRUN_FILE,
        {
            "PROXY_CONTAINER_NAME": PROXY_CONTAINER_NAME,
            "PROXY_DOCKER_IMAGE": PROXY_DOCKER_IMAGE,
            "BACKEND_CONTAINER_NAME": BACKEND_CONTAINER_NAME,
            "BACKEND_DOCKER_IMAGE": BACKEND_DOCKER_IMAGE,
            "CELERY_CONTAINER_NAME": CELERY_CONTAINER_NAME,
            "CELERY_BEAT_CONTAINER_NAME": CELERY_BEAT_CONTAINER_NAME,
            "DOCKER_REPO": DOCKER_REPO,
            "DOCKER_TAG": tag,
        },
    )


def prepare_workspace(path: pathlib.Path) -> None:
    shutil.rmtree(path, ignore_errors=True)
    path.mkdir(parents=True)


def replace_file_content(
    source: pathlib.Path, destination: pathlib.Path, params: dict[str, str]
) -> None:
    source_text = source.read_text()
    replaced_content = source_text % params
    destination.write_text(replaced_content)


def zip_folder(folder: pathlib.Path) -> io.BytesIO:
    zipped_source = io.BytesIO()
    with zipfile.ZipFile(zipped_source, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for entry in folder.rglob("*"):
            if entry.is_file():
                zip_file.write(entry, entry.name)
    zipped_source.seek(0)
    return zipped_source


def generate_s3_file_name(app_name: str, version: str) -> str:
    return f"{app_name}/{version}.zip"


def upload_to_s3(source: io.BytesIO, s3_file_name: str, bucket_name: str) -> None:
    s3 = boto3.resource("s3")
    s3.Object(bucket_name.lower(), s3_file_name).put(Body=source)


def create_application_version(
    app_name: str, version: str, bucket_name: str, s3_file_name: str
) -> None:
    ebs = boto3.client("elasticbeanstalk", region_name=AWS_REGION)
    try:
        ebs.create_application_version(
            ApplicationName=app_name,
            VersionLabel=version,
            Description=version,
            SourceBundle={"S3Bucket": bucket_name, "S3Key": s3_file_name},
            AutoCreateApplication=True,
            Process=True,
        )
    except exceptions.ClientError as e:
        if ALREADY_EXISTS_MESSAGE in e.response["Error"]["Message"]:
            log.info("The application already exists")
        else:
            raise


def update_environment(app_name: str, env_name: str, version: str) -> None:
    ebs = boto3.client("elasticbeanstalk", region_name=AWS_REGION)
    wait_for_ready_to_update(ebs, app_name, version)
    ebs.update_environment(
        ApplicationName=app_name,
        EnvironmentName=env_name,
        VersionLabel=version,
    )
    wait_for_finish_updating(ebs, app_name, env_name)


def wait_for_ready_to_update(ebs: typing.Any, app_name: str, version: str) -> None:
    while True:
        status = ebs.describe_application_versions(
            ApplicationName=app_name, VersionLabels=[version]
        )["ApplicationVersions"][0]["Status"]
        if status == Status.PROCESSED.value:
            return
        log.info("Waiting for ready to update. Status: %r", status)
        time.sleep(UPDATE_WAIT_SECS)


def wait_for_finish_updating(ebs: typing.Any, app_name: str, env_name: str) -> None:
    while True:
        status = ebs.describe_environments(
            ApplicationName=app_name, EnvironmentNames=[env_name]
        )["Environments"][0]["Status"]
        if status != Status.READY.value:
            return
        log.info("Waiting for finished updating. Status: %r", status)
        time.sleep(UPDATE_WAIT_SECS)


def deploy() -> None:
    app_name, env_name = get_ebs_application()
    log.info("EBS application name: %r, EBS application env: %r", app_name, env_name)

    tag = generate_tag()
    log.info("Generated tag: %r", tag)

    workspace_dir = WORKSPACE_DIR
    prepare_dockerrun(workspace_dir, CONFIG_DIR, tag)
    log.info("Prepared Dockerrun")

    s3_file_name = generate_s3_file_name(app_name, tag)
    log.info("Generated s3 file name: %r", s3_file_name)

    zipped_source = zip_folder(workspace_dir)
    log.info("Zipped configuration")

    app_bucket = APP_BUCKET
    upload_to_s3(zipped_source, s3_file_name, app_bucket)
    log.info("Uploaded source file to the s3")

    create_application_version(app_name, tag, app_bucket, s3_file_name)
    update_environment(app_name, env_name, tag)
    log.info("Updated environment")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    deploy()
