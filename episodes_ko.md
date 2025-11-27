---
title: Korean Episodes
layout: default
permalink: /episodes_ko.html
body_class: episode-page
---

<div class="row">
{% assign eps = site.episodes | where: "language", "Korean" | sort: "published_date" | reverse %}
{% for ep in eps %}
<div class="col col-4 col-t-6 col-m-12">
  <article class="c-blog-card">
    <div class="c-blog-card__inner">
      <div class="c-blog-card__image-wrapper">
        <a class="c-blog-card__image" href="{{ ep.link }}" target="_blank" rel="noopener">
          <img src="{{ ep.cover | default: '/images/podcast-cover.png' }}" alt="{{ ep.title | escape }}">
        </a>
      </div>
      <div class="c-blog-card__text-content">
        <div class="c-blog-card__tags-box">
          {% for tag in ep.tags limit:2 %}<span class="c-blog-card__tag">{{ tag }}</span>{% endfor %}
        </div>
        <h3 class="c-blog-card__title">
          <a href="{{ ep.link }}" target="_blank" rel="noopener">{{ ep.title }}</a>
        </h3>
        <p class="c-blog-card__excerpt">{{ ep.description | strip_html | truncatewords: 20 }}</p>
      </div>
    </div>
  </article>
</div>
{% endfor %}
</div>
