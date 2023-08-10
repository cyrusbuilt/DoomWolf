#!/usr/bin/env sh

echo "Cleaning build directories..."
dist_path='dist'
if [ -d $dist_path ]; then
  echo "Removing directory '$dist_path' ..."
  rm -rf $dist_path
fi

egg_info='DoomWolf.egg-info'
if [ -d $egg_info ]; then
  echo "Removing directory '$egg_info' ..."
  rm -rf $egg_info
fi

build_path='build'
if [ -d $build_path ]; then
  echo "Removing directory '$build_path' ..."
  rm -rf $build_path
fi

echo "Done."
