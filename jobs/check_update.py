"""
[GENERATED BY CURSOR]
This script retrieves the latest updates from various content sources
listed in subscriptions.toml, checks for new content, and caches update information.

This implements the first phase of the two-phase content retrieval approach:
1. Check for updates and cache minimal metadata (this script)
2. Retrieve full content details when needed (implemented in jobs/preprocess.py)
"""

from utils.logging_config import logger
from connectors.sources.youtube import YoutubeConnector
from connectors.sources.podcast import PodcastConnector
from connectors.sources.bilibili import BilibiliConnector
from connectors.sources.website.pipeline import WebsiteConnector
from utils.toml_loader import load_toml_file
from utils.connector_cache import ConnectorCache
import asyncio


async def process_youtube_channels(youtube_channels):
    """Check for updates from YouTube channels and return results."""
    for channel_name in youtube_channels:
        logger.info(f"Checking for updates from YouTube channel: {channel_name}")
        try:
            # YoutubeConnector takes channel and optional duration_min. API key is handled internally.
            youtube_connector = YoutubeConnector(channel=channel_name) 
            await youtube_connector.check_latest_updates() # Populates cache, returns None
        except Exception as e:
            logger.error(f"Error processing YouTube channel {channel_name}: {e}", exc_info=True)


async def process_podcasts(podcast_names):
    """Check for updates from podcasts and return results."""
    for podcast_name in podcast_names:
        logger.info(f"Checking for updates from podcast: {podcast_name}")
        try:
            podcast_connector = PodcastConnector(podcast_name) 
            await podcast_connector.check_latest_updates() 
        except Exception as e:
            logger.error(f"Error processing Podcast {podcast_name}: {e}", exc_info=True)


async def process_bilibili(bilibili_users):
    """Check for updates from Bilibili users and return results."""
    
    if not bilibili_users:
        logger.info("No Bilibili users found in subscriptions.")
        return
            
    for user in bilibili_users:
        uid = user.get('uid')
        name = user.get('name')            
        logger.info(f"Checking for updates from Bilibili user: {name} (uid: {uid})")
        try:
            bilibili_connector = BilibiliConnector(uid=uid, channel=name) 
            await bilibili_connector.check_latest_updates() 
        except Exception as e:
            logger.error(f"Error processing Bilibili user {name}: {e}", exc_info=True)
            
        await asyncio.sleep(2) # Keep the delay, but make it non-blocking


async def process_websites(websites):
    """Check for updates from websites and return results."""
    for website_subscription in websites:
        channel = website_subscription.get('channel')
        source_url = website_subscription.get('source_url')
            
        logger.info(f"Processing website subscription: {channel} ({source_url})")
        
        try:
            website_connector = WebsiteConnector(channel=channel, source_url=source_url) 
            await website_connector.check_latest_updates()
        except Exception as e:
            logger.error(f"Error during website_check_updates for {channel} ({source_url}): {e}. Skipping.")        


async def main():
    """Main function to check for updates from all sources and save results."""
    try:

        cache = ConnectorCache()
        cache.clear_old_cache(days=0) # clear all caches
        
        subscriptions = load_toml_file("subscriptions.toml")

        # Schedule all processing tasks to run concurrently
        logger.info("Scheduling update checks for all sources...")
        youtube_task = process_youtube_channels(subscriptions.get('youtube', []))
        podcast_task = process_podcasts(subscriptions.get('podcast', []))
        bilibili_task = process_bilibili(subscriptions.get('bilibili', []))
        website_task = process_websites(subscriptions.get('website', []))

        logger.info("Starting concurrent update checks...")
        await asyncio.gather(
            youtube_task,
            podcast_task,
            bilibili_task,
            website_task
        )
        logger.info("Concurrent update checks completed.")

    except Exception as e:
        logger.error(f"An error occurred during update checking: {str(e)}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(main()) 