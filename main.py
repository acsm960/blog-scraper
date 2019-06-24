

import feedparser
import json
import hashlib
import re
import datetime
import time
from email import utils
import pprint



def main():
    print("Hello {}!".format("Worldz"))

    # blogs.append("https://sec6441.tumblr.com/rss")
    # blogs.append("https://kxy-6441.tumblr.com/rss")
    # blogs.append("https://acsm6441.tumblr.com/rss")
    # blogs.append("https://blog.securityengineering.online/feed/")
    
    blogs = []
    listOfBlogs = open("blogs.txt", "r")
    for blog in listOfBlogs:
        blogs.append(blog)


    allBlogs = {}
    try:
        with open("logs/allBlogs.json", 'r') as fp:
                allBlogs = json.load(fp)
    except:
        print ("Couldn't find existing file. New file will be created.")


    for blogURL in blogs:
        print(" ----", blogURL, "---- ")

        canonicalURL = getCanonicalURL(blogURL)
        filename = "logs/" + canonicalURL + ".json"

        # Extract previous blog history
        blogHistory = {}
        blogHistory["data"] = {}
        blogHistory["logs"] = []
        try:
            with open(filename, 'r') as fp:
                blogHistory = json.load(fp)
        except:
            print ("Couldn't find existing log for ", canonicalURL)
    
    # Grab the blog's RSS feed and iterate through it. 
        try:
            blogFeed = feedparser.parse(blogURL)

            for post in blogFeed['entries']:
      
                currentTime = getCurrentTimeString()

                # Create JSON object to hold details about this blog. 
                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(post)
                # print(post)

                blogPost = {}
                blogPost['GUID'] = post['id'] 
                blogPost['title'] = post['title_detail']['value']
                if 'summary' in post:
                    blogPost['content'] = post['summary']
                else:
                    blogPost['content'] = ""
                blogPost['published'] = post['published']
                blogPost['scrapeDate'] = currentTime
                try:
                    blogPost['previousScrapeDate'] = blogHistory["logs"][-1]
                except:
                    print ("ERROR GETTING PREVIOUS SCRAPE DATE")
                    blogPost['previousScrapeDate'] = ""
                # print (blogPost)
                
                # Unique identifiers for this post
                guid = post['id']
                uniqueIdentifier = blogPost['title'] + blogPost['content'] + blogPost['published']
                versionIDHash = hashlib.sha256(uniqueIdentifier.encode('utf-8')).hexdigest()



                # HANDLING VERSIONING OF POSTS
                # Grab previous versions of this post, if they exist
                try:
                    blogPostVersions = blogHistory["data"][guid]
                except:
                    blogPostVersions = {}

                print ("Unique Identifier is ", uniqueIdentifier)
                print (versionIDHash)

                # Add this version of this blog post
                if versionIDHash not in blogPostVersions:
                    blogPostVersions[versionIDHash] = blogPost #Add this blog post as a version of this post. 
                blogHistory["data"][guid] = blogPostVersions # Add all versions of this post to list of all posts. 
        except:
            print ("Couldn't find feed, or an error occured. Skipping : ", canonicalURL)

        blogHistory["logs"].append((getCurrentTimeString()))

        # print ("Printing data ", blogHistory)
        # Write all of the blog's history out to a file.
        with open(filename, 'w') as fp:
            json.dump(blogHistory, fp, sort_keys=False, indent=4)

        # Add this blog to the list containing all blogs and their data. 
        allBlogs[canonicalURL] = blogHistory

    #Write all blogs and their posts and history to file. 
    with open("logs/allBlogs.json", 'w') as fp:
        json.dump(allBlogs, fp, sort_keys=True,  indent=4)


def getCurrentTimeString():
    nowdt = datetime.datetime.now()
    nowtuple = nowdt.timetuple()
    nowtimestamp = time.mktime(nowtuple)
    timestamp = utils.formatdate(nowtimestamp)
    return timestamp


def getCanonicalURL(URL):
    result = re.search('(?<=\/\/).*?(?=/)', URL)
    canonicalURL = result.group()
    # print("Canonical name : ", result.group() )
    return result.group()

def readRSS():
    d = feedparser.parse('https://sec6441.tumblr.com/rss')
    entries = d['entries']
    for entry in entries:
        print (entry['title'])
        # print(entry)
    # print (d)
    try:
        d = feedparser.parse('https://sec6441.tumblr.com/rss')
        entries = d['entries']
        for entry in entries:
            print (d['title'])
        print (d)
    except:
        print("whoops")

    # print (d)


if __name__ == '__main__':
    main()
    # readRSS()
