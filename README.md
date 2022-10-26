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
- **Requirements**:
  - pip-22.3 
  - python>=3.8
1) clone the repo `git clone https://github.com/Nootka-io/wee-benchmarking-tool.git`
2) `cd` into the directory you cloned the repo to
3) create a venv `python3 -m venv venv`
4) activate venv `source venv/bin/activate`
5) `pip install -e .`

## Using `wee-cli`

**Usage**:

```console
$ wee-cli [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `list-extractors`: Print a list of all the available extractors.
* `run`: Run both the extractors and the evaluation...
* `run-eval`: Evaluate the results from an output...
* `run-extract`: Run the extractors and generate the outputs...

### `wee-cli list-extractors`

Print a list of all the available extractors.

**Usage**:

```console
$ wee-cli list-extractors [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `wee-cli run`

Run both the extractors and the evaluation scripts.

**Usage**:

```console
$ wee-cli run [OPTIONS] [OUTPUT_DIR]
```

**Arguments**:

* `[OUTPUT_DIR]`: the folder where the outputs will be saved and evaluations created from  [default: default]

**Options**:

* `--extractors TEXT`: which extractors your want to run. Must match the `name`. Use `list-extractors to view available extractors.`
* `--help`: Show this message and exit.

### `wee-cli run-eval`

Evaluate the results from an output directory.

**Usage**:

```console
$ wee-cli run-eval [OPTIONS] [OUTPUT_DIR]
```

**Arguments**:

* `[OUTPUT_DIR]`: the folder where the outputs were saved.  [default: default]

**Options**:

* `--extractors TEXT`: which extractors your want to run. Must match the `name`. Use `list-extractors to view available extractors.`
* `--help`: Show this message and exit.

### `wee-cli run-extract`

Run the extractors and generate the outputs to the specified output directory.

**Usage**:

```console
$ wee-cli run-extract [OPTIONS] [OUTPUT_DIR]
```

**Arguments**:

* `[OUTPUT_DIR]`: the folder where the outputs will be saved and evaluations created from  [default: default]

**Options**:

* `--extractors TEXT`: which extractors your want to run. Must match the `name`. Use `list-extractors to view available extractors.`
* `--extract-in-parallel`: whether to run the extractors in parallel with Dask  [default: False]
* `--help`: Show this message and exit.


## How to add extractors
Only one file needs to be added to `wee_cli/extractors/`. The title should be run_[THE_NAME_OF_THE_EXTRACTOR].py. Make sure to change the `name` parameter at the start of the class, and extend the `BaseExtractor` class implementing the `extract()` method.

**See**: [../wee_cli/extractors/](https://github.com/Nootka-io/wee-benchmarking-tool/tree/master/wee_cli/extractors/) for an examples

**ToDo:** add better documentation and examples

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