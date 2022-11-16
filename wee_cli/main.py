import typer
from rich import print
from rich.table import Table
from enum import Enum
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from typing import Optional, List
import os

from wee_cli.evaluate import eval_results as evaluate
from wee_cli.extract import list_available_extractors, extract


app = typer.Typer()


class Backend(str, Enum):
    sequential = 'sequential'
    dask_bag = 'dask_bag'
    multiprocessingpool = 'multiprocessingpool'


@app.command()
def run(
    output_dir: Optional[str] = typer.Argument('default', help="the folder where the outputs will be saved and evaluations created from"),
    extractors: Optional[List[str]] = typer.Option(None, help="which extractors your want to run. Must match the `name`. Use `list-extractors to view available extractors.`"),
    backend: Backend = typer.Option(Backend.sequential, case_sensitive=False, help="which backend to run")
):
    """
    Run both the extractors and the evaluation scripts.
    """
    print('Running the complete extraction and evaluation')
    run_extract(output_dir, extractors, backend)
    run_eval(output_dir, extractors)


@app.command()
def run_extract(
    output_dir: Optional[str] = typer.Argument('default', help="the folder where the outputs will be saved and evaluations created from"),
    extractors: Optional[List[str]] = typer.Option(None, help="which extractors your want to run. Must match the `name`. Use `list-extractors to view available extractors.`"),
    backend: Backend = typer.Option(Backend.sequential, case_sensitive=False, help="which backend to run")
):
    """
    Run the extractors and generate the outputs to the specified output directory.
    """
    if output_dir == 'base':
        print('`base` is a protected output dir, input a different output-dir')
        raise typer.Exit()
    # ToDo: check if directory already exists and ask to overwrite
    if os.path.exists(f'./output/{output_dir}'):
        replace_output_dir = typer.confirm(f"`{output_dir}` already exists are you sure you want to replace it?", abort=True)

    # validate extractors
    if extractors:
        validate_extractors(extractors)

    what_runs = extractors if extractors else 'ALL'

    # response = extract(output_dir, extractors, extract_in_parallel)

    with Progress(
        SpinnerColumn(),
        TextColumn('[progress.description]{task.description}'),
        TimeElapsedColumn()
        # transient=True
    ) as progress:
        progress.add_task(description=f"Running `{what_runs}` extractors...", total=None)
        response = extract(output_dir, extractors, backend)
    print('[bold green]Done running extractors \u2714 [/bold green]')

@app.command()
def run_eval(
    output_dir: Optional[str] = typer.Argument('default', help="the folder where the outputs were saved."),
    extractors: Optional[List[str]] = typer.Option(None, help="which extractors your want to run. Must match the `name`. Use `list-extractors to view available extractors.`"),
):
    """
    Evaluate the results from an output directory.
    """
    # validate extractors
    if extractors:
        validate_extractors(extractors)

    what_runs = extractors if extractors else 'ALL'
    evaluate(output_dir, extractors)
    with Progress(
        SpinnerColumn(),
        TextColumn('[progress.description]{task.description}'),
        TimeElapsedColumn()
        # transient=True
    ) as progress:
        progress.add_task(description=f"Running `{what_runs}` evaluations...", total=None)
        response = evaluate(output_dir, extractors)

    print('[bold green]Done evaluating results \u2714 [/bold green]')
    print('Similarity Threshold Results - classified as successful if the similarity of the extraction was greater than 90% compared to the ground truth')
    s_table = Table('Library', 'Accuracy', 'Precision', 'Recall', 'FScore', 'Mean Similarity', 'End2End Throughput \n Items/sec', 'time on `extract()`')
    for k, v in response.items():
        s_table.add_row(
            k,
            str(round(v['similarity'].get('accuracy'), 4) if v['similarity'].get('accuracy') else None),
            str(round(v['similarity'].get('precision'), 4) if v['similarity'].get('precision') else None),
            str(round(v['similarity'].get('recall'), 4) if v['similarity'].get('recall') else None),
            str(round(v['similarity'].get('fscore'), 4) if v['similarity'].get('fscore') else None),
            str(round(v['similarity'].get('mean_similarity'), 4) if v['similarity'].get('mean_similarity') else None),
            str(round(v.get('items_sec'), 4) if v.get('items_sec') else None),
            str(round(v.get('time_on_extract'), 4) if v.get('time_on_extract') else None)
        )
    print(s_table)

    print('Complex Score Results - comparing tokens from both ground truth and prediction')
    c_table = Table('Library', 'Accuracy', 'Precision', 'Recall', 'FScore', 'Mean Similarity', 'End2End Throughput \n Items/sec', 'Extracted Throughput \n Items/sec')
    for k, v in response.items():
        c_table.add_row(
            k,
            str(round(v['complex'].get('accuracy'), 4) if v['complex'].get('accuracy') else None),
            str(round(v['complex'].get('precision'), 4) if v['complex'].get('precision') else None),
            str(round(v['complex'].get('recall'), 4) if v['complex'].get('recall') else None),
            str(round(v['complex'].get('fscore'), 4) if v['complex'].get('fscore') else None),
            str(round(v['similarity'].get('mean_similarity'), 4) if v['similarity'].get('mean_similarity') else None),
            str(round(v.get('items_sec'), 4) if v.get('items_sec') else None),
            str(round(v.get('ips_extraction'), 4) if v.get('ips_extraction') else None)
        )
    print(c_table)

    # ToDo: mean similarity doesn't take into account the number of extractions

@app.command()
def list_extractors():
    """
    Print a list of all the available extractors.
    """
    print(list_available_extractors())

def validate_extractors(extractors):
    unknown = list(set(extractors) - set(list_available_extractors()))
    if unknown:
        print(f'{unknown}, are not setup, please add them to extractors, or remove them from the `--extractors` argument. Hint: run `list-extractors` to view available')
        raise typer.Exit()

    return True

if __name__ == '__main__':
    app()
