import pathlib
import subprocess
from importlib.metadata import version
from invoke import task
from TerraformLibrary import terraformlibrary

ROOT = pathlib.Path(__file__).parent.resolve().as_posix()
VERSION = version("robotframework-terraformlibrary")

@task
def utests(context):
    cmd = [
        "coverage",
        "run",
        "--source=TerraformLibrary",
        "-p",
        "-m",
        "pytest",
        f"{ROOT}/utest",
    ]
    subprocess.run(" ".join(cmd), shell=True, check=True)

@task
def atests(context):
    cmd = [
        "coverage",
        "run",
        "--source=TerraformLibrary",
        "-p",
        "-m",
        "robot",
        "--loglevel=TRACE:DEBUG",
        "--outputdir=./reports",
        f"{ROOT}/atest",
    ]
    subprocess.run(" ".join(cmd), shell=True, check=True)

@task(utests, atests)
def tests(context):
    subprocess.run("coverage combine", shell=True, check=False)
    subprocess.run("coverage report", shell=True, check=False)
    subprocess.run("coverage html", shell=True, check=False)

@task
def libdoc(context):
    print(f"Generating libdoc for library version {VERSION}")
    target = f"{ROOT}/docs/terraformlibrary.html"
    cmd = [
        "python",
        "-m",
        "robot.libdoc",
        "-n TerraformLibrary",
        f"-v {VERSION}",
        "TerraformLibrary",
        target,
    ]
    subprocess.run(" ".join(cmd), shell=True, check=False)

@task
def readme(context):
    with open(f"{ROOT}/docs/README.md", "w", encoding="utf-8") as readme:
        doc_string = terraformlibrary.__doc__
        readme.write(str(doc_string))