#!/bin/bash

VERSION=$(date -I)
PACKAGE="backup-active-collab_$VERSION"

gtar cvzf "../$PACKAGE.tar.gz" --transform "s+^+$PACKAGE/+"  \
	--exclude ".DS_Store" \
	--exclude "._*" \
	--exclude ".git/" \
	--exclude ".idea" \
	--exclude ".venv" \
	--exclude "*.pyc" \
	--exclude "__pycache__" \
	--exclude "data*" \
	--exclude "*.ini" \
	-- *

