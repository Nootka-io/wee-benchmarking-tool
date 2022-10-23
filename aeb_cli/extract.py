from rich import print


def extract(output_dir):
    # ToDo: autoload these
    # ToDo: add config option for which to run

    from extractors.run_goose import Goose3Extract
    g_run = Goose3Extract(output_dir)
    g_run()

    from extractors.run_trafilatura import TrafilaturaExtract
    t_run = TrafilaturaExtract(output_dir)
    t_run()

    from extractors.run_resiliparse import ResiliparseExtract
    rp_run = ResiliparseExtract(output_dir)
    rp_run()

    from extractors.run_newspaper3k import Newspaper3kExtract
    np_run = Newspaper3kExtract(output_dir)
    np_run()

    from extractors.run_boilerpy3 import BoilerPy3Extract
    bp_run = BoilerPy3Extract(output_dir)
    bp_run()

    return True

