#!/bin/bash

# publish.sh - One-command publishing for Jekyll blog with Obsidian integration
# Created: 2025-04-25

set -e  # Exit on error

echo "🚀 Starting blog publishing process..."

# Directory paths
BLOG_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OBSIDIAN_POSTS="$BLOG_ROOT/blog_vault/posts"
JEKYLL_POSTS="$BLOG_ROOT/_posts"
OBSIDIAN_ASSETS="$BLOG_ROOT/blog_vault/assets"
JEKYLL_ASSETS="$BLOG_ROOT/assets/img"

# Create directories if they don't exist
mkdir -p "$JEKYLL_POSTS"
mkdir -p "$JEKYLL_ASSETS"
mkdir -p "$OBSIDIAN_ASSETS"

# Step 1: Copy posts from Obsidian to Jekyll
echo "📝 Copying posts from Obsidian to Jekyll..."
find "$OBSIDIAN_POSTS" -name "*.md" -type f | while read -r post; do
    filename=$(basename "$post")
    # Only copy if the file doesn't exist or is newer
    if [ ! -f "$JEKYLL_POSTS/$filename" ] || [ "$post" -nt "$JEKYLL_POSTS/$filename" ]; then
        echo "  - Copying $filename"
        cp "$post" "$JEKYLL_POSTS/$filename"
    fi
done

# Step 2: Copy images from Obsidian to Jekyll
echo "🖼️ Copying images from Obsidian to Jekyll..."
if [ -d "$OBSIDIAN_ASSETS" ]; then
    find "$OBSIDIAN_ASSETS" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" -o -name "*.gif" \) | while read -r img; do
        rel_path=$(realpath --relative-to="$OBSIDIAN_ASSETS" "$img")
        target="$JEKYLL_ASSETS/$rel_path"
        target_dir=$(dirname "$target")
        
        mkdir -p "$target_dir"
        
        # Only copy if the file doesn't exist or is newer
        if [ ! -f "$target" ] || [ "$img" -nt "$target" ]; then
            echo "  - Copying image $rel_path"
            cp "$img" "$target"
        fi
    done
fi

# Step 3: Build the site locally (optional, for preview)
if [ "$1" == "--preview" ]; then
    echo "🔍 Building site for preview..."
    cd "$BLOG_ROOT"
    bundle exec jekyll serve
    exit 0
fi

# Step 4: Commit changes to Git
echo "💾 Committing changes to Git..."
cd "$BLOG_ROOT"
git add .
git commit -m "Blog update: $(date +"%Y-%m-%d %H:%M:%S")" || echo "No changes to commit"

# Step 5: Push to GitHub
echo "☁️ Pushing to GitHub..."
git push origin main || git push origin master

echo "✅ Blog publishing complete! Your changes will be live shortly at https://mikeloven.github.io/blog/"
