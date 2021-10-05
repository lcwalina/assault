import click
import json
import sys
from typing import TextIO

from .http import assault
from .stats import Results


@click.command()
@click.option("--requests", "-r", default=500, help="Number of requests")
@click.option("--concurrency", "-c", default=1, help="Number of concurrent requests")
@click.option("--json-file", "-j", default=None, help="Path to output json file")
@click.argument("url")
def cli(requests, concurrency, json_file, url):
    output_file = None
    if json_file:
        try:
            output_file = open(json_file, 'w')
        except:
            print(f"Unable to open file {json_file}")
            sys.exit(1)

    total_time, requests_dict = assault(url, requests, concurrency)
    results = Results(total_time, requests_dict)
    display(results, output_file)


def display(results: Results, json_file: TextIO):
    if json_file:
        json.dump(
            {
                "successful_requests": results.successful_requests(),
                "slowest": results.slowest(),
                "fastest": results.fastest(),
                "average_time": results.average_time(),
                "total_time": results.total_time,
                "requests_per_minute": results.requests_per_minute(),
                "requests_per_second": results.requests_per_second()
            },
            json_file
        )
        json_file.close()
        print(".... Done!")
    else:
        print(
            ".... Done!\n"
            "--- Results ---\n"
            f"Successful requests {results.successful_requests()}\n"
            f"Slowest             {results.slowest():.2f}s\n"
            f"Fastest             {results.fastest():.2f}s\n"
            f"Average             {results.average_time():.2f}s\n"
            f"Total time          {results.total_time:.2f}s\n"
            f"Requests Per Minute {results.requests_per_minute()}\n"
            f"Requests Per Second {results.requests_per_second()}"
        )
