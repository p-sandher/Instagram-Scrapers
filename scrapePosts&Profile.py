import instaloader
import csv
import os

def scrape_instagram_profile_and_posts(username, post_count=20):
    # Initialize Instaloader
    L = instaloader.Instaloader()

    # Load the profile
    profile = instaloader.Profile.from_username(L.context, username)

    # Extract profile information
    profile_info = {
        'username': profile.username,
        'followers': profile.followers,
        'post_count': profile.mediacount,
    }

    # Initialize a list to store post data
    posts_data = []

    # Iterate over the profile's posts
    for post in profile.get_posts():
        if len(posts_data) >= post_count:
            break
        post_info = {
            'url': f"https://www.instagram.com/p/{post.shortcode}/",
            'likes': post.likes,
            'hashtags': ', '.join(post.caption_hashtags),  # Convert list to string
            'location': None  # Default to None
        }

        # Check if the post has a location tag in its caption
        if post.location is not None:
            post_info['location'] = f"{post.location.name} (Lat: {post.location.lat}, Lng: {post.location.lng})"

        posts_data.append(post_info)

    return profile_info, posts_data

def save_to_csv(profile_info, posts_data, csv_filename, field):
    # Check if the file already exists
    file_exists = os.path.isfile(csv_filename)

    # Write profile information and post details to CSV file
    with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write header row if the file is newly created
        if not file_exists:
            writer.writerow(['Field', 'Username', 'Followers', 'Post Count', 'Post URL', 'Likes', 'Hashtags', 'Location'])

        # Write profile information and field
        for post in posts_data:
            writer.writerow([field, profile_info['username'], profile_info['followers'], profile_info['post_count'], post['url'], post['likes'], post['hashtags'], post['location']])

def main(username, csv_filename, field):
    profile_info, recent_posts = scrape_instagram_profile_and_posts(username)
    save_to_csv(profile_info, recent_posts, csv_filename, field)


csv_filename = 'instagram_data.csv'  

# Specify the Instagram username 
username = 'championsleague' 
field = 'Sports'  
main(username, csv_filename, field)

username = 'tomholland2013' 
field = 'Movies'  
main(username, csv_filename, field)

username = 'akaashsingh' 
field = 'Comedy'  
main(username, csv_filename, field)
