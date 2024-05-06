import subprocess
import requests
import json
import re

# Discord webhook URL
discord_webhook_url = ""

def send_to_discord(message):
    payload = {"content": message}
    response = requests.post(discord_webhook_url, json=payload)
    if response.status_code != 200:
        print(f"Failed to send message to Discord webhook. Status code: {response.status_code}")
        print(response.text)

def surround_sentence_with_asterisks(text, trigger):
    command_index = text.find(trigger) + len(trigger)
    sentence = text[command_index:].strip()
    return f"**{sentence}**"

# Function to tail -f the log file, filter lines, and send them to Discord
def tail_and_send_log(log_file):
    process = subprocess.Popen(["tail", "-n", "0", "-f", log_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    while True:
        line = process.stdout.readline().strip()
        if "New connection:" in line:
            line = line.replace("Docker Log: {", "{")
            json_data = json.loads(line)
            command = surround_sentence_with_asterisks(json_data['log'], "New connection:")
            string = "New connection:", command
            send_to_discord('|-------------------------------------------------------open-------------------------------------------------------|')
            send_to_discord('@everyone')
            send_to_discord(str(string))
            continue
        if "Command found:" in line:
            line = line.replace("Docker Log: {", "{")
            json_data = json.loads(line)
            command = surround_sentence_with_asterisks(json_data['log'], "Command found:")
            string = "Executed:", command
            continue
            send_to_discord(str(string))
        if "login attempt" in line:
            line = line.replace("Docker Log: {", "{")
            json_data = json.loads(line)
            command = surround_sentence_with_asterisks(json_data['log'], "login attempt")
            string = "Login attempt:", command
            send_to_discord(str(string))
            continue
        if "CMD:" in line:
            line = line.replace("Docker Log: {", "{")
            json_data = json.loads(line)
            command = surround_sentence_with_asterisks(json_data['log'], "CMD:")
            string = "Executed:", command
            send_to_discord(str(string))
            continue
        if "Connection lost after" in line:
            line = line.replace("Docker Log: {", "{")
            json_data = json.loads(line)
            command = surround_sentence_with_asterisks(json_data['log'], "Connection lost after")
            string = "Session took:", command
            send_to_discord(str(string))
            send_to_discord('|-------------------------------------------------------close-------------------------------------------------------|')
            continue
      
# Run main function
if __name__ == "__main__":
    log_file = "/var/snap/docker/common/var-lib-docker/containers/7859c5d2be3524904241af8b3ab45f8f7e54ff63e684034ea696e68a7895884e/7859c5d2be3524904241af8b3ab45f8f7e54ff63e684034ea696e68a7895884e-json.log"
    tail_and_send_log(log_file)
