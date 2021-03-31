from invoke import task

@task
def start(ctx):
    ctx.run("python3 src/index.py")

@task
def build(ctx):
    ctx.run("python3 src/build.py")

@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest")

@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html")