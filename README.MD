# Web Extraction Benchmark
A tool for evaluating extractions from webpages. 

## Installation

## Running the scripts
It's built with typer so:
- `python aeb_cli/main.py run new`
- `python aeb_cli/main.py --help`

## How to add extractors

## ToDos
- provide longer better real world examples - most samples are quite short, and goose has show to be faster than trafilutura in real world scenarios. 
- evaluate other metrics
- ability run tests in parallel - eg goose runs faster than trafilutura in dask 
- write tests
- package
- add license
- add author 
- support different dataset formats, like; prodigy, and label-studio
- when an article is skipped how is scoring affected