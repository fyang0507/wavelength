import requests
import xml.etree.ElementTree as ET

def get_latest_episode(podcast_name):
    """
    Fetch the latest episode metadata for a given podcast name from Apple Podcasts.
    
    Args:
        podcast_name (str): Name of the podcast channel
    """
    try:
        # Format the URL for iTunes Search API
        base_url = "https://itunes.apple.com/search"
        params = {
            "term": podcast_name,
            "entity": "podcast",
            "limit": 1
        }
        
        # Get the podcast information
        response = requests.get(base_url, params=params)
        # feed is an xml file
        feed =  response.json()['results'][0]['feedUrl']

        # parse the xml feed
        response = requests.get(feed)
        root = ET.fromstring(response.content)

        channel = root.find('channel')
        latest_item = channel.find('item')

        for child in latest_item:
            if 'title' in child.tag:
                title = child.text
            elif 'pubDate' in child.tag:
                pubDate = child.text
            elif 'duration' in child.tag:
                duration = child.text
            elif 'summary' in child.tag:
                summary = child.text
            elif 'link' in child.tag:
                link = child.text
            elif 'description' in child.tag:
                description = child.text
            elif 'episode' in child.tag and 'episodeType' not in child.tag:
                episode = child.text
        
        return {
            "title": title,
            "pubDate": pubDate,
            "duration": duration,
            "summary": summary,
            "link": link,
            "description": description,
            "episode": episode
        }
        
    except requests.RequestException as e:
        print(f"Error fetching podcast data: {e}")
        return e
    except Exception as e:
        print(f"Error processing podcast data: {e}")
        return e

if __name__ == "__main__":
    # Example usage
    podcast_name = input("Enter podcast name: ")
    result = get_latest_episode(podcast_name)
    
    if result:
        print("\nLatest Episode Metadata:")
        print("-" * 50)
        for key, value in result.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
