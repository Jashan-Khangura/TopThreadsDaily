import praw
import openai
import tweepy
import random

reddit_client_id = ""
reddit_client_secret = ""
reddit_user_agent = ""
reddit_username = ""
reddit_password = ""

reddit = praw.Reddit(
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    user_agent=reddit_user_agent,
    password=reddit_password,
    username=reddit_username
)

openai_api_key = ""

openai.api_key = openai_api_key

twitter_consumer_key = ''
twitter_consumer_secret = ''
twitter_access_token = ''
twitter_access_token_secret = ''
twitter_bearer_token = ''

client = tweepy.Client(
    consumer_key=twitter_consumer_key,
    consumer_secret=twitter_consumer_secret,
    access_token=twitter_access_token,
    access_token_secret=twitter_access_token_secret,
    bearer_token=twitter_bearer_token)


def buildThread():
    try:
        top_posts = []
        for submission in reddit.subreddit("technology+Futurology+worldbuilding").top(time_filter="day", limit=50):
            top_posts.append(submission)
        random_int = random.randint(0, 49)
        random_post = top_posts[random_int]
        response = analysePost(random_post)
        client.create_tweet(text=response.strip(), user_auth=True)
    except Exception as e:
        print(f"Error while fetching post from Reddit or while posting tweet: {e}")


def analysePost(top_post):
    top_comments = top_post.comments
    top_comments = [comment.body for comment in top_comments[:10]]
    prompt = (f"Analyze the following Reddit post, including its title, description, and comments. Based on this "
              f"analysis, create a Twitter post of upto 280 characters that presents "
              f"the information in a natural and engaging way,"
              f"as if you came across this topic yourself. Also, give your opinion based on the information. Don't "
              f"directly reference Reddit or the post"
              f"itself; the goal is to make it feel like it's your own observation or thought. The tone should be "
              f"conversational, insightful, and appropriate for a Twitter audience and no images or links"
              f"\nTitle: {top_post.title}\nComments: "
              f"{top_comments}\nDescription: {top_post.selftext}")

    response = openai.chat.completions.create(
        model="",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    return response.choices[0].message.content.strip()


if __name__ == '__main__':
    buildThread()
