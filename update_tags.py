import os
import re
from bs4 import BeautifulSoup
import yaml

def get_episode_number_from_title(title):
    match = re.search(r"Episode (\d+)", title)
    if match:
        return int(match.group(1))
    return None

def get_tags_from_card(card):
    tags = []
    tags_p = card.find("p", class_="tags")
    if tags_p:
        for span in tags_p.find_all("span"):
            tags.append(span.text)
    return tags

def main():
    with open("episodes.html", "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")
    episode_cards = soup.find_all("div", class_="episode-card")

    episode_tags = {}
    for card in episode_cards:
        title_h2 = card.find("h2")
        if title_h2:
            title = title_h2.text
            episode_number = get_episode_number_from_title(title)
            if episode_number:
                tags = get_tags_from_card(card)
                episode_tags[episode_number] = tags

    episodes_dir = "collections/_episodes"
    for filename in os.listdir(episodes_dir):
        if filename.endswith(".md"):
            filepath = os.path.join(episodes_dir, filename)
            
            match = re.search(r"episode-(\d+)\.md", filename)
            if match:
                episode_number = int(match.group(1))
                if episode_number in episode_tags:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    parts = content.split("---")
                    if len(parts) >= 3:
                        try:
                            front_matter = yaml.safe_load(parts[1])
                            front_matter["tags"] = episode_tags[episode_number]
                            
                            with open(filepath, "w", encoding="utf-8") as f:
                                f.write("---\n")
                                yaml.dump(front_matter, f, allow_unicode=True, sort_keys=False)
                                f.write("---" + "---".join(parts[2:]))
                            print(f"Updated tags for {filename}")
                        except yaml.YAMLError as e:
                            print(f"Error parsing YAML in {filename}: {e}")

if __name__ == "__main__":
    main()
