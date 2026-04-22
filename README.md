# Prerequisites

- Docker engine
- Instapaper API key - You need to apply for an [here](https://www.instapaper.com/developers/applications)

# Install

### 1. Clone and enter the repo
```
git clone https://github.com/naivchan/instapaper-to-opds.git
cd instapaper-to-opds
```

### 2. Copy the environment template and populate it with your Instapaper API credentials.
```
cp .env.example .env
nano .env
```

### 3. Start the web server container
```
docker compose up -d
```

### 4. Run the initial sync to populate the feed
```
docker compose run --rm instapaper-downloader
```

### 5. Setup the automation for the tool to refresh

Open the Crontab editor
```Bash
# Open the Crontab editor
crontab -e
```

Add the following line to the bottom of the file with your directory path. This example runs the sync every 30 minutes:
```
# Example Crontab for running instapaper-downloader every 30 minutes
*/30 * * * * cd /path/to/your/repo && /usr/bin/docker compose run --rm instapaper-downloader >> sync.log 2>&1
```

### 6. Access
Your OPDS catalog is now live at:
http://<your-vps-ip>:<port>
