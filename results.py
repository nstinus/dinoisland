#!/usr/bin/env python

import re, os
from numpy import mean, median, std

LOG_DIR="/tmp"
FILENAME_REGEX=re.compile("dino.(?P<version>.*-\d+-g\w+(-dirty)?).(?P<date>\d{8}_\d{6}).log")

class Run:
    def __init__(self, filename, version, date):
        self.filename = filename
        self.version = version
        self.date = date
        self.score = -1

    def parse(self):
        f = open(self.filename)
        for l in f.readlines():
            if "END" in l:
                for i in l.split():
                    if "score=" in i:
                        self.score = int(i.split("=")[1][:-1])
                    # if "best=" in i:
                    #    self.best = int(i.split("=")[1])
                break
        f.close()

    def __cmp__(self, other):
        return cmp(self.score, other.score)

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-p", "--pattern", dest="pattern", default=".*")
    (options, args) = parser.parse_args()

    version_pattern = re.compile(options.pattern)

    RUNS = dict()
    
    for f in os.listdir(LOG_DIR):
        m = FILENAME_REGEX.match(f)
        if m:
            k = m.group("version")
            if not RUNS.has_key(k):
                RUNS[k] = list()
            RUNS[k].append(Run(os.path.join(LOG_DIR, f), k, m.group("date")))
    
    print "%-20s    %4s    %7s  %15s    %7s    %7s    %7s" % ("version", "N#", "max", "date", "mean", "std", "median")
    lines = list()
    for version, runs in RUNS.iteritems():
        for i in range(len(runs)):
            runs[i].parse()
        runs =[r for r in runs if r.score != -1]
        if len(runs) == 0:
            continue
        M = max(runs)
        N = len(runs)
        med = median([i.score for i in runs])
        stddev = std([i.score for i in runs])
        avg = mean([i.score for i in runs])
        lines.append("%-20s    %4d    %7d  %15s    %7.0f    %7.0f    %7.0f" % (version, N, M.score, M.date, round(avg), round(stddev), round(med)))
    for l in sorted(lines):
        if version_pattern.match(l):
            print l
