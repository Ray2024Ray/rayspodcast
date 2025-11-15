---
layout: default
title: Home
lang: en
permalink: /
---

<section class="c-hero">
  <div class="container">
    <div class="c-hero__inner row">
      <!-- 左侧：标题 + 文案 + 按钮 -->
      <div class="c-hero__left col col-6">
        <h1 class="c-hero__title">Cross-cultural Stories</h1>

        <div class="c-hero__description">
          <p>Hi there, I’m Ray, a chemical engineer turned storyteller. In this podcast, I talk to friends, family, and fellow travelers in Mandarin, English, or Korean about the things we bring with us—and the things we leave behind. We explore cultural differences, identity shifts, everyday joy, and emotional struggles. You may hear your own story in ours.</p>
        </div>

        <!-- 订阅平台（只出现一次） -->
        <div class="subscribe-section" style="margin-top:28px;">
          <p style="font-weight:600;margin-bottom:10px;">Subscribe:</p>
          <div class="subscribe-buttons">
            {% if site.podcast.spotify_show %}
            <a class="c-button c-button--primary c-button--small" href="{{ site.podcast.spotify_show }}" target="_blank" rel="noopener">
              <img src="{{ '/images/spotify-icon.png' | relative_url }}" alt="Spotify" style="height:18px;">Spotify
            </a>
            {% endif %}

            {% if site.podcast.apple_show %}
            <a class="c-button c-button--secondary c-button--small" href="{{ site.podcast.apple_show }}" target="_blank" rel="noopener">
              <img src="{{ '/images/apple-icon.png' | relative_url }}" alt="Apple Podcasts" style="height:18px;">Apple Podcasts
            </a>
            {% endif %}

            {% if site.podcast.costbox_show %}
            <a class="c-button c-button--secondary c-button--small" href="{{ site.podcast.costbox_show }}" target="_blank" rel="noopener">
              <img src="{{ '/images/castbox-icon.png' | relative_url }}" alt="Castbox" style="height:18px;">Castbox
            </a>
            {% endif %}

            {% if site.podcast.xiaoyuzhou_show %}
            <a class="c-button c-button--secondary c-button--small" href="{{ site.podcast.xiaoyuzhou_show }}" target="_blank" rel="noopener">
              <img src="{{ '/images/xiaoyuzhou-icon.png' | relative_url }}" alt="小宇宙" style="height:18px;">小宇宙
            </a>
            {% endif %}
          </div>
        </div>
      </div>

      <!-- 右侧：封面图 -->
      <div class="c-hero__right col col-6">
        <div class="c-hero__image">
          <img src="{{ '/images/podcast-cover.png' | relative_url }}" alt="Cross-cultural Stories 封面">
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Latest Episodes： 自动从 _data/episodes.yml 抓取数据 -->
<section class="section">
  <div class="container">
    <div class="section__info">
      <div class="section__head">
        <h2 class="section__title">Latest Episodes</h2>
        <a class="section__link" href="{{ '/episodes.html' | relative_url }}">View all <i class="ion-md-arrow-forward"></i></a>
      </div>
      <div class="section__description">
      </div>
    </div>

    <div class="row">
      {% comment %}
        *** MODIFICATION ***
        我们现在从 _data/episodes.yml (site.data.episodes) 读取
        而不是从 _episodes 文件夹 (site.episodes)
      {% endcomment %}
      {% assign eps_all = site.data.episodes %}

      {% if eps_all and eps_all.size > 0 %}
        {% comment %}
          *** MODIFICATION ***
          我们的 Python 脚本已经按日期排好序了 (最新的在最前)
          所以我们不再需要 'sort' 或 'reverse'，只需要 'slice'
        {% endcomment %}
        {% assign latest_eps = eps_all | slice: 0, 6 %}
        
        {% for ep in latest_eps %}
        <div class="col col-4 col-t-6 col-m-12">
          <article class="c-blog-card">
            <div class="c-blog-card__inner">

              {% comment %}
                *** MODIFICATION ***
                1. 链接: 我们使用 'ep.link' (来自 YAML)
                2. 封面: 'ep.cover' 在我们的 YAML 中不存在,
                   所以它会自动使用你设置的默认封面 '/images/podcast-cover.png'
                   (这很完美!)
              {% endcomment %}
              <a class="c-blog-card__image" href="{{ ep.link }}" target="_blank" rel="noopener">
                <img src="{{ ep.cover | default: '/images/podcast-cover.png' | relative_url }}" alt="{{ ep.title | escape }}">
              </a>
              <div class="c-blog-card__content">
                <div class="c-blog-card__tags-box">
                  {% comment %}
                    *** MODIFICATION ***
                    我们用 'ep.language' 替换了 'ep.tags'
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
                  我们用 'ep.description' (来自 YAML) 替换了 'ep.excerpt'
                  我们必须 'strip_html' (去除HTML) 和 'truncatewords' (截断)
                  否则它会破坏你首页的布局
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
  </div>
  {% include contact_form.html %}

</section>
