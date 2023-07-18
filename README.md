# DoomWolf

## Description

This was another attempt at teaching myself game programming. It doesn't hurt that I also happen to enjoy playing it and
my daughters are (currently) obsessed with it. This is inspired by and based on the work by
[Stanislov Petrov](https://github.com/StanislavPetrovV/DOOM-style-Game), after I watched his
[YouTub video](https://www.youtube.com/watch?v=ECqUrT7IdqQ) about building video games using PyGame. I was particularly
interested in the [Ray casting](https://en.wikipedia.org/wiki/Ray_casting) and
[Path finding](https://en.wikipedia.org/wiki/Pathfinding) algorithms. It also gave me much more insight as to what the
original C code was doing in the ['Wolfenstein'](https://github.com/id-Software/wolf3d) and
['DOOM'](https://github.com/id-Software/DOOM) games. Not to mention, I'm a sucker for nostalgia and video games from
my teenage years.

## But this mostly just looks like Stanislov's game

For now.

Again, I'm largely doing this for the learning experience and wanted a place to start, but already this codebase
improves on the original with the following:

- Better code organization and formatting and stronger type safety.
- Can fully control the game using keyboard only, keyboard and mouse, or gamepad.
- Weapon inventory system
- Fullscreen toggle
- Game pause
- Ability to screenshot
- Better error handling and asset existence checks
- More than one weapon
- User-definable weapons, enemies, level map and sprite map (documentation coming soon)
- Main menu and options screens
- Pause screen
- Map loading system

Future planned improvements:
- More maps!
- More weapons
- More enemies
- More sprites (static and animated)
- Level progression
- Difficulty levels
- Possible multiplayer

## Controls
- Keyboard
- - Player move: W, S, A, D
- - Head turn: Left/Right arrow keys
- - Fire: space bar
- - Pause: P
- - Toggle fullscreen: T
- - Quit/Exit: Esc
- - Weapon switch: Tab
- - Screenshot: M
- - Use/Interact: E
- Mouse
- - Head turn: mouse move left/right
- - Fire: Left mouse button
- Game pad/controller
- - Player move: D-pad
- - Head turn: Left/right bumpers
- - Fire: A
- - Weapon switch: B
- - Use/Interact: X
- - Pause: Start
- - Quit/Exit: Mode/Select

## Technology
This game was built in [Python](https://www.python.org/) using [PyGame](https://www.pygame.org/), which essentially is
a Python wrapper for [SDL](http://www.libsdl.org/). Generally, for performance reasons and stability reasons, I would
prefer to write games in a strongly-typed object-oriented language because I like type safety and Python certainly has
its place but is notoriously slower than more performant languages (like Rust, C, C++, etc). That being said, you can
get better type safety thanks to [mypy](https://mypy-lang.org/) and the newer features in Python 3.x, and we can speed
up performance using a number of other technologies such as [CPython](https://en.wikipedia.org/wiki/CPython) and the
like. But also, I'm starting to enjoy the ease, readability, and rapid pace of building the non-engine game logic in a
language like Python. I'm starting to have an appreciation for games that were built such that the engine is written in
a low-level language like C/C++ and the game logic is implemented using a high-level language like Python/Lua. Note:
while this game has an 'engine' package, it isn't an actual engine per se. The *real* engine is PyGame itself and my
engine package is more-or-less a wrapper around the pieces I care about and does the explicit work for managing the
different pieces of the game while allowing for extensibility.

## Requirements
- Python 3.x (tested with Python 3.10) (make sure you also have pip3)
- Pipenv
- PyGame

## OK, how do I run it?
First the prerequisites: If you haven't already, install pipenv:
```sh
pip install pipenv
```

Now install dependencies:
```sh
pipenv install --dev
```

Launch virtual environment:
```sh
pipenv shell
```

Now run it:
```sh
python main.py
```

## Debug
In order to see things like the tile map skeleton, player and enemy ray-casting and see the pathfinding algorithm in
action, you can change the DEBUG constant in `engine/constants.py` to `True` and then run the game.