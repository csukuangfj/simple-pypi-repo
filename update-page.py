#!/usr/bin/env python3

# Copyright (c)  2021  Xiaomi Corporation (authors: Fangjun Kuang)

from pathlib import Path
from typing import List

import argparse
import glob
import os

import pyinotify


def get_args() -> str:
    parser = argparse.ArgumentParser(
        'Update index.html in the dst dir whenever a wheel '
        'file is added to the directory dst/whl')

    parser.add_argument('--dst',
                        required=True,
                        help='The dest directory where index.html is placed')

    args = parser.parse_args()
    assert Path(args.dst).is_dir(), f'dst dir {args.dst} does not exist'
    return args.dst


def generate_links(files: List[str]) -> str:
    ans = ''
    for f in files:
        ans += f'<a href="{f}">{f}</a><br/>\n'
    return ans


def generate_html(links: str):
    ans = '<html><head><head/>\n'
    ans += '<body>\n'
    ans += links
    ans += '\n'
    ans += '</body>\n'
    ans += '</html>'
    return ans


def update_page(dst_dir: str):
    wheel_dir = Path(dst_dir) / 'whl'
    wheels = glob.glob(f'{wheel_dir}/*.whl')
    files = []
    basename = Path(wheel_dir).name
    for f in wheels:
        name = Path(f).name
        files.append(f'{basename}/{name}')
    files.sort()
    links = generate_links(files)
    html = generate_html(links)
    f = Path(dst_dir) / 'index.html'
    f.write_text(html)


class EventHandler(pyinotify.ProcessEvent):
    def my_init(self, dst_dir: str):
        self.dst_dir = dst_dir

    def process_IN_CREATE(self, event):
        if Path(event.pathname).is_file() and event.pathname.endswith('.whl'):
            update_page(self.dst_dir)

    def process_IN_DELETE(self, event):
        if Path(event.pathname).is_file() and event.pathname.endswith('.whl'):
            update_page(self.dst_dir)


if __name__ == '__main__':
    dst = get_args()
    update_page(dst)

    wm = pyinotify.WatchManager()
    mask = pyinotify.IN_CREATE | pyinotify.IN_DELETE

    handler = EventHandler(dst_dir=dst)
    notifier = pyinotify.Notifier(wm, handler)
    wdd = wm.add_watch(f'{dst}/whl', mask, rec=False)
    notifier.loop()
