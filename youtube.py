"""Ref: https://developers.google.com/youtube/v3/docs/"""
from googleapiclient.discovery import build
from datetime import datetime
import tomllib

def get_channel_id_from_name(channel_name, api_key):
    """
    Get channel ID from channel name/handle
    
    Args:
        channel_name (str): YouTube channel name or handle (with or without '@')
        api_key (str): YouTube Data API key
    
    Returns:
        str: Channel ID or None if not found
    """
    try:
        # Remove @ symbol if present
        channel_name = channel_name.lstrip('@')
        
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        # Search for the channel
        request = youtube.search().list(
            part='snippet',
            q=channel_name,
            type='channel',
            maxResults=1
        ).execute()
        
        if not request['items']:
            return None
            
        channel_id = request['items'][0]['id']['channelId']
        
        # Verify if this is the exact channel by checking the handle/name
        channel_response = youtube.channels().list(
            part='snippet',
            id=channel_id
        ).execute()
        
        if channel_response['items']:
            channel_info = channel_response['items'][0]['snippet']
            # Check if either custom URL or title matches
            if (channel_name.lower() in channel_info.get('customUrl', '').lower() or 
                channel_name.lower() in channel_info['title'].lower()):
                return channel_id
                
        return None
        
    except Exception as e:
        print(f"Error finding channel ID: {str(e)}")
        return None

def get_latest_video_metadata(channel_id, api_key):
    """
    Fetch metadata of the latest video from a YouTube channel
    
    Args:
        channel_id (str): The YouTube channel ID
        api_key (str): Your YouTube Data API key
    
    Returns:
        dict: Video metadata or None if error occurs
    """
    try:
        # Create YouTube API client
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        # First, get the uploads playlist ID of the channel
        channel_response = youtube.channels().list(
            part='contentDetails',
            id=channel_id
        ).execute()
        
        uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        
        # Get the latest video from uploads playlist
        playlist_response = youtube.playlistItems().list(
            part='snippet',
            playlistId=uploads_playlist_id,
            maxResults=1
        ).execute()
        
        if not playlist_response['items']:
            return None
            
        video_data = playlist_response['items'][0]['snippet']
        
        # Get additional video statistics
        video_id = video_data['resourceId']['videoId']
        # video_stats = youtube.videos().list(
        #     part='statistics',
        #     id=video_id
        # ).execute()

        # for testing
        # return {'stats': video_stats, 'data': video_data}
        
        # Combine video data and statistics
        metadata = {
            'title': video_data['title'],
            'description': video_data['description'],
            'published_at': datetime.strptime(video_data['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'),
            'video_id': video_id,
            'url': f'https://www.youtube.com/watch?v={video_id}',
            'thumbnail_url': video_data['thumbnails']['default']['url'], # this could be changed to other sizes
            # 'view_count': video_stats['items'][0]['statistics']['viewCount'],
            # 'like_count': video_stats['items'][0]['statistics'].get('likeCount', 'N/A'),
            # 'comment_count': video_stats['items'][0]['statistics'].get('commentCount', 'N/A'),
        }
        
        return metadata
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def main():
    # Replace with your YouTube Data API key
    with open('.api.toml', 'rb') as f:
        API_KEY = tomllib.load(f)['youtube']
    
    # Get channel name from user
    channel_name = input("Enter the YouTube channel name (with or without @): ")
    
    # Get channel ID
    channel_id = get_channel_id_from_name(channel_name, API_KEY)
    
    if not channel_id:
        print(f"Could not find channel ID for '{channel_name}'")
        return
        
    print(f"Channel ID: {channel_id}")
    metadata = get_latest_video_metadata(channel_id, API_KEY)
    
    if metadata:
        print("\nLatest Video Metadata:")
        print(f"Title: {metadata['title']}")
        print(f"Published: {metadata['published_at']}")
        print(f"URL: {metadata['url']}")
        print(f"Views: {metadata['view_count']}")
        print(f"Likes: {metadata['like_count']}")
        print(f"Comments: {metadata['comment_count']}")
        print(f"\nDescription:\n{metadata['description']}")
    else:
        print("Could not fetch video metadata")

if __name__ == "__main__":
    main()
