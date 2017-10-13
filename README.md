# wg-crawler
A script for crawling ads

## Prerequisite
* docker-compose

## Installation
<code>
  git clone https://github.com/travistang/wg-crawler
</code>

## Usage
1. `cd wg-crawler/wggesucht/wggesucht/`
2. `python d.py`

### How do I see what is crawled?
1. `cd wg-crawler/wggesucht/wggesucht/`
2. `cat ad_list`

### Why didn't the crawler send any emails out?
that's probably because you forgot to set the <code>DONT_SEND</code> field in the <code>INFO</code> dictionary to <code>False</code>
