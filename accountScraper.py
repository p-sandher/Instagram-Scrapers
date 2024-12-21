import instaloader
import csv
import os

# scrapeInstagramProfileAndPosts: Retrieve an instagram profile and get the 20 latest posts
def scrapeInstagramProfileAndPosts(username, postCount=20):
    L = instaloader.Instaloader()
    profile = instaloader.Profile.from_username(L.context, username)
    profileInfo = {
        'username': profile.username,
        'followers': profile.followers,
    }
    postsData = []
    for post in profile.get_posts():
        if len(postsData) >= postCount:
            break
        postInfo = {
            'url': f"https://www.instagram.com/p/{post.shortcode}/",
        }
        postsData.append(postInfo)
    return profileInfo, postsData

# saveToCSV: Write profile/post analytics to a csv file
def saveToCsv(profileInfo, postsData, csvFilename, field):
    fileExists = os.path.isfile(csvFilename)
    with open(csvFilename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not fileExists:
            writer.writerow(['Field', 'Username', 'Followers', 'Post URL'])
        for post in postsData:
            writer.writerow([field, profileInfo['username'], profileInfo['followers'], post['url']])

# processCsv:  Reads a csv and gets the instagram usernames of various profiles
def processCsv(inputCsvFilename, outputCsvFilename):
    with open(inputCsvFilename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            field, username = row
            profileInfo, recentPosts = scrapeInstagramProfileAndPosts(username)
            saveToCsv(profileInfo, recentPosts, outputCsvFilename, field)

# Main : create a csv containing instagram analytics of profiles
inputCsvFilename = 'accountUsernames.csv'
outputCsvFilename = 'instagramAccountData.csv'

processCsv(inputCsvFilename, outputCsvFilename)
