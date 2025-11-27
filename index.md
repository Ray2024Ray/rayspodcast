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

<!-- Latest Episodes：自动抓取站内最近的 6 期（3×2） -->
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
      {% assign eps_all = site.episodes | default: empty %}
      {% if eps_all and eps_all != empty %}
        {% assign latest_eps = eps_all | sort: 'published_date' | reverse | slice: 0, 6 %}
        {% for ep in latest_eps %}
        <div class="col col-4 col-t-6 col-m-12">
          <article class="c-blog-card">
            <div class="c-blog-card__inner">
              <a class="c-blog-card__image" href="{{ ep.link }}" target="_blank" rel="noopener">
                <img src="{{ ep.cover | default: '/images/podcast-cover.png' }}" alt="{{ ep.title | escape }}">
              </a>
              <div class="c-blog-card__content">
                <div class="c-blog-card__tags-box">
                  {% for tag in ep.tags limit:2 %}<span class="c-blog-card__tag">{{ tag }}</span>{% endfor %}
                </div>
                <h3 class="c-blog-card__title">
                  <a href="{{ ep.link }}" target="_blank" rel="noopener">{{ ep.title | remove: "(Chinese)" | remove: "(English)" | remove: "(Korean)" }}</a>
                </h3>
                <p class="c-blog-card__excerpt">{{ ep.description | strip_html | truncatewords: 20 }}</p>
              </div>
            </div>
          </article>
        </div>
        {% endfor %}
      {% else %}
        <div class="col col-12">
          <p>（还没有节目条目。请在 <code>site/collections/_episodes/</code> 新增 6 篇带 <code>title/date/spotify/cover</code> 的 md 文件。）</p>
        </div>
      {% endif %}
    </div>
  </div>
  {% include contact_form.html %}

</section>
