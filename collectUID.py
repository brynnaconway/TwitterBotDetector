import tweepy
import json

# Authentication details. To  obtain these visit dev.twitter.com

# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):

    def __init__(self): 
        self.count = 0
        self.users = set()

    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)
        if len(self.users) <= 500:
            try:
                self.count += 1
                self.users.add(decoded['user']['id'])
                return True
            except:
                return True
        else:
            for user in self.users:
                print user
            exit(1)

    def on_error(self, status):
        print(status)
        exit(1)

if __name__ == '__main__':
    l = StdOutListener()

    #auth = tweepy.OAuthHandler('MQfvmonUl6Ma0BqIDZPf8TgV8','PlsljRGIeseuQP8q14QdFdXdxycNoD3mEbobMV7DkZlANwnpWR')
    #uth.set_access_token('965192514-d88SjfmStUJ1ydFo3QIFRm6RrH6iyKu7N3X3gz96', 'D1awNzlohgmHVfPw07oeLE2QrVXi4wFKvCeSDinkazvbl')

    auth = tweepy.OAuthHandler("Xz1swASBUvn63XdoaWyv8pVh8", "3DjVqTTBWhFkb0ls9m4bGVvygQICXqYIWC8ybsU0NZqOcazXdi")
    auth.set_access_token("752284238-aMurTFUTrYE3GHZHciybB7WLds7WrqYjvuMWvLNY", "85ctdbbNSH8EqTdiJiqvIzgkcjTdDxIrXKdyGMqg4mAQ9")
    api = tweepy.API(auth)
    #print("Showing all new tweets for #programming:")

    # There are different kinds of streams: public stream, user stream, multi-user streams
    # In this example follow #programming tag
    # For more details refer to https://dev.twitter.com/docs/streaming-apis
    stream = tweepy.Stream(auth = auth, listener = l)

    stream.filter(track=["a", "the", "I", "."], languages=['en'], async=True)
