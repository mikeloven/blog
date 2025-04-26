#!/bin/bash

# publish.sh - One-command publishing for Jekyll blog with Obsidian integration
# Created: 2025-04-25

set -e  # Exit on error

echo "🚀 Starting blog publishing process..."

# Directory paths
BLOG_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OBSIDIAN_POSTS="$BLOG_ROOT/blog_vault/posts"
OBSIDIAN_DRAFTS="$BLOG_ROOT/blog_vault/drafts"
JEKYLL_POSTS="$BLOG_ROOT/_posts"
OBSIDIAN_ASSETS="$BLOG_ROOT/blog_vault/assets"
JEKYLL_ASSETS="$BLOG_ROOT/assets/img"

# Create directories if they don't exist
mkdir -p "$JEKYLL_POSTS"
mkdir -p "$JEKYLL_ASSETS"
mkdir -p "$OBSIDIAN_ASSETS"

# Step 1: Copy posts from Obsidian to Jekyll
echo "📝 Copying posts from Obsidian to Jekyll..."

# Copy from posts directory
find "$OBSIDIAN_POSTS" -name "*.md" -type f | while read -r post; do
    filename=$(basename "$post")
    # Only copy if the file doesn't exist or is newer
    if [ ! -f "$JEKYLL_POSTS/$filename" ] || [ "$post" -nt "$JEKYLL_POSTS/$filename" ]; then
        echo "  - Copying $filename from posts"
        cp "$post" "$JEKYLL_POSTS/$filename"
    fi
done

# Copy from drafts directory
find "$OBSIDIAN_DRAFTS" -name "*.md" -type f | while read -r draft; do
    # Convert spaces to hyphens and lowercase for Jekyll compatibility
    original_filename=$(basename "$draft")
    # Remove .md extension, convert spaces to hyphens, convert to lowercase
    processed_name=$(echo "${original_filename%.md}" | tr ' ' '-' | tr '[:upper:]' '[:lower:]')
    # Add current date if not already present and add .md extension back
    if [[ ! $processed_name =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}- ]]; then
        jekyll_filename="$(date +"%Y-%m-%d")-$processed_name.md"
    else
        jekyll_filename="$processed_name.md"
    fi
    
    # Only copy if the file doesn't exist or is newer
    if [ ! -f "$JEKYLL_POSTS/$jekyll_filename" ] || [ "$draft" -nt "$JEKYLL_POSTS/$jekyll_filename" ]; then
        echo "  - Copying $original_filename from drafts as $jekyll_filename"
        cp "$draft" "$JEKYLL_POSTS/$jekyll_filename"
    fi
done

# Step 2: Copy images from Obsidian to Jekyll
echo "💼️ Copying images from Obsidian to Jekyll..."
if [ -d "$OBSIDIAN_ASSETS" ]; then
    find "$OBSIDIAN_ASSETS" -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" -o -name "*.gif" \) | while read -r img; do
        rel_path=$(realpath --relative-to="$OBSIDIAN_ASSETS" "$img")
        # Create a web-safe filename (replace spaces with hyphens)
        safe_filename=$(basename "$rel_path" | tr ' ' '-')
        target_dir="$JEKYLL_ASSETS"
        target="$target_dir/$safe_filename"
        
        mkdir -p "$target_dir"
        
        # Only copy if the file doesn't exist or is newer
        if [ ! -f "$target" ] || [ "$img" -nt "$target" ]; then
            echo "  - Copying image $rel_path as $safe_filename"
            cp "$img" "$target"
        fi
    done
fi

# Step 3: Process Obsidian image links (manual conversion recommended for now)
echo "ℹ️ Note: For Obsidian image links, please convert them manually in your posts"
echo "   From: ![[image.png]] "
echo "   To:   ![Alt text](/assets/img/image-name.png)"

# The automatic conversion was causing issues, so we've disabled it for now
# You can manually format your image links in Obsidian using standard Markdown format

# Step 4: Build the site locally (optional, for preview)
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
