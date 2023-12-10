import twint   #Since I do not posess any means of accessing Tweepy as of current

# Function to fetch tweets
def fetch_tweets(hashtag, limit=100, output_file='tweets.json'):
    """
    Fetch tweets containing the specified hashtag and save them to a JSON file.
    """
    # Configure Twint
    c = twint.Config()
    c.Search = hashtag
    c.Limit = limit
    c.Store_json = True
    c.Output = output_file

    
    twint.run.Search(c)

if __name__ == "__main__":
    fetch_tweets("#afetadres")
