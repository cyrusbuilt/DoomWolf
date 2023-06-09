VERSION = '1.0'
__author__ = 'Cyrus Brunner'
__author_email__ = 'cyrusbuilt@gmail.com'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2023, Cyrus Brunner'

if __name__ == '__main__':
    title = f'DoomWolf v{VERSION}'
    print(title)
    print(__copyright__)

    from game import run_doom_wolf
    run_doom_wolf(title)
