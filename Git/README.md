# Git & GitHub Quick Reference

A practical Git cheat sheet for initializing repositories, configuring Git, pushing code to GitHub, handling branches, stashing changes, checking differences, and recovering from common mistakes.

---

## Table of Contents

- [Initial Setup](#initial-setup)
- [Create or Connect a Repository](#create-or-connect-a-repository)
- [Authentication with GitHub Token](#authentication-with-github-token)
- [Basic Daily Workflow](#basic-daily-workflow)
- [Branching](#branching)
- [Syncing with Remote](#syncing-with-remote)
- [Stash Commands](#stash-commands)
- [Logs and History](#logs-and-history)
- [Difference Checking](#difference-checking)
- [Checkout and Restore](#checkout-and-restore)
- [Reset and Revert](#reset-and-revert)
- [Tagging](#tagging)
- [Useful Inspection Commands](#useful-inspection-commands)
- [Open GitHub Project in VS Code Online](#open-github-project-in-vs-code-online)
- [Detached HEAD Fix](#detached-head-fix)
- [Notes](#notes)

---

## Initial Setup

### Show current Git configuration
```bash
git config --list --show-origin
```
Shows all configured Git values such as username, email, editor, and the file where each setting is stored.

### Edit global Git configuration
```bash
git config --global --edit
```
Opens the global Git config file for editing.

Example Windows location:
```text
C:\Users\shuva\.gitconfig
```

### Set your Git username
```bash
git config --global user.name "Shuvabrata Dey"
```
Sets the author name used in commits.

### Set your Git email
```bash
git config --global user.email "shuvabratadey@gmail.com"
```
Sets the author email used in commits.

### Add all folders as safe directories
```bash
git config --global --add safe.directory '*'
```
Allows Git to trust all repositories on your machine.

> **Warning:** This is convenient, but less secure. Use it only if you understand the risks.

### Cache credentials temporarily
```bash
git config --global credential.helper cache
```
Temporarily stores credentials so you do not need to enter them repeatedly.

### Recommended on Windows
```bash
git config --global credential.helper manager-core
```
Uses Git Credential Manager for secure credential storage on Windows.

---

## Create or Connect a Repository

### Initialize a new Git repository
```bash
git init
```
Creates a new local Git repository in the current folder.

### Add a remote GitHub repository
```bash
git remote add origin <repository-link>
```
Connects your local repository to a remote GitHub repository.

Example:
```bash
git remote add origin https://github.com/username/project.git
```

### Check remote repositories
```bash
git remote -v
```
Shows the remote URLs linked to your local repository.

### Clone an existing repository
```bash
git clone https://github.com/shuvabratadey/FPGA-CPU-Design.git
```
Downloads a GitHub repository to your local machine.

---

## Authentication with GitHub Token

GitHub no longer accepts account passwords for Git operations over HTTPS.  
Use a **Personal Access Token (PAT)** instead.

Generate a token from:
```text
https://github.com/settings/tokens
```

After generating the token:

```bash
git push origin master
```

When prompted:
- **Username** → your GitHub username
- **Password** → your GitHub Personal Access Token

> Use the token in place of your password.

---

## Basic Daily Workflow

### Check repository status
```bash
git status
```
Shows modified files, staged files, and untracked files.

### Add all files
```bash
git add .
```
Stages all changes in the current directory.

### Add a specific file
```bash
git add <file_name>
```
Stages only the selected file.

### Commit staged changes
```bash
git commit -m "Your commit message"
```
Saves the staged changes with a message.

### Push code to remote branch
```bash
git push origin master
```
Uploads commits to the `master` branch on GitHub.

> Some repositories use `main` instead of `master`.

### Push and set upstream branch
```bash
git push --set-upstream origin master
```
Pushes the branch and links it with the remote branch so future `git push` works without extra arguments.

---

## Branching

### Create a new branch
```bash
git branch <branch_name>
```
Creates a new branch.

### Switch to a branch
```bash
git checkout <branch_name>
```
Moves to the selected branch.

### Create and switch in one command
```bash
git checkout -b <branch_name>
```
Creates a new branch and switches to it immediately.

### Modern alternative
```bash
git switch <branch_name>
```
Switches branches using the newer Git command.

### Create and switch using modern command
```bash
git switch -c <branch_name>
```
Creates a branch and switches to it.

### Push a branch to GitHub
```bash
git push origin <branch_name>
```
Uploads the local branch to GitHub.

### Delete a local branch
```bash
git branch -d <branch_name>
```
Deletes a branch if it has already been merged.

### Force delete a local branch
```bash
git branch -D <branch_name>
```
Deletes a branch even if it has not been merged.

### Delete a remote branch
```bash
git push origin --delete <branch_name>
```
Removes the branch from GitHub.

### List all local branches
```bash
git branch
```
Displays all local branches.

### List all local and remote branches
```bash
git branch -a
```
Shows both local and remote branches.

---

## Syncing with Remote

### Pull changes from remote
```bash
git pull origin master
```
Downloads and merges changes from the remote `master` branch.

### Set upstream while pulling
```bash
git pull --set-upstream origin master
```
Associates your current branch with the remote branch while pulling.

### Fetch remote updates without merging
```bash
git fetch
```
Downloads remote changes but does not merge them into your current branch.

### Fetch all remotes
```bash
git fetch --all
```
Downloads updates from all remotes.

### Merge fetched changes
```bash
git merge origin/master
```
Merges fetched changes into your current branch.

### Rebase current branch on remote
```bash
git pull --rebase origin master
```
Pulls changes and reapplies your local commits on top of the updated remote history.

---

## Stash Commands

### Save current uncommitted changes
```bash
git stash
```
Temporarily stores your working changes.

### Restore the latest stash
```bash
git stash pop
```
Reapplies the most recent stash and removes it from stash history.

### Restore stash without deleting it
```bash
git stash apply
```
Reapplies stashed changes but keeps the stash entry.

### View all stashes
```bash
git stash list
```
Shows all saved stashes.

### Delete a specific stash
```bash
git stash drop stash@{0}
```
Deletes one stash entry.

### Delete all stashes
```bash
git stash clear
```
Removes all saved stashes.

---

## Logs and History

### Show commit history
```bash
git log
```
Displays commit history.

### Show compact one-line history
```bash
git log --oneline
```
Shows each commit in one line.

### Show graphical branch history
```bash
git log --all --decorate --graph --oneline
```
Displays a visual commit graph with branch and tag labels.

### Show details of last commit
```bash
git log -1
```
Displays the latest commit details.

### Show who changed each line
```bash
git blame <file_name>
```
Shows line-by-line commit authorship for a file.

---

## Difference Checking

### Show unstaged changes
```bash
git diff
```
Displays changes that are not yet staged.

### Show difference for a specific file
```bash
git diff <file_path/file_name>
```
Displays changes for a particular file.

### Show staged changes
```bash
git diff --staged
```
Displays changes that are staged but not yet committed.

### Compare two commits
```bash
git diff <commit1> <commit2>
```
Shows differences between two commits.

### Compare current branch with another branch
```bash
git diff master..feature-branch
```
Shows differences between branches.

---

## Checkout and Restore

### Checkout a specific commit
```bash
git checkout <commit_id>
```
Moves your working tree to a specific commit.

### Return to previous branch
```bash
git checkout -
```
Switches back to the last checked-out branch.

### Restore a file to last committed version
```bash
git restore <file_name>
```
Discards working directory changes for a file.

### Unstage a file
```bash
git restore --staged <file_name>
```
Removes a file from the staging area without deleting its changes.

---

## Reset and Revert

### Soft reset last commit
```bash
git reset
```
Reverse of "git add ."

### Soft reset last commit
```bash
git reset --soft HEAD~1
```
Removes the last commit but keeps changes staged.

### Mixed reset last commit
```bash
git reset HEAD~1
```
Removes the last commit and unstages the changes.

### Hard reset last commit
```bash
git reset --hard HEAD~1
```
Removes the last commit and deletes all associated changes.

> **Warning:** This permanently deletes uncommitted work.

### Reset branch to a specific commit
```bash
git reset --hard <commit_id>
```
Moves the branch pointer and working tree to a specific commit.

### Revert a commit safely
```bash
git revert <commit_id>
```
Creates a new commit that undoes an earlier commit without rewriting history.

---

## Tagging

### Create a tag
```bash
git tag v1.0
```
Creates a lightweight tag.

### Create an annotated tag
```bash
git tag -a v1.0 -m "Version 1.0 release"
```
Creates a tag with extra information.

### Push tags to GitHub
```bash
git push origin --tags
```
Uploads all tags to the remote repository.

### List tags
```bash
git tag
```
Displays all available tags.

---

## Useful Inspection Commands

### See current branch
```bash
git branch --show-current
```
Shows the active branch name.

### Show commit hash of current HEAD
```bash
git rev-parse HEAD
```
Displays the full commit ID of the current HEAD.

### Show tracked files
```bash
git ls-files
```
Lists files tracked by Git.

### Remove an untracked file
```bash
git clean -f
```
Deletes untracked files.

### Remove untracked files and folders
```bash
git clean -fd
```
Deletes untracked files and directories.

> **Warning:** This cannot be undone.

---

## Open GitHub Project in VS Code Online

You can open a GitHub repository directly in a browser-based VS Code interface.

### Example repository
```text
https://github.com/shuvabratadey/ESP-IDF-Free-RTOS
```

### Add `1s` after `github`
```text
https://github1s.com/shuvabratadey/ESP-IDF-Free-RTOS
```

This opens the repository in a VS Code-like online viewer.

---

## Detached HEAD Fix

If your HEAD is detached and you want to recover:

```bash
git log -1
```
Note the latest commit SHA.

```bash
git checkout master
```
Switch back to your main branch.

```bash
git reset --hard <commit-id>
```
Move your branch back to the detached commit.

> Use this carefully because `--hard` discards local changes.

Reference:
```text
https://stackoverflow.com/questions/999907/git-push-says-everything-up-to-date-even-though-i-have-local-changes
```

---

## Notes

- `master` and `main` are different branch names. Use whichever your repository uses.
- Prefer `user.name` and `user.email` over incorrect keys like:
  - `user.username`
  - `user.usernameemail`
  - `user.password`
- Never store your GitHub password in Git config.
- Use a **Personal Access Token** or Git Credential Manager instead.

---

## Recommended Beginner Workflow

```bash
git init
git remote add origin <repository-link>
git add .
git commit -m "Initial commit"
git branch -M main
git push --set-upstream origin main
```

This is a common workflow for creating and pushing a new project to GitHub.

---
