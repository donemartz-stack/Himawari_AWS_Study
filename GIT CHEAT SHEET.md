GIT CHEAT SHEET - Himawari + Python + Jupyter Workflow

==========================
1. Basic Commands
==========================
git init                # Initialize a new local Git repository
git clone <repo_url>    # Clone a remote GitHub repo
git status              # Show status of files
git add <file>          # Stage a file for commit
git add .               # Stage all changes
git commit -m "msg"     # Commit staged changes with message
git log                 # View commit history

==========================
2. Branching & Merginggit 
==========================
git branch              # List local branches
git branch <name>       # Create a new branch
git checkout <name>     # Switch to branch
git checkout -b <name>  # Create and switch to new branch
git merge <branch>      # Merge branch into current
git branch -d <branch>  # Delete a local branch

==========================
3. Remote (GitHub) Commands
==========================
git remote -v           # List remote repositories
git remote add origin <repo_url>  # Link local repo to GitHub
git push                # Push commits to GitHub
git push -u origin <branch>       # Push branch first time
git pull                # Fetch and merge remote changes
git branch -r           # List remote branches
git branch -a           # List all branches

==========================
4. Undo / Fix Mistakes
==========================
git reset <file>        # Unstage a file
git checkout -- <file>  # Discard local changes
git diff                # Show differences in files
git log                 # View commit history

==========================
5. Tips for Jupyter + Git
==========================
- Clear notebook outputs before committing
- Keep raw data in data/ folder (.gitignore prevents push)
- Commit frequently with meaningful messages
- Use branches for experiments, main branch stays stable
- Only push scripts and notebooks to GitHub

==========================
6. Daily Workflow Example
==========================
1. Edit notebooks in notebooks/
2. Move stable code to src/
3. Clear outputs from notebooks
4. Stage & commit:
   git add .
   git commit -m "Descriptive message"
5. Push to GitHub:
   git push
6. Pull updates before working on another machine:
   git pull origin main