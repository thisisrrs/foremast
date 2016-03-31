"""Entrypoint to Application Configuration preparer."""
import argparse
import logging

from .outputs import write_variables
from .prepare_configs import process_git_configs, process_runway_configs

LOG = logging.getLogger(__name__)


def main():
    """Append Application Configurations to a given file in INI format."""
    logging.basicConfig()

    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('-d',
                        '--debug',
                        action='store_const',
                        const=logging.DEBUG,
                        default=logging.INFO,
                        help='Set DEBUG output')
    parser.add_argument('-o',
                        '--output',
                        required=True,
                        help='Name of environment file to append to')
    parser.add_argument(
        '-t',
        '--token-file',
        help='File with GitLab API private token, required for --git-short')
    parser.add_argument(
        '-g',
        '--git-short',
        metavar='GROUP/PROJECT',
        required=True,
        help='Short name for Git, e.g. forrest/core, requires --token-file')
    parser.add_argument(
        '-r',
        '--runway-dir',
        help='Runway directory with app.json files, requires --git-short')
    args = parser.parse_args()

    LOG.setLevel(args.debug)
    logging.getLogger(__package__).setLevel(args.debug)

    if args.runway_dir:
        configs = process_runway_configs(runway_dir=args.runway_dir)
    else:
        if not args.token_file:
            raise SystemExit('Must provide private token file as well.')
        configs = process_git_configs(git_short=args.git_short,
                                      token_file=args.token_file)

    write_variables(app_configs=configs,
                    out_file=args.output,
                    git_short=args.git_short)


if __name__ == '__main__':
    main()
