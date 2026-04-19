You need to apply for an [instapaper developer API key](https://www.instapaper.com/developers/applications) in order for this tool to work. After that, you can enter your instapaper login details into the .env file and then `docker compose up`.

You can manually run the instapaper downloader with this command: `docker compose run --rm instapaper-downloader`

You also need to setup a crontab so that this will run every set interval. 

2. Open the Crontab editor
```Bash
crontab -e
```

3. Add the sync schedule
Add the following line to the bottom of the file with your directory path. This example runs the sync every 30 minutes:
Code snippet
```
*/30 * * * * cd /path/to/your/repo && /usr/bin/docker compose run --rm instapaper-downloader >> sync.log 2>&1
```
