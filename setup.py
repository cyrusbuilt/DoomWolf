from distutils.core import setup

from main import TITLE
from main import VERSION
from main import __author__
from main import __author_email__


setup(
    name=TITLE,
    version=VERSION,
    author=__author__,
    author_email=__author_email__,
    packages=["engine", "enemy", "game", "maps", "screens", "sprite_object",
              "weapon"],
    include_package_data=True,
    license="LICENSE",
    description="Doom/Wolfenstein Hybrid First-Person Shooter",
    long_description=open("README.md").read(),
    requires=["pygame", "pygame_menu"],
)
