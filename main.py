# coding=UTF-8
import asyncio
import requests
import configparser
import time
import platform
from asyncore import write
from datetime import datetime, timedelta
from dateutil import parser
from discord import Embed
from discord.colour import Color
from discord.ext import tasks
from discord.ext.commands.bot import Bot

if platform.system()=='Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Get the settings from the config file.
CONFIG_FILE = 'bot.config' 
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

# Discord settings
DISCORD_API_TOKEN=config.get('DISCORD','API_TOKEN')
discord_channel_id=int(config.get('DISCORD','CHANNEL_ID'))   

# Contract settings
CONTRACT_ADDRESS=config.get('CONTRACT','ADDRESS')

# Opensea Settings
OS_API_KEY=config.get('OPENSEA','API_KEY')
headers = {'X-API-KEY': OS_API_KEY}

def save_last_run_time(time):
    try:
        with open('lastrun.txt', 'w') as f:
            f.write(str(time))
            print(time)
    except Exception as e:
            print('Bad last run time in lastrun.txt. defaulting last run time to 1 hour ago. ' + str(e))

class MyListingBot(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__('/',*args, **kwargs)
        print('Listing bot started.')

        # start the task
        self.get_listings.start()

    @tasks.loop(seconds=60)
    async def get_listings(self):
        print('Listing activity check started.')
        try:          
            # Last run time
            presentDate = datetime.now()
            unix_timestamp = datetime.timestamp(presentDate) - 3600
            try:            
                with open('lastrun.txt') as f:
                    last_run_temp = f.read().strip()
                    #print(last_run_temp)
                    if(len(last_run_temp) > 0):
                        unix_timestamp = float(last_run_temp)                    
            except Exception as e:
                print('Bad last run time in lastrun.txt. defaulting last run time to 1 hour ago. ' + str(e))
            
            parsed_last_run_time = datetime.fromtimestamp(unix_timestamp).strftime('%Y-%m-%dT%H:%M:%SZ')
            last_listing_timestamp=parsed_last_run_time
            lookup_offset=0
            
            events_url = 'https://api.opensea.io/api/v1/events?only_opensea=false&offset=' + str(lookup_offset) + '&limit=10&asset_contract_address=' + str(CONTRACT_ADDRESS) + '&event_type=created&occurred_after=' + str(last_listing_timestamp)
            #print(events_url)
            events_response = requests.get(events_url, headers=headers)
            json_data = events_response.json()

            # Sort the results
            sorted_event_list = []
            for event_temp in json_data['asset_events']:
                sorted_event_list.insert(0, event_temp)

            for asset_event in sorted_event_list:
                print('Listing event')
                # Get the json data.
                token_id = asset_event.get('asset').get('token_id')
                image_url=asset_event.get('asset').get('image_preview_url')
                asset_name=asset_event.get('asset').get('name')
                starting_price = asset_event.get('starting_price')
                seller_address = asset_event.get('seller').get('address')
                seller_name =  seller_address[0:6]
                if(asset_event.get('seller').get('user') != None):
                   seller_name = asset_event.get('seller').get('user').get('username')

                # format the listing price
                formatted_value='0.0'
                value_temp=str(starting_price)
                if(len(value_temp) > 18):
                    formatted_value = (value_temp[:(len(value_temp) - 18)] + '.' + value_temp[(len(value_temp) - 18):])[:5]
                else:
                    formatted_value = ('0.' + str(value_temp).rjust(18, '0'))[:5]
                formatted_value = formatted_value + ' ⧫'

                # Add 1 second to the last listing timestamp.
                last_listing_timestamp=asset_event.get('created_date')
                parsed_time=parser.parse(last_listing_timestamp)                
                added_seconds = timedelta(0, 1)
                parsed_time = parsed_time + added_seconds
                last_listing_timestamp = (parsed_time.isoformat())[:19] + 'Z'
                
                # Format the discord post.
                embed=Embed(title=asset_name, 
                            type='rich',
                            url='https://opensea.io/assets/' + str(CONTRACT_ADDRESS) + '/' + str(token_id), 
                            color = Color.green(), 
                            description='was just listed for ' + str(formatted_value) + ' \n')
                embed.set_thumbnail(url=image_url)  
                embed.add_field(name='**Seller**', 
                                value='[' + str(seller_name) + '](https://opensea.io/' + str(seller_address) + ')', 
                                inline='true')               
                embed.set_footer(text='Data provided by OpenSea', 
                                icon_url='https://storage.googleapis.com/opensea-static/Logomark/Logomark-Blue.png')

                # Set the channel
                channel = self.get_channel(discord_channel_id)

                # Send the message
                await channel.send(embed=embed)
            
                save_last_run_time(parsed_time.timestamp())                
            print('Listing activity check complete')
        except Exception as e:
            print('Get bot listings failed. ' + str(e))    

    @get_listings.before_loop
    async def before_my_task(self):
        await self.wait_until_ready() # wait until the bot logs in

    @get_listings.after_loop
    async def shutdown(self):
            print('Closing discord connection')      
            time.sleep(1)
            await self.close()  

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

bot = Bot('/')
client = MyListingBot()
client.run(DISCORD_API_TOKEN)
