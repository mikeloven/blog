# Mike Loven's Blog

A personal blog built with Jekyll using the Chirpy theme, with seamless Obsidian integration for content creation.

## Overview

This repository contains a Jekyll blog that's configured to:
1. Use the Chirpy theme for a beautiful, responsive design
2. Integrate with Obsidian for drafting posts in Markdown
3. Deploy to GitHub Pages with a single command

## Features

- **Jekyll with Chirpy Theme**: Clean, responsive design with dark/light mode
- **Obsidian Integration**: Draft posts in Obsidian and publish them seamlessly
- **One-Command Publishing**: Single script to handle the entire publishing workflow
- **GitHub Pages Hosting**: Free, reliable hosting with automatic builds

## Directory Structure

```
.
├── _config.yml          # Jekyll configuration
├── _posts/              # Published blog posts (generated from Obsidian)
├── assets/              # Images and other assets
├── blog_vault/          # Obsidian vault
│   ├── posts/           # Blog posts drafted in Obsidian
│   └── templates/       # Templates for new posts
└── publish.sh           # One-command publishing script
```

## Workflow

### Writing New Posts

1. Open Obsidian and navigate to the `blog_vault` folder
2. Create a new post in the `posts` folder using the Jekyll template
3. Write your content in Markdown
4. Save images in the `blog_vault/assets` folder and reference them in your posts

### Publishing

Run the publishing script to update your blog:

```bash
./publish.sh
```

This script will:
- Copy posts from Obsidian to Jekyll's `_posts` directory
- Copy images to the appropriate Jekyll assets folder
- Commit changes to Git
- Push to GitHub, triggering a GitHub Pages build

For local preview before publishing:

```bash
./publish.sh --preview
```

## Setup

This repository is already configured and ready to use. Just clone it and start writing!

## License

This blog is based on the Chirpy theme, which is published under [MIT License](https://github.com/cotes2020/chirpy-starter/blob/master/LICENSE).
