from typing import Tuple

import click

from slc_ci_setup.cli.cli import cli


@cli.command()
@click.option('--flavor-root-path', required=True, multiple=True,
              type=click.Path(file_okay=False, dir_okay=True, exists=True),
                 help="Path where script language container flavors are located.")
@click.option('--output-file', type=click.Path(file_okay=True, dir_okay=False, exists=False, writable=True),
              default="buildspec.yaml",
                 help="Path where script language container flavor are located.")
def build_test_container(
        flavor_root_path: str,
        output_file: Tuple[str, ...],
        ):
    """
    This command generates the buildspec file for AWS CodeBuild based on the flavors located in path "flavor_root_path".
    """
    print(f"Generating...{output_file} from {flavor_root_path}")

