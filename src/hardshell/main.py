#########################################################################################
# Imports
#########################################################################################
import click

from src.hardshell import __version__
from src.hardshell.scan import start_scanner


# Package Version
@click.version_option(version=__version__)


# Base Group
@click.group()
def cli():
    pass


# System Group
@cli.group(name="system")
def system_cli():
    pass


# Audit Command
@system_cli.command()
def audit():
    click.echo(click.style("System Audit", fg="blue"))
    start_scanner()


# Harden Command
@system_cli.command()
@click.confirmation_option()
def harden():
    print("System Harden")


# Config Group
@cli.group()
def config():
    pass


@config.command()
@click.confirmation_option()
def generate():
    print("Config Generate")


def main():
    cli()


if __name__ == "__main__":
    main()
