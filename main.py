import click
import os


VERSION = '1.0'
TITLE = 'DoomWolf'
__author__ = 'Cyrus Brunner'
__author_email__ = 'cyrusbuilt@gmail.com'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2023, Cyrus Brunner'


def test_the_map(map_path: str):
    if not os.path.exists(map_path):
        print(f'ERROR: Map file not found: {map_path}')
        quit()

    from game import test_map
    test_map(map_path)


@click.command()
@click.version_option(VERSION, prog_name='DoomWolf')
@click.option('--test_map', required=False, type=click.Path(),
              help='Test the specified map.')
def main(test_map):
    title = f'{TITLE} v{VERSION}'
    print(title)
    print(__copyright__)
    if test_map:
        test_the_map(test_map)
    else:
        from game import run_doom_wolf
        run_doom_wolf(title)


if __name__ == '__main__':
    main()
