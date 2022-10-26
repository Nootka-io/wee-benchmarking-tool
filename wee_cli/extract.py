from rich import print
from inspect import isclass
from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module


def get_extractors():
    # iterate through the modules in the current package
    package_dir = str(Path('wee_cli/extractors').resolve())

    for (_, module_name, _) in iter_modules([package_dir]):

        # import the module and iterate through its attributes
        module = import_module(f"wee_cli.extractors.{module_name}")

        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)

            if isclass(attribute) and 'Extract' in attribute_name and not attribute_name in ['BaseExtractor']:
                yield attribute

def list_available_extractors():
    extractors = [x.name for x in get_extractors()]
    return extractors

def extract(output_dir, extractors_to_run = None, extract_in_parallel = False):

    if not extractors_to_run:
        extractors_to_run = list_available_extractors()

    extractors = get_extractors()

    for extractor in extractors:
        if extractor.name in extractors_to_run:
            _run = extractor(output_dir, extract_in_parallel)
            _run()
            del _run

    return True

