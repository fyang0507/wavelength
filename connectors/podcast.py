"""Ref: https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/index.html"""
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

        # Initialize variables to None
        title = pubDate = duration = summary = link = description = episode = None

        # Extract link from enclosure tag if present
        enclosure_tag = latest_item.find('enclosure')
        if enclosure_tag is not None and 'url' in enclosure_tag.attrib:
            link = enclosure_tag.attrib['url']

        # Parse other details
        for child in latest_item:
            tag_name = child.tag.split('}')[-1] # Handle potential namespaces

            if tag_name == 'title':
                title = child.text
            elif tag_name == 'pubDate':
                pubDate = child.text
            # Check for namespaced duration tag first
            elif tag_name == 'duration' and 'itunes' in child.tag: 
                duration = child.text
            # Check for namespaced summary tag first
            elif tag_name == 'summary' and 'itunes' in child.tag: 
                summary = child.text
            elif tag_name == 'description':
                 # Prefer description if itunes:summary not found or is different
                description = child.text 
            # Check for namespaced episode tag, avoiding episodeType
            elif tag_name == 'episode' and 'itunes' in child.tag and 'episodeType' not in child.tag:
                 episode = child.text
            # Fallback to non-namespaced duration/summary if necessary (less common)
            elif tag_name == 'duration' and duration is None:
                 duration = child.text
            elif tag_name == 'summary' and summary is None:
                 summary = child.text
        
        # Use description as summary if summary is still None
        if summary is None:
            summary = description

        return {
            "title": title,
            "published_at": pubDate,
            "duration": duration,
            "summary": summary,
            "link": link, # Use the extracted enclosure URL
            "description": description,
            "episode": episode
        }
        
    except requests.RequestException as e:
        print(f"Error fetching podcast data: {e}")
        return None # Return None on error
    except Exception as e:
        print(f"Error processing podcast data: {e}")
        return None # Return None on error


def main():
    # Example usage
    # podcast_name = "Decoder with Nilay Patel"
    podcast_name = "Greymatter"
    print(f"TEST: Fetching latest episode for {podcast_name}")
    result = get_latest_episode(podcast_name) 
    
    if result: 
        print("\\nLatest Episode Metadata:")
        print("-" * 50)
        # Handle potential None values when printing
        for key, value in result.items():
            print(f"{key.replace('_', ' ').title()}: {value if value is not None else 'N/A'}")


if __name__ == "__main__":
    main()
