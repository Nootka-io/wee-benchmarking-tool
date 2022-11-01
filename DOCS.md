# `wee-cli`

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

## `wee-cli list-extractors`

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
* `--backend [sequential|dask_bag|multiprocessingpool]`: which backend to run  [default: sequential]
* `--help`: Show this message and exit.

## `wee-cli run-eval`

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

## `wee-cli run-extract`

Run the extractors and generate the outputs to the specified output directory.

**Usage**:

```console
$ wee-cli run-extract [OPTIONS] [OUTPUT_DIR]
```

**Arguments**:

* `[OUTPUT_DIR]`: the folder where the outputs will be saved and evaluations created from  [default: default]

**Options**:

* `--extractors TEXT`: which extractors your want to run. Must match the `name`. Use `list-extractors to view available extractors.`
* `--backend [sequential|dask_bag|multiprocessingpool]`: which backend to run  [default: sequential]
* `--help`: Show this message and exit.
