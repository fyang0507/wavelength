# Wavelength: Deep Focus On The Content That Matters
Jumping between apps to track subscribed creators only to discover irrelevant contents? Stop the endless scroll! Wavelength gathers your favorite subscriptions in one place, filtering out the noise using AI and serving up only the meaningful content you actually matches your wavelength.

## Don't TLDR: Obsession with depth and quality
In the era of information overflow and "ChatGPT, can you summarize this for me?", I am still a believer in watching long videos, listening to long podcasts, and reading long articles because (1) **context matters**, and (2) I want to pay respect to creators who thoughtfully produced the whole content.

Wavelength is about solving the "how should I spend my free time" problem, not overwhelming myself with exhaustive updates on world events as if I require presidential-level briefings.

For the latter purpose, open-source projects like [Folo](https://github.com/RSSNext/Folo) or [Meridian](https://github.com/iliane5/meridian) that focus on the "recall" and "timeliness" aspects of information, and curated digests like [TLDR newsletter](https://tldr.tech/) (one of my favorites) offering byte-sized themed summaries are better choices. Wavelength is not about substituting these channels but compliment them.

In wavelength, I made a conscious choice not to build tldr-over-tldr (name inspired by FOF, or [Fund of Funds](https://en.wikipedia.org/wiki/Fund_of_funds)). Instead, this project sources quality content directly from its original publishers.

## Key program flow
* Search daily for new content from the provided subscription list
* Given user preference, sort new updates in must-see (a time limit for it), nice-to-see, you-may-not-like categories
* Generate Daily Digest and Weekly in-case-you-missed-this (given user's status update) in Notion

## Supported: 

Media | Platform | Connector
-|-|-|
Audio | Apple Podcast | API (iTunes search)
Video | Youtube | API (data API, captions not available, need OAuth2)
Video | Bilibili | API (recArchivesByKeywords)


## To cover:
- Other podcasts (jike, xiaoyuzhou, etc.) can possibly try [listennotes](https://www.listennotes.com/)
- Wechat public account (highly impossible)
- Newsletter: TLDR, The Batch, AlphaSignal, Snack
- Website: a16z, sequoia
- Substack

## Improvements
-  use AI to summarize the multimedia (cost?): can we use audio/video -> llm -> summary instead? need to estimate cost
- ~~add status updates for each connectors~~
- ~~duration is missing~~
- **only need to retain the latest entry for each channel (filter.py)**
- ~~one podcast does not have good summary and the channel name is wrong~~
- need to convert UTC to EDT time

## Noticeable OSS *not* used
|OSS|Use|Why not used|
-|-|-|
[wewe-rss](https://github.com/cooderl/wewe-rss) | Retrieve wechat public account | Not stable |
[RSSHub](https://github.com/DIYgod/RSSHub) | "Everything is RSSible" | Some sources are not stable


## Mostly vibe coded
This project is mostly vibe coded through Cursor.

## Technology
- [MarkItDown](https://github.com/microsoft/markitdown)
  - useful for Youtube video with captions enabled
- any possibility for using Notion MCP?
- Stagehand

## Challenges to parse newsletters

- Tried various combinations of [trafilatura](https://github.com/adbar/trafilatura), [MarkItDown](https://github.com/microsoft/markitdown), [markdownify](https://github.com/matthewwithanm/python-markdownify) / [html-to-markdown](https://github.com/Goldziher/html-to-markdown). No matter we go from
  - html -> cleaned_html -> md
  - html -> md
  - html -> pdf -> md
  - no methods work satisfactory to faithfully preserve the document