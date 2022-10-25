# WEE (Web Extraction) Benchmarking Tool
A tool for evaluating extractions from webpages. Evaluate article, price, and language extractions from html.

# Features
- a simple and slick CLI built with [Typer](https://typer.tiangolo.com/)
- run & evaluate only the extractors your want
- Reduced boilerplate. extractors are autoloaded:
  - add new extractors with just a few lines of code
  - easily write custom extractors to benchmark
- benchmark extraction in parallel (with Dask) or sequentially (you maybe surprised how the throughput changes!)
- support for multiple methods of evaluating extractions
- supports for multiple types of extractions
  - Coming soon: Language benchmarks
  - Coming soon: Title benchmarks
  - Coming soon: Product benchmarks
- Coming soon: Support for custom datasets

## Installation
- Requirements:
  - pip-22.3 
  - python>=3.8
1) clone the repo ``
2) cd into the directory you cloned it to
3) create a venv `python3 -m venv venv`
4) activate venv `source venv/bin/activate`
5) `pip install -e .`

## Running the scripts
It's built with typer so:
- `python weeaeb_cli/main.py run new`
- `python aeb_cli/main.py --help`

## How to add extractors
Only one file needs to be added to `wee_cli/extractors/`. The title should be run_[THE_NAME_OF_THE_EXTRACTOR].py. Make sure to change the `name` parameter at the start of the class, and extend the `BaseExtractor` class implementing the `extract()` method.

See: [https://github.com//extractors/]() for an examples

ToDo: add better documentation and examples

## Roadmap
- language extraction benchmarks
- product extraction benchmarks
- ability to run various extraction tests
- Support for adding different metrics easier
- support different dataset formats, like; prodigy, and label-studio
- parallel evaluation of results


## ToDos
- provide longer better real world examples - most samples are quite short, and goose has show to be faster than trafilutura in real world scenarios. 
- evaluate other metrics
- write tests
- package
- add license
- add author 
- support different dataset formats, like; prodigy, and label-studio
- when an article is skipped how is scoring affected
- run evaluations in parallel
- store evaluation results
- how to support anything available in scehma.org markup, and throughput of any schema extractor. 

## Inspired By:
- [Scrapinghub's Article Extraction Benchmark](https://github.com/scrapinghub/article-extraction-benchmark)
- [Adbar's Evaluation script in Trafilatura](https://github.com/adbar/trafilatura#evaluation-and-alternatives)