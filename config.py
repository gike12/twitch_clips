import argparse
import config

min_view=15
game_id=21779 # for lol
language="en" # ['en','es','de','it','fr','da','nl']
range_of_days = 1 # 1d 7d 30d -- only num
client_id =
client_secret=
token=open("token",'r').read()

def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--game_id', type=int, help='Name of the game with twitchs game_id', default=config.game_id)
    parser.add_argument('--min_view', type=int, help='Minimum view count for clips to download', default=config.min_view)
    parser.add_argument('--language', type=str, help='Comma-separated list of languages to download clips from', default=config.language)
    parser.add_argument('--days', type=str, help='How many days does the script scrape only today is 1', default=config.range_of_days)
    

    args = parser.parse_args()

    game_id = args.game_id
    min_view = int(args.min_view)
    language = args.language.split(',')
    range_of_days = int(args.days)

    return range_of_days, min_view, language,game_id

