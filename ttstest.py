import os
import glob
import time
import pyautogui
import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import asyncio
from asyncio import Lock

load_dotenv()

# Discord Bot Token
DISC_BOT = os.getenv("DISC_BOT")

# Path to the Downloads folder
downloads_folder = r"C:\Users\Megas\Downloads"

# List of file paths to select
files_to_select = [
    r'"C:\Users\Megas\Documents\Samples\hutao1.wav"',  # Replace with your actual file paths
    r'"C:\Users\Megas\Documents\Samples\hutao2.wav"',
    r'"C:\Users\Megas\Documents\Samples\hutao3.wav"',
    r'"C:\Users\Megas\Documents\Samples\hutao4.wav"'
]

# Initialize the WebDriver (open the browser only once)
driver = webdriver.Chrome()

# Set up the bot
intents = discord.Intents.default()
intents.message_content = True  # Make sure to enable this intent in your Discord Developer Portal
bot = commands.Bot(command_prefix='!', intents=intents)

# Open the page only once
driver.get("http://localhost:9872/")

# Navigate the WebDriver to the file input section
WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="component-11"]/div[2]/button'))
).click()

# Give time for file explorer to appear and type the Downloads folder path
time.sleep(1)
pyautogui.typewrite(downloads_folder)
pyautogui.press('enter')

# Wait for file dialog to appear and select files
time.sleep(1)
file_paths_to_select = ' '.join(files_to_select)
pyautogui.typewrite(file_paths_to_select)
pyautogui.press('enter')

# Select "English" in the language dropdowns
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

# Select "English" again in the second dropdown
listbox2 = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="component-28"]/div[2]/div/div[1]/div/input'))
)
listbox2.click()
time.sleep(0.5)
pyautogui.hotkey('ctrl', 'a')
pyautogui.press('backspace')
pyautogui.typewrite("English")
pyautogui.press('enter')

# Function to process input text, enter it in the WebDriver, and download the TTS
def process_input(input_text):
    input_box = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="component-25"]/label/textarea'))
    )
    input_box.clear()
    input_box.send_keys(input_text)

    # Submit the text
    submit_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="component-41"]'))
    )
    submit_button.click()
    
    time.sleep(3)

    # Wait for the download button to appear and click it
    download_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="component-42"]/div[2]/a/button'))
    )
    time.sleep(1)
    # Wait for the div that contains the "hide" class to be hidden or removed
    while True:
        hide_element = driver.find_element(By.XPATH, '//*[@id="component-42"]/div[1]')
        if "hide" in hide_element.get_attribute("class"):
            # If "hide" is not in the class, it's visible, so we can click the download button
            break
        else:
            # Wait for 1 second and check again
            time.sleep(1)
    
    download_button.click()

# Event when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Create a lock to synchronize the file download process
download_lock = Lock()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Specify the channel ID you want to listen to (replace with your channel ID)
    target_channel_id = 1248111106480803840  # Replace with your channel ID
    specific_user_id = 1317303826738319390  # Replace with the user ID you want to listen to

    # Only process messages from the specified user in the target channel
    if message.channel.id == target_channel_id and message.author.id == specific_user_id:
        print(f"Received message: {message.content}")
        user_input = message.content
        
        # Check if the user input is empty
        if not user_input.strip():
            return  # Do nothing if the input is empty

        # Acquire the lock to ensure only one message is processed at a time
        async with download_lock:
            # Process the input (enter text, submit, and download)
            recent_wav_file = await process_input(user_input)

            # Print the downloaded file path for debugging
            print(f"Downloaded file: {recent_wav_file}")

# Start the bot
async def start_bot_and_process():
    await bot.start(DISC_BOT)  # Replace with your bot's token

asyncio.run(start_bot_and_process())
