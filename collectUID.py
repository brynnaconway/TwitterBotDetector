import tweepy
import json

# Authentication details. To  obtain these visit dev.twitter.com

# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)
        print(decoded['user'])
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()

    auth = tweepy.OAuthHandler('MQfvmonUl6Ma0BqIDZPf8TgV8','PlsljRGIeseuQP8q14QdFdXdxycNoD3mEbobMV7DkZlANwnpWR')
    auth.set_access_token('965192514-d88SjfmStUJ1ydFo3QIFRm6RrH6iyKu7N3X3gz96', 'D1awNzlohgmHVfPw07oeLE2QrVXi4wFKvCeSDinkazvbl')

    print("Showing all new tweets for #programming:")

    # There are different kinds of streams: public stream, user stream, multi-user streams
    # In this example follow #programming tag
    # For more details refer to https://dev.twitter.com/docs/streaming-apis
    stream = tweepy.Stream(auth = auth, listener = l)
