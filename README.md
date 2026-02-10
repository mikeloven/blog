# Mike's Blog

Personal blog built with Jekyll and GitHub Pages.

## Writing Posts

1. Create a new file in `_posts/` named `YYYY-MM-DD-title.md`
2. Add front matter:
   ```yaml
   ---
   layout: post
   title: "Your Title"
   date: YYYY-MM-DD
   ---
   ```
3. Write in Markdown
4. Commit and push — GitHub Actions handles the rest

## Images

- Put images in `Attachments/` folder
- Reference them in posts as `![[image.png]]` (Obsidian style) or `![alt](Attachments/image.png)`
- The build script automatically converts and copies them

## Local Development

```bash
bundle install
bundle exec jekyll serve
```

Then visit http://localhost:4000/blog/
