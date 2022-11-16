import json
from pathlib import Path
import gzip
import time
import os
import dask.bag as db


class BaseExtractor:

    name = 'base-extractor'

    def __init__(self, output_dir='default', backend = 'sequential'):
        self.extracts = {}
        self.elapsed_time = 0
        self.output_dir = output_dir
        self.backend = backend

    def __call__(self):

        if self.backend == 'sequential':
            self.extract_sequentially()
        elif self.backend == 'multiprocessingpool':
            self.extract_w_multiprocessingpool()
        elif self.backend == 'dask_bag':
            self.extract_w_daskbag()
        # write to json file
        self.write_to_json()

    def load_sequence(self):
        sequence = []
        for path in Path('datasets/scrappinghub_aeb/html').glob('*.html.gz'):
            with gzip.open(path, 'rt', encoding='utf8') as f:
                html = f.read()
            item_id = path.stem.split('.')[0]
            sequence.append({
                'item_id': item_id,
                'html': html
            })
        return sequence

    def extract_w_multiprocessingpool(self):
        """
        runs the extracts in parallel using python multiprocessingpool.
        """
        sequence = self.load_sequence()
        from multiprocessing import Pool
        start = time.perf_counter()
        with Pool() as p:
            bagged = p.map(self.extract_wrapped, sequence)
        self.elapsed_time = time.perf_counter() - start
        self.extracts = {item['item_id']: {'articleBody': item['articleBody']} for item in bagged}

    def extract_w_daskbag(self):
        """
        runs the extracts in parallel using dask.
        """
        sequence = self.load_sequence()
        start = time.perf_counter()
        bagged = db.from_sequence(sequence)\
            .map(self.extract_wrapped)
        bagged = bagged.compute()
        self.elapsed_time = time.perf_counter() - start
        self.extracts = {item['item_id']:{'articleBody': item['articleBody']} for item in bagged}

    def extract_sequentially(self):
        sequence = self.load_sequence()
        extracted = []
        start = time.perf_counter()
        for item in sequence:
            extracted.append(self.extract_wrapped(item))
        self.elapsed_time += time.perf_counter() - start
        self.extracts = {item['item_id']: {'articleBody': item['articleBody']} for item in extracted}

    def extract_wrapped(self, _x):
        html = _x['html']
        res = self.extract(html)
        _x['articleBody'] = res if res else ' '
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
