#!/bin/bash
# Blog publishing script - copies posts from Obsidian, syncs images and pushes to GitHub

cd /home/mloven/workspace/github.com/mikeloven/blog

echo "Copying blog posts from Obsidian to Hugo..."
cp -v /home/mloven/Documents/obsidian_vaults/vault/blog/*.md content/posts/

echo "Syncing images from Obsidian..."
python3 sync-images.py

echo "Adding all changes..."
git add .

echo "Committing changes..."
if git diff --staged --quiet; then
    echo "No changes to commit."
else
    commit_message="Update blog content - $(date '+%Y-%m-%d %H:%M')"
    git commit -m "$commit_message"
    
    echo "Pushing to GitHub..."
    git push origin main
    
    echo "Blog published! Check GitHub Actions for deployment status."
    echo "Your blog will be available at: https://blog.mikeloven.com"
fi