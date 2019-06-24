# blog-scraper
Dockerised python script for logging all versions of blogs via their RSS feed. 

##Usage

1. Install docker

```apt install docker.io```

2. Add list of blog RSS feeds in ./blogs.txt

3. Run Script

```docker-compose up```

4. Recommend setting a cronjob to scan daily.


You will find a JSON object in the /logs directory which contains all the blogs. 