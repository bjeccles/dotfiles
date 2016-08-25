#!/usr/bin/env bash

ROOT_DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

scp $ROOT_DIR/.bashrc_ballbot $1:.bashrc
scp $ROOT_DIR/.gitconfig $1:.gitconfig
scp $ROOT_DIR/.dircolors $1:.dircolors
scp $ROOT_DIR/.ssh_config $1:.ssh/config

