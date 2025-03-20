#!/bin/bash
# SPDX-FileCopyrightText: Copyright (c) 2025 Cisco and/or its affiliates.
# SPDX-License-Identifier: Apache-2.0

set -e

########################################
# Sphinx documentation builder script.
# It should be called with Taskfile.
########################################

## Input config (absolute paths only)
SOURCE_DIR="${SOURCE_DIR:-}"
SCHEMA_DIR="${SCHEMA_DIR:-}"
BUILD_DOCS_DIR="${BUILD_DOCS_DIR:-}"

## Cleanup previous builds
rm -rf $BUILD_DOCS_DIR

## Configure source
cd $SOURCE_DIR
SOURCE_REQ_FILE="requirements.txt"
SOURCE_PAGES_DIR="pages/"

## Install packages
pip3 install -r $SOURCE_REQ_FILE

## Generate diagrams
proto-gen-md-diagrams -d $SCHEMA_DIR
mv ./*.proto.md $SOURCE_PAGES_DIR

## Build using sphinx
sphinx-build -M clean "$SOURCE_DIR" "$BUILD_DOCS_DIR"
sphinx-build -M html "$SOURCE_DIR" "$BUILD_DOCS_DIR"
