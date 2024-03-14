#!/bin/bash

# Define the branch you want to check
BRANCH="master"
BASE_DIR=~/dataViz
cd $BASE_DIR || exit
# Fetch the latest changes from the remote repository
git checkout $BRANCH
git fetch

# Check if the local branch is behind the remote branch
if [ "$(git rev-list HEAD..origin/${BRANCH} --count)" -gt 0 ] || [ "$1" = "force" ]; then
  echo "There are new commits on the ${BRANCH} branch."
  git stash
  git pull -X theirs || exit
  sh $BASE_DIR/tools/deploy/deploy_django.sh

  echo "Deployed"
else
  echo "The ${BRANCH} branch is up to date."
fi
