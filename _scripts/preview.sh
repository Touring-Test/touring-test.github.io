#!/usr/bin/env bash

bundle exec jekyll build --verbose
bundle exec jekyll serve -H 0.0.0.0 --incremental --watch
