#!/usr/bin/env python3
"""
Process Obsidian markdown files for Jekyll.
- Converts ![[image.png]] to ![](/assets/images/image.png)
- Converts [[wikilinks]] to regular text
- Copies referenced images from Attachments/ to assets/images/
"""

import os
import re
import shutil
from pathlib import Path

# Configuration
POSTS_DIR = Path("_posts")
ATTACHMENTS_DIR = Path("Attachments")  # Change this to match your Obsidian setup
ASSETS_DIR = Path("assets/images")

# Patterns
OBSIDIAN_IMAGE = re.compile(r'!\[\[([^\]]+)\]\]')
OBSIDIAN_IMAGE_WITH_ALT = re.compile(r'!\[\[([^\]|]+)\|([^\]]+)\]\]')
OBSIDIAN_WIKILINK = re.compile(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]')
STANDARD_IMAGE = re.compile(r'!\[([^\]]*)\]\((?:\.\.\/)?(?:Attachments|attachments)\/([^)]+)\)')


def process_post(filepath: Path) -> set:
    """Process a single post file. Returns set of referenced images."""
    images = set()
    content = filepath.read_text(encoding='utf-8')
    original = content

    # Convert ![[image.png|alt]] to ![alt](/assets/images/image.png)
    def replace_image_with_alt(m):
        img = m.group(1)
        alt = m.group(2)
        images.add(img)
        return f'![{alt}](/assets/images/{img})'
    content = OBSIDIAN_IMAGE_WITH_ALT.sub(replace_image_with_alt, content)

    # Convert ![[image.png]] to ![](/assets/images/image.png)
    def replace_image(m):
        img = m.group(1)
        images.add(img)
        return f'![](/assets/images/{img})'
    content = OBSIDIAN_IMAGE.sub(replace_image, content)

    # Convert ![](Attachments/image.png) to ![](/assets/images/image.png)
    def replace_standard_image(m):
        alt = m.group(1)
        img = m.group(2)
        images.add(img)
        return f'![{alt}](/assets/images/{img})'
    content = STANDARD_IMAGE.sub(replace_standard_image, content)

    # Convert [[wikilinks]] to plain text (or you could make them links)
    def replace_wikilink(m):
        target = m.group(1)
        display = m.group(2) if m.group(2) else target
        return display
    content = OBSIDIAN_WIKILINK.sub(replace_wikilink, content)

    # Write back if changed
    if content != original:
        filepath.write_text(content, encoding='utf-8')
        print(f"Processed: {filepath}")

    return images


def main():
    # Create assets directory
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    # Process all posts
    all_images = set()
    if POSTS_DIR.exists():
        for post in POSTS_DIR.glob("*.md"):
            images = process_post(post)
            all_images.update(images)

    # Copy referenced images
    if ATTACHMENTS_DIR.exists():
        for img in all_images:
            src = ATTACHMENTS_DIR / img
            dst = ASSETS_DIR / img
            if src.exists():
                shutil.copy2(src, dst)
                print(f"Copied: {img}")
            else:
                print(f"Warning: Image not found: {img}")
    elif all_images:
        print(f"Warning: Attachments directory not found: {ATTACHMENTS_DIR}")

    print(f"\nProcessed {len(all_images)} images")


if __name__ == "__main__":
    main()
