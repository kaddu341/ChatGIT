import sys
import os
import configparser


phrase = ''
for i in range(1,len(sys.argv)):
    phrase += sys.argv[i] + ' '

# Get the user's home directory
user_home = os.path.expanduser("~")

# Define the path to the configuration file
config_file_path = os.path.join(user_home, "config.ini")

# Read the API key from the configuration file
config = configparser.ConfigParser()
config.read(config_file_path)
api_key = config.get("API", "api_key")


if(api_key == 'none'):
    print("No ChatGPT API key found. Enter API key:")
    api_key = input("Please enter your API key")

with open(config_file_path, "w") as configfile:
    config.write(configfile)

    
# send "phrase to chatGPT"