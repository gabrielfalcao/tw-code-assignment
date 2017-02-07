# -*- coding: utf-8 -*-
import io
import os
import argparse

from tw_conference_manager.models import TalkList
from tw_conference_manager.models import ConferenceTrackManager


def main():
    parser = argparse.ArgumentParser(description='TW Conference Track Manager')
    parser.add_argument(
        'textfile',
        help='the path to a text file',
    )
    parser.add_argument(
        '-n', '--name',
        default='TWConf',
        help='the path to a text file'
    )
    args = parser.parse_args()

    if os.path.isfile(args.textfile):
        text = io.open(args.textfile).read()
    else:
        print "the given file does not exist:", args.textfile
        raise SystemExit(1)

    conference = ConferenceTrackManager(args.name)

    talks = TalkList.from_text(text)
    conference.allocate_talks(talks)

    print "\n".join(conference.to_lines())


if __name__ == '__main__':
    main()
