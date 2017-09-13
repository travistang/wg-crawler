# wg-crawler
A script for crawling ads

## Prerequisite
* docker-compose

## Installation
<code>
  git clone https://github.com/travistang/wg-crawler
</code>

## Usage
1. Fill in the <code>INFO</code> dictionary in <code>wg-crawler/wggesucht/wggesucht/settings.py</code> according to your need.
2. Start the compose.
<p><code>
cd wg-crawler
</code></p>
<p><code>
APP_ID=wggesucht MASTER_KEY=wggesucht REST_API_KEY=wggesucht PARSE_DASHBOARD_ALLOW_INSECURE_HTTP=1 ALLOW_INSECURE_HTTP=1 PARSE_DASHBOARD_ALLOW_INSECURE_HTTP=1 ALLOW_CLIENT_CLASS_CREATION=1 SERVER_URL=http://localhost:1337/parse docker-compose up -d --build
</code></p>
3. You should see emails from WG-Gesucht that informs you you have sent out email to the landlords.

## FAQ
### How to stop the crawler?

1. <p><code>cd wg-crawler; # go to the directory where docker-compose.yml is in</code></p>
2. <p><code>docker-compose down</code></p>

### How do I see what is crawled?

visit http://localhost:4040 and you will see a dashboard. Then log in with the credential <code>wg:wggesucht</code>
