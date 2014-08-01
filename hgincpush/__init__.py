#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Just a simple script that adds/commits/pushes all changes by parts.
# Used to push very large changesets in an incremental manner
#
# The MIT License (MIT)
# 
# Copyright (c) 2014 Moritz Wundke
# 
# Permission is hereby granted, free of charge, to any person obtaining 
# a copy of this software and associated documentation files (the "Software"), 
# to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the 
# Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
# IN THE SOFTWARE.
#
from mercurial import ui, hg
from mercurial.node import hex
from mercurial import commands
import os
import time
import subprocess
import argparse

__license__ = 'MIT'
__version__ = '1.0'
__author__ = 'Moritz Wundke'

start_time = []

def split(arr, count):
    return [arr[i::count] for i in range(count)]

def time_push():
    """
    Push a start time mark
    """
    global start_time
    start_time.append(time.time())

def time_pop():
    """
    Calculate ellapsed time from the last push start mark
    """
    global start_time
    start = start_time.pop()
    if start >= 0:
        return time.time() - start
    return 0

def hg_status(repo_path, is_dry_run):
    proc = subprocess.Popen(
        ["hg", "status"],
        stdout=subprocess.PIPE,
        cwd=repo_path
        )
    stdout = proc.communicate()[0]
    if proc.returncode != 0:
        raise RuntimeError("Status command failed to succeed! {error}".format(error=stdout))
    if is_dry_run:
        print(stdout)
    return stdout.split('\n')

def hg_push(repo_path, is_dry_run):
    print(" - Pushing to default branch")
    if not is_dry_run:
        proc = subprocess.Popen(
            ["hg", "push", "--chunked"],
            stdout=subprocess.PIPE,
            cwd=repo_path
            )
        stdout = proc.communicate()[0]
        if proc.returncode != 0:
            print(stdout)
            raise RuntimeError("Push command failed to succeed! {error}".format(error=stdout))

def hg_commit(repo_path, is_dry_run, msg):
    print(" - Commiting")
    if not is_dry_run:
        proc = subprocess.Popen(
            ["hg", "commit", "-m", msg],
            stdout=subprocess.PIPE,
            cwd=repo_path
            )
        stdout = proc.communicate()[0]
        if proc.returncode != 0:
            raise RuntimeError("Commit command failed to succeed! {error}".format(error=stdout))

def hg_add(repo_path, is_dry_run, files):
    # Split the process in smaller pieces
    print(" - Adding {num}".format(num=len(files)))
    bunches = split(files,10)
    for bunch in bunches:
        if not is_dry_run:
            proc = subprocess.Popen(
                ["hg", "add",] + bunch,
                stdout=subprocess.PIPE,
                cwd=repo_path
                )
            stdout = proc.communicate()[0]
            if proc.returncode != 0:
                print(stdout)
                raise RuntimeError("Add command failed to succeed! {error}".format(error=stdout))
        else:
            print("  > {files}".format(files=bunch))

def get_buckets(files, max_files=200, max_bucket_size=200):
    buckets = {}
    bucket_num = 1
    file_counter = 0
    file_size_counter = 0
    for file_status in files:
        status = file_status.split()
        if len(status) == 2:
            if not bucket_num in buckets:
                buckets[bucket_num] = []

            file_size = os.path.getsize(status[1]) / float(1024 * 1024)
            buckets[bucket_num].append(status[1])

            if len(buckets[bucket_num]) >= max_files or file_size_counter >= max_bucket_size:
                bucket_num += 1
                file_size_counter = 0

            file_size_counter += file_size
    return buckets

def push_buckets(repo_path, is_dry_run, buckets, template_msg):
    buckets_num = len(buckets)
    for bucket in buckets:
        msg = template_msg.format(bucket=bucket, total=buckets_num, files=len(buckets[bucket]))
        print("> {msg}".format(msg=msg))
        time_push()
        commit_bucket(repo_path, is_dry_run, buckets[bucket], msg)
        print(" - Completed in {secs}s".format(secs=time_pop()))
            
    # Now push all changes
    hg_push(repo_path, is_dry_run)

def commit_bucket(repo_path, is_dry_run, files, msg):
    hg_add(repo_path, is_dry_run, files)
    hg_commit(repo_path, is_dry_run, msg)

def do_push_buckets(repo_path, is_dry_run, max_files, max_bucket_size, template_msg):
    buckets = get_buckets(hg_status(repo_path, is_dry_run), max_files=max_files, max_bucket_size=max_bucket_size)
    push_buckets(repo_path, is_dry_run, buckets, template_msg)

def main():
    parser = argparse.ArgumentParser(description='Mercurial incremental push helper (%s). By %s' % (__version__, __author__))

    parser.add_argument('-v', '--version', action='version', version=__version__)
    parser.add_argument('-s', help='Maximum size in  MB a bucket can hold', default=200, type=int)
    parser.add_argument('-f', help='Number of max file a bucket can hold', default=2000000, type=int)
    parser.add_argument('-p', '--path', help='Path to the mercurial clone', required=True)
    parser.add_argument('-m', '--msg', help='Custom msg to be used when performing the comments. Use {bucket}, {total} and {files} for extra information.', default='Commiting bucket {bucket}/{total} with {files} files.')
    parser.add_argument('-d', '--dry', help='Perform a dryrun printing into the log the content of the possible buckets', action="store_true", default=False)
    args = parser.parse_args()

    time_push()
    do_push_buckets(args.path, args.dry, args.f, args.s, args.msg)
    print("Total time: {secs}s".format(secs=time_pop()))

if __name__ == "__main__":
    main()
