#!/usr/bin/env python3
"""
Process Obsidian markdown files for Jekyll.

Default mode is build-safe and only processes files:
- Converts ![[image.png]] to ![](/assets/images/image.png)
- Converts [[wikilinks]] to regular text
- Copies referenced images from Attachments/ to assets/images/

Publish mode also commits and pushes publishable blog changes:
    python3 scripts/process_posts.py --publish
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Resolve paths relative to the repository root, not the caller's cwd.
REPO_ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = REPO_ROOT / "_posts"
ATTACHMENTS_DIR = REPO_ROOT / "Attachments"
ASSETS_DIR = REPO_ROOT / "assets/images"

# Only these paths are staged by --publish. Local scratch folders such as notes/
# and drafts/ remain ignored/unpublished unless manually moved into _posts/.
PUBLISH_PATHS = ["_posts", "Attachments", "assets/images"]

# Patterns
OBSIDIAN_IMAGE = re.compile(r'!\[\[([^\]]+)\]\]')
OBSIDIAN_IMAGE_WITH_ALT = re.compile(r'!\[\[([^\]|]+)\|([^\]]+)\]\]')
OBSIDIAN_WIKILINK = re.compile(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]')
STANDARD_IMAGE = re.compile(r'!\[([^\]]*)\]\((?:\.\.\/)?(?:Attachments|attachments)\/([^)]+)\)')
FRONTMATTER_TITLE = re.compile(r'^title:\s*["\']?(.+?)["\']?\s*$', re.MULTILINE)


def run(command: list[str], *, check: bool = True) -> subprocess.CompletedProcess:
    """Run a command from the repository root."""
    print(f"$ {' '.join(command)}")
    return subprocess.run(command, cwd=REPO_ROOT, text=True, check=check)


def capture(command: list[str]) -> str:
    """Run a command and return stdout from the repository root."""
    return subprocess.check_output(command, cwd=REPO_ROOT, text=True).strip()


def process_post(filepath: Path) -> set[str]:
    """Process a single post file. Returns set of referenced images."""
    images = set()
    content = filepath.read_text(encoding="utf-8")
    original = content

    # Convert ![[image.png|alt]] to ![alt](/assets/images/image.png)
    def replace_image_with_alt(m):
        img = m.group(1)
        alt = m.group(2)
        images.add(img)
        return f"![{alt}](/assets/images/{img})"

    content = OBSIDIAN_IMAGE_WITH_ALT.sub(replace_image_with_alt, content)

    # Convert ![[image.png]] to ![](/assets/images/image.png)
    def replace_image(m):
        img = m.group(1)
        images.add(img)
        return f"![](/assets/images/{img})"

    content = OBSIDIAN_IMAGE.sub(replace_image, content)

    # Convert ![](Attachments/image.png) to ![](/assets/images/image.png)
    def replace_standard_image(m):
        alt = m.group(1)
        img = m.group(2)
        images.add(img)
        return f"![{alt}](/assets/images/{img})"

    content = STANDARD_IMAGE.sub(replace_standard_image, content)

    # Convert [[wikilinks]] to plain text.
    def replace_wikilink(m):
        target = m.group(1)
        display = m.group(2) if m.group(2) else target
        return display

    content = OBSIDIAN_WIKILINK.sub(replace_wikilink, content)

    # Write back if changed.
    if content != original:
        filepath.write_text(content, encoding="utf-8")
        print(f"Processed: {filepath.relative_to(REPO_ROOT)}")

    return images


def process_posts() -> int:
    """Process all Jekyll posts and copy referenced images. Returns image count."""
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    all_images = set()
    if POSTS_DIR.exists():
        for post in sorted(POSTS_DIR.glob("*.md")):
            images = process_post(post)
            all_images.update(images)

    if ATTACHMENTS_DIR.exists():
        for img in sorted(all_images):
            src = ATTACHMENTS_DIR / img
            dst = ASSETS_DIR / img
            if src.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                print(f"Copied: {img}")
            else:
                print(f"Warning: Image not found: {img}")
    elif all_images:
        print(f"Warning: Attachments directory not found: {ATTACHMENTS_DIR.relative_to(REPO_ROOT)}")

    print(f"\nProcessed {len(all_images)} images")
    return len(all_images)


def publishable_status() -> str:
    """Return git status for paths managed by publish mode."""
    return capture(["git", "status", "--short", "--", *PUBLISH_PATHS])


def infer_commit_message(status_text: str | None = None) -> str:
    """Infer a useful commit message from newly added posts when possible."""
    status_text = status_text if status_text is not None else publishable_status()
    new_posts = []
    for line in status_text.splitlines():
        # Handles both untracked (?? path) and staged new files (A  path).
        status_code = line[:2]
        path_text = line[3:]
        if path_text.startswith("_posts/") and path_text.endswith(".md") and (
            status_code == "??" or "A" in status_code
        ):
            new_posts.append(REPO_ROOT / path_text)

    if len(new_posts) == 1:
        content = new_posts[0].read_text(encoding="utf-8")
        match = FRONTMATTER_TITLE.search(content)
        if match:
            return f"Add post: {match.group(1)}"
        return f"Add post: {new_posts[0].stem}"

    return "Publish blog updates"


def publish(message: str | None, *, dry_run: bool = False, push: bool = True) -> None:
    """Stage publishable paths, commit them if needed, and optionally push."""
    print("\nChecking git status before publishing...")
    run(["git", "status", "--short", "--branch"])

    pre_stage_status = publishable_status()
    if dry_run:
        if not pre_stage_status:
            print("No publishable changes to commit.")
            return
        commit_message = message or infer_commit_message(pre_stage_status)
        print(f"DRY RUN: would run: git add {' '.join(PUBLISH_PATHS)}")
        print("DRY RUN: publishable changes would be:")
        print(pre_stage_status)
        print(f"DRY RUN: would commit with message: {commit_message}")
        if push:
            print("DRY RUN: would run: git push")
        return

    commit_message = message or infer_commit_message(pre_stage_status)
    run(["git", "add", *PUBLISH_PATHS])

    staged = capture(["git", "diff", "--cached", "--name-only"])
    if not staged:
        print("No publishable staged changes to commit.")
        return

    run(["git", "commit", "-m", commit_message])

    if push:
        run(["git", "push"])
    else:
        print("Skipping push because --no-push was set.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Process Obsidian/Jekyll blog posts.")
    parser.add_argument(
        "--publish",
        action="store_true",
        help="After processing, git add publishable paths, commit, and push.",
    )
    parser.add_argument(
        "-m",
        "--message",
        help="Commit message to use with --publish. Defaults to an inferred message.",
    )
    parser.add_argument(
        "--no-push",
        action="store_true",
        help="With --publish, commit locally but do not push.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what --publish would do without staging, committing, or pushing.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    process_posts()

    if args.publish:
        publish(args.message, dry_run=args.dry_run, push=not args.no_push)

    return 0


if __name__ == "__main__":
    sys.exit(main())
