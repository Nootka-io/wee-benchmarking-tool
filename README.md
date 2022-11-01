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

## Evaluating the Results
Wow! Here's my initial impression after writing this library to determine some issues I experienced running in parallel. Some extremly fast libraries slow down, and one of the slower ones, makes the biggest improvement. 

**Sequential Results**

Similarity Threshold Results - classified as successful if the similarity of the extraction was greater than 90% compared to 
the ground truth

| Library           | Accuracy | Precision | Recall | FScore | Mean Similarity | Items/sec |
|-------------------|----------|-----------|--------|--------|-----------------|-----------| 
| boilerpy3         | 0.4033   | 0.4033    | 0.4033 | 0.4033 | 0.7506          | 59.2786   |
| goose3            | 0.6796   | 0.6796    | 0.6796 | 0.6796 | 0.8344          | 9.817     |
| inscriptis        | 0.0331   | 0.0331    | 0.0331 | 0.0331 | 0.5092          | 73.4007   |
| news-please       | 0.5635   | 0.5635    | 0.5635 | 0.5635 | 0.8133          | 4.8152    |
| newspaper3k       | 0.7901   | 0.7901    | 0.7901 | 0.7901 | 0.8868          | 7.6203    |
| resiliparse-plain | 0.0718   | 0.0718    | 0.0718 | 0.0718 | 0.564           | 812.9227  |
| resiliparse       | 0.6298   | 0.6298    | 0.6298 | 0.6298 | 0.8819          | 514.2251  |
| trafilatura       | 0.5635   | 0.5635    | 0.5635 | 0.5635 | 0.8567          | 22.3564   |

Complex Score Results - comparing tokens from both ground truth and prediction

| Library           | Accuracy | Precision | Recall | FScore | Mean Similarity | Items/sec |
|-------------------|----------|-----------|--------|--------|-----------------|-----------|
| boilerpy3         | 0.6381   | 0.8412    | 0.8743 | 0.8373 | 0.7506          | 60.2163   |
| goose3            | 0.6276   | 0.9283    | 0.8561 | 0.8755 | 0.8344          | 9.919     |
| inscriptis        | 0.6706   | 0.4561    | 0.9711 | 0.5869 | 0.5092          | 75.6116   |
| news-please       | 0.638    | 0.9105    | 0.8952 | 0.8861 | 0.8133          | 4.9255    |
| newspaper3k       | 0.6443   | 0.9281    | 0.9139 | 0.9041 | 0.8868          | 7.6611    |
| resiliparse-plain | 0.6793   | 0.492     | 0.9965 | 0.6253 | 0.6054          | 769.1841  |
| resiliparse       | 0.6754   | 0.8529    | 0.9852 | 0.904  | 0.8819          | 504.2229  |
| trafilatura       | 0.6602   | 0.8975    | 0.9485 | 0.9113 | 0.8446          | 40.0767   |

**Parallel Results**

Metrics are the same, only timings change. Dask bag adds significant overhead when serializing the text, sometimes resulting in slower results than sequential. It's my recommendation to run in parallel with pythons multiprocessing pool, and break work in chunks or use a messaging queue to solve distributed computing.     


| Library           | Items/sec - dask bag | Items/sec - multiprocessing pool |
|-------------------|----------------------|----------------------------------|
| boilerpy3         | 59.3189              | 487.311                          |
| goose3            | 29.9498              | 62.1065                          |
| inscriptis        | 60.2938              | 515.984                          |
| news-please       | 15.3577              | 25.7767                          |
| newspaper3k       | 15.2595              | 23.5398                          |
| resiliparse-plain | 65.9997              | 1215.9166                        |
| resiliparse       | 68.0967              | 1076.61.48                       |
| trafilatura       | 45.1772              | 304.4185                         |

**Notes:**
- the items/sec metric will vary depending on available cores, memory, and more.
- thanks to [Phoerious](https://github.com/phoerious) for helping me work through some multiprocessing issues, https://github.com/chatnoir-eu/chatnoir-resiliparse/issues/23, resulting from dask in relation to the [resiliparse](https://github.com/chatnoir-eu/chatnoir-resiliparse) library, but affecting everything

**ToDo:** Provide more insights into the metrics and how the metrics are calculated. 


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
- structured data markup extraction benchmarks
- language extraction benchmarks
- product extraction benchmarks
- ability to run various extraction tests
- Support for adding different metrics easier
- support different dataset formats, like; prodigy, and label-studio
- parallel evaluation of results


## ToDos
- provide longer better real world examples 
- evaluate other metrics
- write tests
- package (on hold since newspaper is installed from git)
- support different dataset formats, like; prodigy, and label-studio
- run evaluations in parallel
- store evaluation results (likely in sqlite)
- how to support anything available in scehma.org markup, and throughput of any schema extractor. 
- export tables as MD
- get rid of goose3 terrible logging


## Inspired By:
- [Scrapinghub's Article Extraction Benchmark](https://github.com/scrapinghub/article-extraction-benchmark)
- [Adbar's Evaluation script in Trafilatura](https://github.com/adbar/trafilatura#evaluation-and-alternatives)