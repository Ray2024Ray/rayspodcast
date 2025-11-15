---
title: Chinese Episodes
layout: default
permalink: /episodes_zh.html
body_class: episode-page
---

# Chinese Episodes

<div class="row">
{% assign eps = site.episodes | where: "lang", "zh" | sort: "date" | reverse %}
{% for ep in eps %}
<div class="col col-4 col-t-6 col-m-12">
  <article class="c-blog-card">
    <div class="c-blog-card__inner">
      <div class="c-blog-card__image-wrapper">
        <a class="c-blog-card__image" href="{{ ep.spotify | default: ep.external_url }}" target="_blank" rel="noopener">
          <img src="{{ ep.cover | default: '/images/podcast-cover.png' | relative_url }}" alt="{{ ep.title | escape }}">
        </a>
      </div>
      <div class="c-blog-card__text-content">
        <div class="c-blog-card__tags-box">
          {% for tag in ep.tags limit:2 %}<span class="c-blog-card__tag">{{ tag }}</span>{% endfor %}
        </div>
        <h3 class="c-blog-card__title">
          <a href="{{ ep.spotify | default: ep.external_url }}" target="_blank" rel="noopener">{{ ep.title }}</a>
        </h3>
        {% if ep.excerpt %}<p class="c-blog-card__excerpt">{{ ep.excerpt }}</p>{% endif %}
      </div>
    </div>
  </article>
</div>
{% endfor %}
</div>
