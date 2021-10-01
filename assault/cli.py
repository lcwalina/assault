import click
from .http import assault

@click.command()
@click.option("--requests", "-r", default=500, help="Number of requests")
@click.option("--concurrency", "-c", default=1, help="Number of concurrent requests")
@click.option("--json-file", "-j", default=None, help="Path to output json file")
@click.argument("url")
def cli(requests, concurrency, json_file, url):
    assault(url, requests, concurrency)


if __name__ == "__main__":
    cli()