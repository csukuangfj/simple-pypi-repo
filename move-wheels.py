#!/usr/bin/env python3

# Copyright (c)  2021  Xiaomi Corporation (authors: Fangjun Kuang)

from pathlib import Path
from typing import Tuple

import argparse
import os
import shutil

import pyinotify


def get_args() -> Tuple[str, str]:
    '''Return a tuple (src_dir, dst_dir).
    '''
    parser = argparse.ArgumentParser(
        "Move wheels from src directory to dest directory")

    default_src = Path(os.getcwd()) / 'wheel'
    parser.add_argument('--src',
                        help='The source directory to be watched',
                        default=str(default_src))

    parser.add_argument('--dst',
                        required=True,
                        help='The dest directory to which *.whl files '
                        'in the source directory are moved')

    args = parser.parse_args()
    assert Path(args.src).is_dir(), f'src dir {args.src} does not exist'
    assert Path(args.dst).is_dir(), f'dst dir {args.dst} does not exist'
    return args.src, args.dst


def move(src_file: str, dst_dir: str):
    '''Move the soruce file to the given directory.

    Args:
      src_file:
        The source file.
      dst_dir:
        The destination directory.
    '''
    assert Path(src_file).is_file()
    assert Path(dst_dir).is_dir()
    name = Path(src_file).name
    shutil.move(src_file, f'{dst_dir}/{name}')


class EventHandler(pyinotify.ProcessEvent):
    def my_init(self, dst_dir: str):
        self.dst_dir = dst_dir

    def process_IN_CREATE(self, event):
        if Path(event.pathname).is_file() and event.pathname.endswith('.whl'):
            move(event.pathname, self.dst_dir)


if __name__ == '__main__':
    src, dst = get_args()

    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_CREATE

    handler = EventHandler(dst_dir=dst)
    notifier = pyinotify.Notifier(wm, handler)
    wdd = wm.add_watch(src, mask, rec=False)
    notifier.loop()
