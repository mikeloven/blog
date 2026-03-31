---
layout: post
title: Hello World!
date: 2026-03-31
categories:
  - ai
  - security
  - offensive-security
  - research-log
tags:
  - llm
  - bug-bounty
  - pentest
  - ai-security
  - prompt-injection
---

## Why I’m starting this blog

I’m a strong believer in AI’s promise. Like the internet, it can unlock incredible things—and, just as easily, terrible ones. It depends on how we use it.

My focus is security in two directions:

- **Offensive AI:** using AI to perform traditional security testing
- **AI Red Teaming:** performing security testing against AI systems

At a recent AI Security Practitioner conference, Nicholas Carlini (Anthropic) described using Claude Code to find zero-days in widely used software:  
[https://www.youtube.com/watch?v=1sd26pWhfmg](https://www.youtube.com/watch?v=1sd26pWhfmg)

That pushed me to start this blog.

My goal is to build in public while I figure this out in real time, and to keep a record I can come back to when I inevitably forget how I did something.

Full disclosure: I haven’t done much writing in a while, so yes—I’ll be using AI to help. I’m inspired by Daniel Miessler’s approach of using his personal AI assistant in his writing workflow. For now, I’ll mostly use AI for outlines and structure, then refine from there.

---

## What I’m actually going to do first

I have a tendency to get stuck in planning until things feel “perfect.”  
So I’m intentionally not over-planning this—I’m choosing to start, even if it’s messy.

My first goal is simple: set up a basic lab environment and run real experiments.  
To begin: a Kali VM with Claude Code and OpenCode installed. (I’m on Claude Pro, so I likely don’t have enough tokens to run Claude Code exclusively.)

I’m starting with an area I know better: CTFs.  
I’ll use agents on Hack The Box challenges and track what actually happens:

- Can an agent solve a challenge with no assistance?
- Where does it fail?
- What interventions improve outcomes?
- Which model/tool setups are most practical?

I also want a repeatable writing flow. I’ll use AI to help outline posts and organize findings, then publish what’s useful—including failures.

I’m not trying to look polished out of the gate.  
I’m trying to get reps in public and improve quickly.

If this is useful to others, great. If not, at minimum it’ll be a searchable memory for future me.

---

## Next post teaser

In the next post, I’ll share my initial setup and first Hack The Box runs, including:

- the exact environment and model/tool choices,
- where agents got stuck,
- where they surprised me,
- and what I changed to improve results.