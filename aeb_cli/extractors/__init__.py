import json
from pathlib import Path
import gzip
import time
import os


class BaseExtractor:

    name = 'base-extractor'

    def __init__(self, output_dir='default'):
        self.extracts = {}
        self.elapsed_time = 0
        self.output_dir = output_dir

    def __call__(self):
        for path in Path('datasets/scrappinghub_aeb/html').glob('*.html.gz'):
            with gzip.open(path, 'rt', encoding='utf8') as f:
                html = f.read()
            item_id = path.stem.split('.')[0]
            start = time.time()
            res = self.extract(html)
            self.elapsed_time += time.time() - start
            self.extracts[item_id] = {'articleBody': res}
        # write to json file
        self.write_to_json()

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
