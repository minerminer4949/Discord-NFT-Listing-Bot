# Discord - NFT Listing Bot  
A discord bot that post NFT listings on OpenSea to a discord channel.  

**__How it works__**  
The bot will call Opensea for any new listings. If new listing are found it will post them to the channel set in bot.config  
Listing will be posted from oldest to newst each run. If there are no new listings nothing is posted.  

**Quick Start**  
1. Download this repo.  
1. Right-click `main.py` -> Send To -> Desktop(create shortcut).  
1. Update the bot.config with your API key, Discord channel and contract address.  
1. Double click the shortcut to run the script.  


# Setup Guide  
## 1. Request an API key from Opensea
[https://docs.opensea.io/reference/request-an-api-key](https://docs.opensea.io/reference/request-an-api-key)  

## 2. Create Your Bot - Discord Setup Guide  
[Discord Bot Setup Guide](https://discordjs.guide/preparations/setting-up-a-bot-application.html#creating-your-bot)  
[Discord Developers Portal](https://discord.com/developers/applications) 

## 3. Discord Server Token  
1. In discord, click the gear icon next to your username  
1. Select Advanced from the left nav menu  
1. Trun on developer mode  
1. Go to the server you want to add the bot to  
1. Click the down arrow next to the Server's name  
1. Select Server Settings -> Widget   
1. Copy the Server ID  
1. Copy the Channel ID  
1. Update setting bot.config file.  

## 4. Download the bot  
[Discord NFT Listing Bot](https://github.com/minerminer4949/Discord-NFT-Listing-Bot/archive/refs/heads/main.zip)

## 5. Update bot.config file  
1. Set the Discord `API_TOKEN`
1. Set the Discord `CHANNEL_ID` where the bot should post listings
1. Set the Contract `ADDRESS`
1. Set the Opensea `API Key`

```
[DISCORD]
API_TOKEN=
CHANNEL_ID=

[CONTRACT]
ADDRESS=0x5aeb2a703323f69b20f397bcb7b38610ec37237b 

[OPENSEA]
API_KEY=
```

## 6. Windows Setup (Python) 
1. [How To Install Python 3 on Windows 10](https://phoenixnap.com/kb/how-to-install-python-3-windows)  
**Required** Add Python Path to Environment Variables  
1. Open the Start menu and start the Run app.  
![image](https://user-images.githubusercontent.com/83915691/154369254-f3dfee3f-baf7-4fd4-ae9d-2f314bdf24a2.png)

1. Type **sysdm.cpl** and click **OK**. This opens the **System Properties** window.
1. Navigate to the **Advanced tab** and select **Environment Variables**.
1. Under **System Variables**, find and select the **Path** variable.
1. Click **Edit**.
1. Select the **Variable value** field. Add the path to the **python.exe** file preceded with a **semicolon (;)**.  
For example, in the image below, we have added "**;C:\Python34.**"  
![image](https://user-images.githubusercontent.com/83915691/154369290-60375fb6-b907-4f7d-ac34-1425332b9b44.png)
1. Click **OK** and close all windows.   

**Command Prompt or Powershell Usage**  
By setting this up, you can execute Python scripts like this:  
`python script.py`

## 7. Starting the bot  
1. Open a command window at the root on the app  
1. Run `python main.py` to start the bot  
1. Crtl+C to stop the bot.  
or
1. Right-click `main.py` -> Send To -> Desktop(create shortcut).   
1. Double click the shortcut to run the script.  



## Linux Setup  
Install pip  
`sudo apt install python3-pip`

Install discord.py  
`python3 -m pip install -U discord.py`

Install discord-py-slash-command.py  
`sudo -H pip3 install -U discord-py-slash-command`

Install python-dateutil.py  
`sudo -H pip3 install python-dateutil`

**Running the bot as a background service**  
Review [Service.MD](https://github.com/minerminer4949/Discord-NFT-Listing-Bot/archive/refs/heads/Service.MD)



