#!/usr/bin/env bash
set -e

# install Python dependencies
pip3 install -r requirements.txt

# install Ruby gems
bundle install

# build and serve site
bundle exec jekyll build
bundle exec jekyll serve -H 0.0.0.0 --incremental --watch
