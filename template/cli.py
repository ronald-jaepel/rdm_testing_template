import os
import sys
from pathlib import Path

import click

sys.path.append(Path(os.path.abspath(__file__)).parent.parent.as_posix())

from template import main


@click.command()
@click.option("--options")
def run_main(options=None):
    """
    Setup and run an optimization based on the provided parameters.

    Parameters:
        options:
    """

    main(options, repo_path=os.path.abspath(__file__))


if __name__ == '__main__':
    run_main()
