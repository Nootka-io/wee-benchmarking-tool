import json
from math import fsum
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
        with Pool(processes=os.cpu_count() - 1) as p:
            bagged = p.map(self.parallel_extract, sequence)
        self.elapsed_time = fsum(t for t, _ in bagged) / (os.cpu_count() - 1)
        self.extracts = {item['item_id']: {'articleBody': item['articleBody']} for _, item in bagged}

    def extract_w_daskbag(self):
        """
        runs the extracts in parallel using dask.
        """
        sequence = self.load_sequence()
        bagged = db.from_sequence(sequence).map(self.parallel_extract).compute(
            scheduler='processes', max_workers=os.cpu_count() - 1)
        self.elapsed_time = fsum(t for t, _ in bagged) / (os.cpu_count() - 1)
        self.extracts = {item['item_id']: {'articleBody': item['articleBody']} for _, item in bagged}

    def extract_sequentially(self):
        timings = []
        for path in Path('datasets/scrappinghub_aeb/html').glob('*.html.gz'):
            with gzip.open(path, 'rt', encoding='utf8') as f:
                html = f.read()
            item_id = path.stem.split('.')[0]
            start = time.process_time()
            res = self.extract(html)
            timings.append(time.process_time() - start)
            self.extracts[item_id] = {'articleBody': res if res else ' '}
        self.elapsed_time = fsum(timings)

    def parallel_extract(self, _x):
        html = _x['html']
        start = time.process_time()
        res = self.extract(html)
        time_elapsed = time.process_time() - start
        _x['articleBody'] = res if res else ' '
        return time_elapsed, _x

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
