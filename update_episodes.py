import feedparser
import yaml
import os
import urllib.request
from time import strftime
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# --- 配置 ---
# 这是你找到的正确 RSS Feed 地址
RSS_FEED_URL = "https://anchor.fm/s/1072535c0/podcast/rss"
DATA_FILE_PATH = "_data/episodes.yml"
# ----------------

def get_language_from_tags(tags, title):
    """
    从播客的 'tags' (类别) 中提取语言。
    (已修复: 现在 title 被正确传递进来了)
    """
    for tag in tags:
        term = tag.get('term', '').strip().lower() # 转换为小写
        if term in ['chinese', 'mandarin']:
            return 'Chinese'
        if term == 'english':
            return 'English'
        if term == 'korean':
            return 'Korean'
    
    # 如果标签里找不到，就从标题里猜
    title_lower = title.lower() # <-- BUG 已修复
    if '(chinese)' in title_lower:
        return 'Chinese'
    if '(english)' in title_lower:
        return 'English'
    if '(korean)' in title_lower:
        return 'Korean'
            
    return 'Unknown' # 默认值

def get_audio_url(links):
    """从 'links' 列表中找到音频文件 (enclosure)。"""
    for link in links:
        if link.get('rel') == 'enclosure':
            return link.get('href')
    return None

def parse_date_to_iso(published_parsed):
    """将 feedparser 的日期元组转换为 ISO 8601 字符串。"""
    try:
        # 转换为 ISO 8601 格式 (YYYY-MM-DDTHH:MM:SSZ)
        return strftime('%Y-%m-%dT%H:%M:%S%z', published_parsed)
    except Exception:
        return None

def fetch_feed(url):
    """
    使用 'User-Agent' 伪装成浏览器来抓取 feed。
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req) as response:
            content = response.read()
            feed = feedparser.parse(content)
            return feed
            
    except Exception as e:
        print(f"严重错误: 抓取 feed 时失败。错误: {e}")
        return None


def main():
    print(f"开始抓取 RSS feed: {RSS_FEED_URL}")
    feed = fetch_feed(RSS_FEED_URL)
    
    if not feed:
        print("错误: 无法获取 feed。脚本终止。")
        return

    if feed.bozo:
        print(f"错误: 无法解析 RSS feed。原因: {feed.bozo_exception}")
        return

    if not feed.entries:
        print("错误: RSS feed 中没有找到任何 'entries'。")
        return

    # 1. 加载已有的播客数据
    existing_guids = set()
    episodes_collection_path = "collections/_episodes"
    if os.path.exists(episodes_collection_path):
        for filename in os.listdir(episodes_collection_path):
            if filename.endswith(".md"):
                filepath = os.path.join(episodes_collection_path, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    try:
                        # Simple YAML front matter parsing
                        content = f.read()
                        if content.startswith("---"):
                            end_of_front_matter = content.find("---", 3)
                            if end_of_front_matter != -1:
                                front_matter_str = content[3:end_of_front_matter]
                                front_matter = yaml.safe_load(front_matter_str)
                                if front_matter and front_matter.get('guid'):
                                    existing_guids.add(front_matter['guid'])
                    except Exception as e:
                        print(f"警告: 无法解析文件 {filename}。错误: {e}")
        print(f"成功加载 {len(existing_guids)} 条已有的播客数据。")
    else:
        print(f"文件夹 {episodes_collection_path} 未找到，将创建新文件夹。")
        os.makedirs(episodes_collection_path)

    # Get the Spotify API credentials from the user
    client_id = input("Enter your Spotify Client ID: ")
    client_secret = input("Enter your Spotify Client Secret: ")

    # Authenticate with the Spotify API
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # 2. 遍历 RSS feed，查找新单集
    new_episodes_found = []
    for entry in feed.entries:
        # Anchor.fm 使用 'id' 或 'guid'
        guid = entry.get('id') or entry.get('guid')
        
        if not guid:
            print(f"警告: 找到一个没有 'id' 或 'guid' 的 entry，跳过。标题: {entry.get('title')}")
            continue

        if guid not in existing_guids:
            print(f"找到新单集: {entry.get('title')}")
            
            entry_title = entry.get('title', '')
            
            # 提取语言 (已修复)
            language = get_language_from_tags(entry.get('tags', []), entry_title)
            
            # 提取音频 URL
            audio_url = get_audio_url(entry.get('links', []))
            
            # 提取并格式化日期
            published_date = parse_date_to_iso(entry.get('published_parsed'))
            
            description = entry.get('description', 'No Description')

            # 提取封面图片
            cover_url = None
            if 'image' in entry and entry.image and 'href' in entry.image:
                cover_url = entry.image.href

            # Search for the episode on Spotify
            results = sp.search(q=entry_title, type='episode', limit=1)
            if results['episodes']['items']:
                track = results['episodes']['items'][0]
                spotify_url = track['external_urls']['spotify']
            else:
                spotify_url = entry.get('link')

            new_ep = {
                'title': entry_title,
                'guid': guid,
                'link': spotify_url,
                'published_date': published_date,
                'description': description,
                'audio_url': audio_url,
                'language': language,
                'cover': cover_url
            }
            new_episodes_found.append(new_ep)
            existing_guids.add(guid) # 确保不会重复添加

    # 3. 将新单集（如果有）写入新文件
    if new_episodes_found:
        print(f"共找到 {len(new_episodes_found)} 条新单集。正在创建新文件...")
        
        for new_ep in new_episodes_found:
            try:
                # Extract episode number from title
                import re
                match = re.search(r"Episode\s*(\d+)", new_ep['title'], re.IGNORECASE)
                if match:
                    episode_number = match.group(1)
                    filename = f"episode-{episode_number}.md"
                    filepath = os.path.join("collections/_episodes", filename)
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write("---\n")
                        yaml.dump(new_ep, f, allow_unicode=True, sort_keys=False)
                        f.write("---\n")
                    print(f"成功创建文件: {filepath}")
                else:
                    print(f"警告: 无法从标题中提取集数: {new_ep['title']}")

            except Exception as e:
                print(f"严重错误: 无法写入文件。错误: {e}")
    else:
        print("没有找到新单集。文件未改动。")

if __name__ == "__main__":
    main()
