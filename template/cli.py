import click

from template import main


@click.command()
@click.option("options")
def run_main(options=None):
    """
    Setup and run an optimization based on the provided parameters.

    Parameters:
        options:
    """

    main(options)


if __name__ == '__main__':
    run_main()
