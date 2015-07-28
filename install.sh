#!/usr/bin/env bash

ROOT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

ln -s -b $ROOT_DIR/.bashrc ~/.bashrc
ln -s -b $ROOT_DIR/.gitconfig ~/.gitconfig
ln -s -b $ROOT_DIR/.dircolors ~/.dircolors
ln -s -b $ROOT_DIR/.ssh_config ~/.ssh/config

