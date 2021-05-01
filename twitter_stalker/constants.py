import advertools as adv
import base64


auth_params = {
    'app_key': '',
    'app_secret': '',
    'oauth_token': '',
    'oauth_token_secret': '',
}

twitter_lang_metadata_filename = 'twitter_stalker/assets/twitter_lang_df.csv'

exclude_columns = ['tweet_entities', 'tweet_geo', 'user_entities',
                   'tweet_coordinates', 'tweet_metadata',
                   'tweet_extended_entities', 'tweet_contributors',
                   'tweet_display_text_range', 'tweet_user', 'tweet_place',
                   'tweet_truncated']

regex_dict = {'Emoji': adv.emoji.EMOJI_RAW,
              'Mentions': adv.regex.MENTION_RAW,
              'Hashtags': adv.regex.HASHTAG_RAW,}

phrase_len_dict = {'Words': 1,
                   '2-word Phrases': 2,
                   '3-word Phrases': 3}

img_base64 = base64.b64encode(open('twitter_stalker/assets/logo.png', 'rb').read()).decode('ascii')
