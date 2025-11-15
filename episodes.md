---
title: All Episodes
layout: default
permalink: /episodes.html
body_class: episode-page
---

# All Episodes

<div class="row">

{% comment %}
  *** MODIFICATION ***
  1. 我们现在从 `site.data.episodes` (the YAML file) 读取
  2. 我们的 Python 脚本已经按日期排好序了 (最新的在最前),
     所以我们不再需要 'sort' 或 'reverse'。
{% endcomment %}
{% assign eps = site.data.episodes %}

{% if eps and eps.size > 0 %}
  {% for ep in eps %}
  <div class="col col-4 col-t-6 col-m-12">
    <article class="c-blog-card">
      <div class="c-blog-card__inner">
        <div class="c-blog-card__image-wrapper">
          {% comment %}
            *** MODIFICATION ***
            1. 链接: 使用 'ep.link' (来自 YAML)。
            2. 封面: 'ep.cover' 在我们的 YAML 中不存在,
               所以 `default` 会自动使用你的 '/images/podcast-cover.png'。
               (这很完美!)
          {% endcomment %}
          <a class="c-blog-card__image" href="{{ ep.link }}" target="_blank" rel="noopener">
            <img src="{{ ep.cover | relative_url }}" alt="{{ ep.title | escape }}">
          </a>
        </div>
        <div class="c-blog-card__text-content">
          <div class="c-blog-card__tags-box">
            {% comment %}
              *** MODIFICATION ***
              我们用 'ep.language' (来自 YAML) 替换了 'ep.tags'。
            {% endcomment %}
            {% if ep.language and ep.language != 'Unknown' %}
              <span class="c-blog-card__tag">{{ ep.language }}</span>
            {% endif %}
          </div>
          <h3 class="c-blog-card__title">
            <a href="{{ ep.link }}" target="_blank" rel="noopener">{{ ep.title }}</a>
          </h3>
          {% comment %}
            *** MODIFICATION ***
            我们用 'ep.description' (来自 YAML) 替换了 'ep.excerpt'。
            我们必须 'strip_html' (去除HTML) 和 'truncatewords' (截断)
            否则它会破坏你页面的布局。
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
    <p>（_data/episodes.yml 文件为空或未找到。请在本地运行 <code>python3 update_episodes.py</code>。）</p>
  </div>
{% endif %}
</div>