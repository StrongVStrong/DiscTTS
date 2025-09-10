#Std
import asyncio
import os
import time
from asyncio import Lock

#Ext
import pyautogui
import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()
DISC_BOT = os.getenv("DISC_BOT")

downloads_folder = r"C:\Users\Megas\Downloads"

# TTS dialogue samples
files_to_select = [
    r'"C:\Users\Megas\Documents\Samples\hutao1.wav"',
    r'"C:\Users\Megas\Documents\Samples\hutao2.wav"',
    r'"C:\Users\Megas\Documents\Samples\hutao3.wav"',
    r'"C:\Users\Megas\Documents\Samples\hutao4.wav"'
]

# Selenium setup
driver = webdriver.Chrome()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

#Have GPT-SoVITS running
driver.get("http://localhost:9872/")

# Self setup
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="component-11"]/div[2]/button'))
).click()
time.sleep(1)

pyautogui.typewrite(downloads_folder)
pyautogui.press('enter')
time.sleep(1)

file_paths_to_select = ' '.join(files_to_select)
pyautogui.typewrite(file_paths_to_select)
pyautogui.press('enter')
time.sleep(1)

listbox1 = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="component-19"]/div[2]/div/div[1]/div/input'))
)
listbox1.click()
time.sleep(0.5)

pyautogui.hotkey('ctrl', 'a')
pyautogui.press('backspace')
pyautogui.typewrite("English")
pyautogui.press('enter')
listbox2 = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="component-28"]/div[2]/div/div[1]/div/input'))
)
listbox2.click()
time.sleep(0.5)

pyautogui.hotkey('ctrl', 'a')
pyautogui.press('backspace')
pyautogui.typewrite("English")
pyautogui.press('enter')

def process_input(input_text):
    # Send input
    input_box = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="component-25"]/label/textarea'))
    )
    input_box.clear()
    input_box.send_keys(input_text)

    # Submit input
    submit_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="component-41"]'))
    )
    submit_button.click()
    
    time.sleep(3)

    # Download
    download_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="component-42"]/div[2]/a/button'))
    )
    time.sleep(1)
    while True:
        hide_element = driver.find_element(By.XPATH, '//*[@id="component-42"]/div[1]')
        if "hide" in hide_element.get_attribute("class"):
            # If "hide" is not in the class it's visible, so download available
            break
        else:
            time.sleep(1)
    
    download_button.click()

# Disc bot setup
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Lock for one at a time
download_lock = Lock()

@bot.event
async def on_message(message):
    #Ignore self ofc
    if message.author == bot.user:
        return

    # Listen to channel and user from their IDs below
    target_channel_id = 1248111106480803840
    specific_user_id = 1317303826738319390

    if message.channel.id == target_channel_id and message.author.id == specific_user_id:
        print(f"Received message: {message.content}")
        user_input = message.content
        
        if not user_input.strip():
            return

        async with download_lock:
            recent_wav_file = await process_input(user_input)
            print(f"Downloaded file: {recent_wav_file}")

# Use your bot token
async def start_bot_and_process():
    await bot.start(DISC_BOT)

asyncio.run(start_bot_and_process())
