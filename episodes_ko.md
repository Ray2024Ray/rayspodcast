---
title: Korean Episodes
layout: default
permalink: /episodes_ko.html
body_class: episode-page
---

<div class="row">

{% comment %}
  *** MODIFICATION ***
  1. 我们从 `site.data.episodes` (YAML file) 读取
  2. 我们使用 'where' 过滤器来只获取 'language' == 'Korean' 的单集
  3. Python 脚本已经按日期排好序了
{% endcomment %}
{% assign eps = site.data.episodes | where: 'language', 'Korean' %}

{% if eps and eps.size > 0 %}
  {% for ep in eps %}
  <div class="col col-4 col-t-6 col-m-12">
    <article class="c-blog-card">
      <div class="c-blog-card__inner">
        <div class="c-blog-card__image-wrapper">
          {% comment %}
            *** MODIFICATION ***
            链接: 使用 'ep.link' (来自 YAML)
          {% endcomment %}
          <a class="c-blog-card__image" href="{{ ep.link }}" target="_blank" rel="noopener">
            <img src="{{ ep.cover | relative_url }}" alt="{{ ep.title | escape }}">
          </a>
        </div>
        <div class="c-blog-card__text-content">
          <div class="c-blog-card__tags-box">
            {% comment %}
              *** MODIFICATION ***
              我们只显示 'ep.language' 标签
            {% endcomment %}
            <span class="c-blog-card__tag">{{ ep.language }}</span>
          </div>
          <h3 class="c-blog-card__title">
            <a href="{{ ep.link }}" target="_blank" rel="noopener">{{ ep.title }}</a>
          </h3>
          {% comment %}
            *** MODIFICATION ***
            我们用 'ep.description' (来自 YAML) 替换了 'ep.excerpt'
            并截断它
          {% endcomment %}
          {% if ep.description %}
            <p class="c-blog-card__excerpt">{{ ep.description | markdownify | strip_html | truncatewords: 20 }}</p>
          {% endif %}
        </div>
      </div>
    </article>
  </div>
  {% endfor %}
{% else %}
  <div class="col col-12">
    <p>（暂时还没有韩语单集。）</p>
  </div>
{% endif %}
</div>