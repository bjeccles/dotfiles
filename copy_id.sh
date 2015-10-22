#!/bin/bash

if (ssh $1 '[ -d $HOME/.ssh/users/bje ]'); then
	ssh $1 'rm -r $HOME/.ssh/users/bje';
fi

ssh $1 'mkdir -p $HOME/.ssh/users/bje'
scp .bashrc $1:~/.ssh/users/bje/.bashrc
scp .gitconfig $1:~/.ssh/users/bje/.gitconfig

ssh-copy-id -i identity $1
