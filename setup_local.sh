#!/bin/bash

f=$(dirname $(readlink -f "$0"))
n=$(grep '^name *=' "$f/typst.toml" | cut -d'"' -f2)
d="$HOME/.local/share/typst/packages/local/$n"
v=$(grep version "$f/typst.toml" | cut -d'"' -f2)

echo "create $n directory in local package repository"
mkdir -p "$d"

echo "link version $v to local package repository"
ln -sf -T "$f" "$d/$v"

echo 'now you can use:'
echo '  use #import "@local/'"$n"':'"$v"'"'
