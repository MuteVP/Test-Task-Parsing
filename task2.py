import requests
import json
import time
from datetime import datetime

url = 'https://twitter.com/i/api/graphql/25oeBocoJ0NLTbSBegxleg/UserTweets?variables={"userId":"44196397","count":20,"includePromotedContent":true,"withQuickPromoteEligibilityTweetFields":true,"withSuperFollowsUserFields":true,"withDownvotePerspective":false,"withReactionsMetadata":false,"withReactionsPerspective":false,"withSuperFollowsTweetFields":true,"withVoice":true,"withV2Timeline":true}&features={"responsive_web_twitter_blue_verified_badge_is_enabled":true,"verified_phone_label_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true,"unified_cards_ad_metadata_container_dynamic_card_content_query_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_uc_gql_enabled":true,"vibe_api_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":false,"interactive_text_enabled":true,"responsive_web_text_conversations_enabled":false,"responsive_web_enhance_cards_enabled":true}:443'

custom_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.107 Safari/537.36',
    # 'Cookie': 'guest_id_marketing=v1%3A166799958046595041; guest_id_ads=v1%3A166799958046595041; personalization_id="v1_xD4Od+IAXqkfNuF+OqeLEg=="; guest_id=v1%3A166799958046595041; _ga=GA1.2.1191615743.1667999588; ct0=230f61e528d37ee6ef2b7c0661201c93; _gid=GA1.2.221203982.1669010429; gt=1594571584576028674',
    'Host': 'twitter.com',
    'Sec-Ch-Ua': '"Chromium";v="107", "Not=A?Brand";v="24"',
    'X-Twitter-Client-Language': 'ru',
    'X-Csrf-Token': '1902f2505abc70ca9e600daae4378c7c',
    'Sec-Ch-Ua-Mobile': '?0',
    'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
    'Content-Type': 'application/json',
    'X-Guest-Token': '1594713527498919936',
    'X-Twitter-Active-User': 'yes',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Accept': '*/*',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://twitter.com/elonmusk',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
}


def parse_tweets(json_tweets):
    count_tweets = 0
    index = 0
    dictionary_tweets = {}

    while (count_tweets != 10):

        if parsed['data']['user']['result']['timeline_v2']['timeline']['instructions'][1]['entries'][index]['content'][
            'entryType'] == 'TimelineTimelineItem':
            if ('retweeted_status_result' not in
                    parsed['data']['user']['result']['timeline_v2']['timeline']['instructions'][1]['entries'][index][
                        'content']['itemContent']['tweet_results']['result']['legacy']):
                tweet = \
                parsed['data']['user']['result']['timeline_v2']['timeline']['instructions'][1]['entries'][index][
                    'content']['itemContent']['tweet_results']['result']['legacy']['full_text']
                tweet_id = str(
                    parsed['data']['user']['result']['timeline_v2']['timeline']['instructions'][1]['entries'][index][
                        'sortIndex'])

                dictionary_tweets[tweet_id] = tweet

                count_tweets += 1
        index += 1

    return dictionary_tweets


def parsed_comments(dictionary_tweets):
    links = []

    for tweet_id in dictionary_tweets:
        url_detail_tweets = f'https://twitter.com/i/api/graphql/3Vx1KiiOQdrNtgB0kxMRCQ/TweetDetail?variables=%7B%22focalTweetId%22%3A%22{tweet_id}%22%2C%22referrer%22%3A%22profile%22%2C%22with_rux_injections%22%3Afalse%2C%22includePromotedContent%22%3Atrue%2C%22withCommunity%22%3Afalse%2C%22withTweetQuoteCount%22%3Atrue%2C%22withBirdwatchNotes%22%3Afalse%2C%22withSuperFollowsUserFields%22%3Afalse%2C%22withUserResults%22%3Atrue%2C%22withBirdwatchPivots%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Afalse%2C%22withVoice%22%3Atrue%7D'
        r = requests.get(url_detail_tweets, headers=custom_header)
        time.sleep(0.1)

        parsed_feedback = json.loads(r.text)

        i = 0
        count_feedbacks = 0
        while (count_feedbacks != 3):
            if parsed_feedback['data']['threaded_conversation_with_injections']['instructions'][0]['entries'][i][
                'content']['entryType'] == 'TimelineTimelineModule':
                if 'tombstoneInfo' not in \
                        parsed_feedback['data']['threaded_conversation_with_injections']['instructions'][0]['entries'][
                            i]['content']['items'][0]['item']['itemContent']:
                    print(' tweet ', tweet_id, ' in parse...')
                    links.append('https://twitter.com/' + str(
                        parsed_feedback['data']['threaded_conversation_with_injections']['instructions'][0]['entries'][
                            i]['content']['items'][0]['item']['itemContent']['tweet_results']['result']['core'][
                            'user_results']['result']['legacy']['screen_name']))
                    count_feedbacks += 1
            i += 1
        print()
    return links


print(' Start... \n')

response = requests.get(url, headers=custom_header)
parsed = json.loads(response.text)
dict_tweets = parse_tweets(parsed)
feedback_links = parsed_comments(dict_tweets)

result_dict = {}

for tweet_id in dict_tweets:
    tmp_list = []
    for _ in range(3):
        tmp_list.append(feedback_links.pop(0))
    result_dict[dict_tweets[tweet_id]] = tmp_list

number = 1
with open('ten_tweets_of_Elon_Musk.txt', 'w') as f:
    f.write('10 last tweets of Elon Musk on ' + str(datetime.now()) + '\n\n')
    print('10 last tweets of Elon Musk on ' + str(datetime.now()) + '\n\n')
    for key in result_dict:
        f.write(str(number) + '.  ' + key + '\n' + '\nLinks on commentators:\n\n')
        print(str(number) + '.  ' + key + '\n' + '\nLinks on commentators:\n\n')
        for i in range(3):
            f.write(result_dict[key][i] + '\n')
            print(result_dict[key][i] + '\n')
        f.write('---------\n\n')
        print('---------\n\n')
        number += 1

print('Results are duplicated in a file named ten_tweets_of_Elon_Musk.txt')