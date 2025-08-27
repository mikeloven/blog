#!/usr/bin/env python3
"""
Sync images from Obsidian vault to Hugo static directory.
This script finds all images referenced in blog posts and copies them from
the Obsidian z-Attachments folder to Hugo's static/images folder.
"""

import os
import re
import shutil
from pathlib import Path

# Paths
OBSIDIAN_VAULT = Path("/home/mloven/Documents/obsidian_vaults/vault")
OBSIDIAN_ATTACHMENTS = OBSIDIAN_VAULT / "z-Attachments"
HUGO_CONTENT_POSTS = Path("/home/mloven/workspace/github.com/mikeloven/blog/content/posts")
HUGO_STATIC_IMAGES = Path("/home/mloven/workspace/github.com/mikeloven/blog/static/images")

# Create Hugo images directory if it doesn't exist
HUGO_STATIC_IMAGES.mkdir(parents=True, exist_ok=True)

def find_image_references(content):
    """Find all image references in markdown content."""
    # Match both ![alt](image.png) and ![[image.png]] formats
    patterns = [
        r'!\[.*?\]\(([^)]+\.(?:png|jpg|jpeg|gif|webp|svg))\)',  # Standard markdown
        r'!\[\[([^]]+\.(?:png|jpg|jpeg|gif|webp|svg))\]\]'      # Obsidian wiki links
    ]
    
    images = []
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        images.extend(matches)
    
    # Extract just the filename from paths like "z-Attachments/image.png"
    cleaned_images = []
    for image in images:
        filename = Path(image).name  # Extract just the filename
        cleaned_images.append(filename)
    
    return cleaned_images

def copy_image_if_exists(image_name):
    """Copy image from Obsidian attachments to Hugo static folder."""
    source = OBSIDIAN_ATTACHMENTS / image_name
    destination = HUGO_STATIC_IMAGES / image_name
    
    if source.exists():
        shutil.copy2(source, destination)
        print(f"Copied: {image_name}")
        return True
    else:
        print(f"Warning: Image not found in attachments: {image_name}")
        return False

def update_image_links_in_content(content):
    """Update image links to use Hugo's static path format."""
    # Convert ![[path/image.png]] to ![](/images/image.png) - extract just filename
    def replace_obsidian_link(match):
        full_path = match.group(1)
        filename = Path(full_path).name
        return f'![](/images/{filename})'
    
    content = re.sub(
        r'!\[\[([^]]+\.(?:png|jpg|jpeg|gif|webp|svg))\]\]',
        replace_obsidian_link,
        content,
        flags=re.IGNORECASE
    )
    
    # Update standard markdown links to use /images/ path - extract just filename
    def replace_markdown_link(match):
        alt_text = match.group(1)
        full_path = match.group(2)
        filename = Path(full_path).name
        return f'![{alt_text}](/images/{filename})'
    
    content = re.sub(
        r'!\[([^\]]*)\]\(([^)]+\.(?:png|jpg|jpeg|gif|webp|svg))\)',
        replace_markdown_link,
        content,
        flags=re.IGNORECASE
    )
    
    return content

def process_blog_posts():
    """Process all markdown files in the Hugo content posts directory."""
    if not HUGO_CONTENT_POSTS.exists():
        print(f"Hugo content posts directory not found: {HUGO_CONTENT_POSTS}")
        return
    
    processed_images = set()
    
    for md_file in HUGO_CONTENT_POSTS.glob("*.md"):
        print(f"Processing: {md_file.name}")
        
        # Read the file
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find images referenced in this file
        images = find_image_references(content)
        
        # Copy images to Hugo static folder
        for image in images:
            if image not in processed_images:
                copy_image_if_exists(image)
                processed_images.add(image)
        
        # Update image links in content
        updated_content = update_image_links_in_content(content)
        
        # Write back if content changed
        if updated_content != content:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"Updated image links in: {md_file.name}")
    
    print(f"\nProcessed {len(processed_images)} unique images")

if __name__ == "__main__":
    print("Syncing images from Obsidian to Hugo...")
    process_blog_posts()
    print("Done!")