import feedparser
import frontmatter
import os
import re
from pathlib import Path
from datetime import datetime
import time
import yaml
from dateutil import parser


# 导入 json 模块，用于处理日期字符串等（虽然最终使用了entry.published）
from json import dumps as json_dumps

# *************** 请修改以下两项配置 ***************

# 你的播客 RSS Feed 地址 (***请替换为你真实的 RSS Feed URL***)
PODCAST_RSS_URL = 'https://anchor.fm/s/1072535c0/podcast/rss' 

# ⬇️ 新增：Jekyll 数据文件的目标路径
DATA_FILE_PATH = Path('..') / '_data' / 'episodes.yml'

# 你的 Jekyll 播客集合目录
EPISODES_DIR = Path('collections/_episodes')
# ⬇️ 新增：Jekyll 数据文件的目标路径
DATA_FILE_PATH = Path('_data') / 'episodes.yml'

# **************************************************

# 辅助函数：将标题转换为 URL 友好格式 (slug)
def slugify(text):
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text) # 移除标点符号
    text = re.sub(r'[-\s]+', '-', text)  # 将空格和连字符合并
    return text.strip('-')

def get_existing_guids():
    """遍历 _episodes 目录，提取现有剧集的 GUID"""
    existing_guids = set()
    print(f"Checking existing files in {EPISODES_DIR}...")
    
    # 确保目录存在
    if not EPISODES_DIR.exists():
        EPISODES_DIR.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {EPISODES_DIR}")
        return existing_guids

    for filepath in EPISODES_DIR.glob('*.md'):
        try:
            # 使用 frontmatter 库安全地读取 Front Matter
            post = frontmatter.load(filepath)
            guid = post.metadata.get('guid')
            if guid:
                existing_guids.add(guid)
        except Exception as e:
            print(f"Warning: Could not read front matter from {filepath}: {e}")
            
    return existing_guids

def update_collection(feed_url):
    """从 RSS Feed 获取并创建新的剧集文件"""
    
    # 1. 获取已存在的 GUID 集合
    existing_guids = get_existing_guids()
    print(f"Found {len(existing_guids)} existing episodes.")
    
    # 2. 获取 RSS Feed
    print(f"Fetching feed from: {feed_url}")
    feed = feedparser.parse(feed_url)
    
    if getattr(feed, 'status', 200) not in [200, 301, 302]:
        print(f"Error fetching feed. Status code: {getattr(feed, 'status', 'N/A')}")
        return False
        
    updates_made = False
    
    # 3. 遍历 Feed 条目
    for entry in feed.entries:
        guid = entry.id
        
        # 4. 检查是否为新剧集
        if not guid or guid in existing_guids:
            continue
            
        print(f"-> Found NEW episode: {entry.title}")
        
        # 5. 提取数据和生成文件
        try:
            # RSS Feed 提供的原始发布日期字符串
            original_published_date = entry.published
            
            # YAML Front Matter 数据，匹配你的第19集格式
            metadata = {
                # 使用 datetime.isoformat() 生成类似 2025-11-22T02:26:42-08:00 的格式
                'published_date': original_published_date, 
                
                # 你的现有文件使用 link 字段作为平台链接
                'link': entry.link, 
                
                'guid': guid,
                'title': entry.title,
                
                # 你的现有文件将描述放在 Front Matter 内
                # feedparser 的描述通常是 HTML 格式
                'description': getattr(entry, 'summary', getattr(entry, 'description', '')),
                
                'audio_url': next((link.href for link in entry.links if link.type and link.type.startswith('audio/')), None),
                
                # 你的现有文件包含这些字段，虽然 RSS Feed 不一定直接提供，但我们保留它们
                'language': 'English', # RSS Feed 应该有语言信息，此处暂用默认值
                'cover': getattr(entry, 'image', {}).get('href', ''), # 尝试获取封面图
                # ⚠️ 注意: 标签信息 RSS Feed 通常不包含，你需要手动编辑
                'tags': [], 
            }
            
            # 文件主体内容设为空，因为描述已放入 Front Matter
            content = ''
            
            # 生成文件名 (Jekyll Collection 文件名只需要 slug)
            filename_slug = slugify(entry.title)
            filepath = EPISODES_DIR / f"{filename_slug}.md"
            
            # 检查文件是否已存在 (以防 slug 重复)
            if filepath.exists():
                print(f"Warning: File {filepath} already exists. Skipping this episode.")
                continue

            # 创建 Post 对象并写入文件
            new_post = frontmatter.Post(content.strip(), handler=frontmatter.YAMLHandler(), **metadata)
            with open(filepath, 'wb') as f:
                frontmatter.dump(new_post, f)
            
            print(f"Successfully created new file: {filepath}")
            existing_guids.add(guid) # 立即加入集合，防止重复创建
            updates_made = True
            
        except Exception as e:
            print(f"Error processing episode {entry.title}: {e}")
            
    return updates_made

def update_data_file():
    """
    遍历 collections/_episodes 目录下的所有文件，提取 front matter，
    并将其按日期降序排列后写入 _data/episodes.yml。
    """
    
    # 存储所有剧集的元数据
    all_episodes_data = []
    
    for file_path in EPISODES_DIR.glob("*.md"):
        # 读取 Markdown 文件
        post = frontmatter.load(file_path)
        
        # 提取所需的元数据
        episode_data = {
            'title': post.metadata.get('title'),
            'guid': post.metadata.get('guid'),
            'link': post.metadata.get('link'),
            'audio_url': post.metadata.get('audio_url'),
            # 使用文件名作为 slug/url 标识符
            'slug': file_path.stem, 
            # 确保日期字段存在，否则无法排序
            'published_date': post.metadata.get('published_date') 
        }
        all_episodes_data.append(episode_data)

    # 按发布日期（published_date）降序排序
    # 按发布日期（published_date）降序排序
    try:
        # 使用 dateutil.parser.parse 来处理复杂的时区格式
        all_episodes_data.sort(key=lambda x: parser.parse(x['published_date']), reverse=True)
    except Exception as e:
        print(f"Warning: Could not sort episodes by date. Error: {e}")

    # 将数据写入 YAML 文件
    try:
        # 确保 _data 目录存在
        DATA_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        with open(DATA_FILE_PATH, 'w', encoding='utf-8') as f:
            # 使用 PyYAML 库写入 YAML
            yaml.dump({'episodes': all_episodes_data}, f, allow_unicode=True, default_flow_style=False)
        
        print(f"-> Successfully updated data file: {DATA_FILE_PATH}")
        return True
    except Exception as e:
        print(f"ERROR: Failed to write to {DATA_FILE_PATH}. {e}")
        return False
    
if __name__ == "__main__":
    try:
        if update_collection(PODCAST_RSS_URL):
            print("Updates were made. Ready to commit.")
        
        # ⬇️ 新增：无论是否有新剧集，都应该同步 _data 文件
        update_data_file() 
        
        # 脚本应该在这里退出
        exit(0)
            
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # 失败时返回非零退出码
        exit(1)
    


