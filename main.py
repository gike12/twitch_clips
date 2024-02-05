import requests
import datetime
from yt_dlp import YoutubeDL
import config
from pathlib import Path
import os
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
import sys


if __name__ == '__main__':

    range_of_days, min_view, language,game_id= config.parse_arguments()
    today= datetime.datetime.today()
    hour_now=int(today.strftime("%H"))
    clear= lambda: os.system('cls')
    token=config.token
    downloadable= []
    last_found=0
    clips_i=0
    not_aval_clp=0

    url= "https://id.twitch.tv/oauth2/validate"
    headers={
        "Authorization": f"OAuth {token}",
        "Bearer": f"{config.client_id}",}
    
    response = requests.get(url, headers=headers).json()
    if 'status' in response:
        url = "https://id.twitch.tv/oauth2/token"
        headers = {
            "client_id": config.client_id,
            "client_secret": config.client_secret,
            "grant_type": "client_credentials"}
        response2 = requests.post(url, json=headers).json()
        with open("token", "w") as myfile:
            myfile.write(response2['access_token'])


    if 'status' not in response:
        for x in reversed(range(range_of_days)):
            for y in range(24):

                
                dt = today + datetime.timedelta(days=-x)
                ht = y
                dt_edited = datetime.datetime.strftime(dt,'%Y-%m-%d')
                dt_if_24 = datetime.datetime.strftime(dt + datetime.timedelta(days=+1),'%Y-%m-%d') if ht+1 == 24 else datetime.datetime.strftime(dt,'%Y-%m-%d')
                ht_if_24 = "00" if ht+1 == 24 else ht+1 


                url = f"https://api.twitch.tv/helix/clips?game_id={game_id}&first=100&started_at={dt_edited}T{ht}:00:00Z&ended_at={dt_if_24}T{ht_if_24}:00:00Z"
                headers ={
                    "Authorization": f"Bearer {token}",
                    "Client-Id": f"{config.client_id}",}
                response = requests.get(url, headers=headers).json()
               

                for i in response['data']:
                    
                    title = i['title'].replace("?","-").replace(":","-").replace("?","-").replace("*","-").replace('"',"-").replace("\\","-").replace("/","-").replace("?","-").replace("|","-").replace("<","-").replace(">","-").replace("\n",'-')
                    datet = datetime.datetime.strptime(i['created_at'], "%Y-%m-%dT%H:%M:%SZ")
                    filepath = f"clips\\{dt_edited}\\{i['language']}\\[{ht}-00_{ht_if_24}-00]\\{i['broadcaster_name']} - {title}.mp4"
                

                    if not Path(filepath).is_file():
                        if i['view_count'] > min_view:
                            if language.count(i['language']) != 0:
                                downloadable.append({"index": len(downloadable),"url": i['url'],"filepath": filepath})

                clear()
                print(f"day: {dt_if_24} {ht_if_24}:00 found clips: {len(downloadable)-last_found} | Σ: {len(downloadable)}")
                last_found=len(downloadable)
    else:
        print("access token has ben reset run the program again")
        sys.exit()
    
    for clips in downloadable:
        
        try:
            
            ydl_opts = {
                "outtmpl": clips['filepath'],
                "quiet": True,}
            YoutubeDL(ydl_opts).download(clips['url'])
            clips_i+=1
            
            clear()
            print(f"{clips_i} out of {len(downloadable)} | {f"{Fore.YELLOW}Missing Clips:{Fore.RESET} {not_aval_clp} | " if not_aval_clp != 0 else ""}{round(clips_i/len(downloadable)*100,2)}%")
        except Exception as ex:
            if "This clip is no longer available" in str(ex):
                not_aval_clp+= 1
                continue
            else:
                break


    print(f'{Fore.GREEN}DONE{Fore.RESET}')