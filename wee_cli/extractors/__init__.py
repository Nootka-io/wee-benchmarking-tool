import json
from pathlib import Path
import gzip
import time
import os
import dask.bag as db


class BaseExtractor:

    name = 'base-extractor'

    def __init__(self, output_dir='default', run_extracts_in_parallel = False):
        self.extracts = {}
        self.elapsed_time = 0
        self.output_dir = output_dir
        self.run_extracts_in_parallel = run_extracts_in_parallel

    def __call__(self):

        if self.run_extracts_in_parallel:
            self.extract_in_parallel()
        else:
            self.extract_sequentially()
        # write to json file
        self.write_to_json()

    def extract_in_parallel(self):
        """
        runs the extracts in parallel using dask.
        This isn't the most effient way with dask, but the sequence is loaded first to get the timings as close as possible
        :return:
        """
        sequence = []
        for path in Path('datasets/scrappinghub_aeb/html').glob('*.html.gz'):
            with gzip.open(path, 'rt', encoding='utf8') as f:
                html = f.read()
            item_id = path.stem.split('.')[0]
            sequence.append({
                'item_id': item_id,
                'html': html
            })
        start = time.time()
        bagged = db.from_sequence(sequence)\
            .map(self.parallel_extract)
        self.elapsed_time += time.time() - start
        bagged = bagged.compute()
        self.extracts = {item['item_id']:{'articleBody': item['articleBody']} for item in bagged}
        # breakpoint()

    def extract_sequentially(self):
        for path in Path('datasets/scrappinghub_aeb/html').glob('*.html.gz'):
            with gzip.open(path, 'rt', encoding='utf8') as f:
                html = f.read()
            item_id = path.stem.split('.')[0]
            start = time.time()
            res = self.extract(html)
            self.elapsed_time += time.time() - start
            self.extracts[item_id] = {'articleBody': res if res else ''}

    def parallel_extract(self, _x):
        html = _x['html']
        _x['articleBody'] = self.extract(html)
        return _x

    @staticmethod
    def extract():
        raise NotImplementedError

    def write_to_json(self):
        output = {
            'elapsed_time': self.elapsed_time,
            'extracts': self.extracts
        }
        directory = f"{Path('output')}/{self.output_dir}"
        file = f"{directory}/{self.name}.json"
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(file, 'w') as fp:
            json.dump(output, fp)
