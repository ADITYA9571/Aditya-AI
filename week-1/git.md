# Git Commands Reference

## Initialize a New Repository
git init

## Check Repository Status
git status

## View Current Branch
git branch

## View Branch Tracking Information
git branch -vv

## Rename Current Branch to Main
git branch -M main

## Add Remote Repository
git remote add origin <repository-url>

## View Remote Repositories
git remote -v

## Pull Existing Repository Content
git pull origin main

## Check All Local and Remote Branches
git branch -a

## Add Files
git add .

## Commit Changes
git commit -m "Commit message"

## Push Current Branch
git push

## Push and Set Upstream Branch
git push -u origin main
git push --set-upstream origin main

## Merge a Branch
git checkout main
git merge feature-branch

## Remove File/Folder from Git Tracking
git rm -r --cached folder_name

## View Commit History
git log --oneline

## View Last 5 Commits
git log --oneline -5

## View Reference History
git reflog

## List Remote Branches on GitHub
git ls-remote --heads origin

## Clone Repository
git clone <repository-url>

## View Repository Files
ls

## Move to Parent Directory
cd ..

## Move into a Specific Folder
cd folder-name

## Basic Daily Workflow
git add .
git commit -m "Meaningful commit message"
git push