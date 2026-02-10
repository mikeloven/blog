---
layout: default
title: Home
---

## Posts

{% for post in site.posts %}
  <article>
    <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
    <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%B %d, %Y" }}</time>
  </article>
{% endfor %}
