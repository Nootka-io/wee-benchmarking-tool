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
| boilerpy3         | 0.4033   | 0.4033    | 0.4033 | 0.4033 | 0.7506          | 57.5429   |
| goose3            | 0.6796   | 0.6796    | 0.6796 | 0.6796 | 0.8344          | 9.8552    |
| inscriptis        | 0.0331   | 0.0331    | 0.0331 | 0.0331 | 0.5092          | 74.6064   |
| news-please       | 0.558    | 0.558     | 0.558  | 0.558  | 0.812           | 4.8268    |
| newspaper3k       | 0.7845   | 0.7845    | 0.7845 | 0.7845 | 0.8855          | 7.6327    |
| resiliparse-plain | 0.0884   | 0.0884    | 0.0884 | 0.0884 | 0.6054          | 776.8351  |
| resiliparse       | 0.6298   | 0.6298    | 0.6298 | 0.6298 | 0.8819          | 505.9411  |
| trafilatura       | 0.5304   | 0.5304    | 0.5304 | 0.5304 | 0.8446          | 36.6354   |



Complex Score Results - comparing tokens from both ground truth and prediction

| Library           | Accuracy | Precision | Recall | FScore | Mean Similarity | Items/sec |
|-------------------|----------|-----------|--------|--------|-----------------|-----------|
| boilerpy3         | 0.6381   | 0.8412    | 0.8743 | 0.8373 | 0.7506          | 57.5429   |
| goose3            | 0.6276   | 0.9283    | 0.8561 | 0.8755 | 0.8344          | 9.8552    |
| inscriptis        | 0.6706   | 0.4561    | 0.9711 | 0.5869 | 0.5092          | 74.6064   |
| news-please       | 0.638    | 0.9105    | 0.8952 | 0.8861 | 0.8133          | 4.8268    |
| newspaper3k       | 0.6443   | 0.9281    | 0.9139 | 0.9041 | 0.8868          | 7.6327    |
| resiliparse-plain | 0.6793   | 0.492     | 0.9965 | 0.6253 | 0.6054          | 776.8351  |
| resiliparse       | 0.6754   | 0.8529    | 0.9852 | 0.904  | 0.8819          | 505.9411  |
| trafilatura       | 0.6602   | 0.8975    | 0.9485 | 0.9113 | 0.8446          | 36.6354   |

**Parallel Results**

Metrics are the same, only timings change.      


| Library           | Items/sec - dask bag | Items/sec - multiprocessing pool |
|-------------------|----------------------|----------------------------------|
| boilerpy3         | 58.7689              | 378.1217                         |
| goose3            | 29.6042              | 59.5797                          |
| inscriptis        | 59.1145              | 421.9863                         |
| news-please       | 15.1085              | 24.9134                          |
| newspaper3k       | 14.3891              | 23.7028                          |
| resiliparse-plain | *64.1965*            | *804.3277*                       |
| resiliparse       | 63.8425              | 801.3418                         |
| trafilatura       | 43.1901              | 263.4183                         |

**Notes:**
- the items/sec metric will vary depending on available cores, memory, and more.
- timings are "wall clocks" and purposely include overhead of the frameworks and serialization times. Different methods distributing the work in parallel the work can have different results. Eg, chunking the data or loading forma shared memory space. It's not ment to profile the inner workings of the frameworks, running a library like [scalene](https://github.com/plasma-umass/scalene) is recommended for that, and an excellent tool for profiling python apps.  
- Dask bag adds significant overhead. It's not clear to me at this time if this is a result of overhead from the use of `concurrent.futures.ProcessPoolExecutor` under the hood or dask directly.
  - sometimes this can result in slower results than sequential. It's my recommendation to run in parallel with pythons multiprocessing pool, and break work in chunks or use a messaging queue to solve distributed computing. 
- Multiprocessing pool is always faster than dask in these benchmarks but may have some memory issues that are not apparent here. They are out side the scope of this article but take a look at this, https://luis-sena.medium.com/understanding-and-optimizing-python-multi-process-memory-management-24e1e5e79047, blog post for a better understanding and the official docs, https://docs.python.org/3/library/multiprocessing.shared_memory.html.

**ToDo:** Provide more insights into the metrics and how the metrics are calculated. 


## Using `wee-cli`

**Quickstart:**
- `wee-cli run` - this will run extractions and evaluations sequentially and output the results to the terminal. 

See [DOCS.md](https://github.com/Nootka-io/wee-benchmarking-tool/blob/main/DOCS.md) for the complete typer CLI documentation. or use `wee-cli --help`

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
