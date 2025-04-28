# Personal TLDR
Ever drown in countless notification and lose track of what's most interesting? Use personal TLDR to let AI sort and digest your subscriptions.


## Supported: 

Media | Platform | Connector
-|-|-|
Audio | Apple Podcast | API (iTunes search)
Video | Youtube | API (data API, captions not available, need OAuth2)
Video | Bilibili | API (recArchivesByKeywords)


## To cover:
- Other podcasts (jike, xiaoyuzhou, etc.) can possibly try [listennotes](https://www.listennotes.com/)
- Wechat public account
- Newsletter: TLDR, The Batch, AlphaSignal, Snack
- Website: a16z, sequoia
- Substack

## Improvements
-  use AI to summarize the multimedia (cost?): can we use audio/video -> llm -> summary instead? need to estimate cost
- add status updates for each connectors
- duration is missing
- only need to retain the latest entry for each channel (filter.py)
- one podcast does not have good summary and the channel name is wrong
- need to convert UTC to EDT time

## Noticeable OSS *not* used
|OSS|Use|Why not used|
-|-|-|
[wewe-rss](https://github.com/cooderl/wewe-rss) | Retrieve wechat public account | Not stable |
[RSSHub](https://github.com/DIYgod/RSSHub) | "Everything is RSSible" | Some sources are not stable


## Technology
- [MarkItDown](https://github.com/microsoft/markitdown)
  - useful for Youtube video with captions enabled
- any possibility for using Notion MCP?
- Stagehand