import time, sys, os, platform, json, csv, logging, requests, threading
from datetime import datetime
from art import text2art
from colorama import init, Fore, Style
from dotenv import load_dotenv

# - - - -  - - - - - - - - - - - - - - - - - - -  - - - - - - - -
init(convert=True) if platform.system() == "Windows" else init()
print(f"{Fore.CYAN}{Style.BRIGHT}{text2art('Created by @ayyitsc9')}\n")
load_dotenv()
# To avoid simultaneous printing from threads
logging.basicConfig(format='%(message)s')
# - - - -  - - - - - - - - - - - - - - - - - - -  - - - - - - - -

lightblue = "\033[94m"
orange = "\033[33m"

class Logger:
    @staticmethod
    def timestamp():
        return str(datetime.now())[:-7]
    @staticmethod
    def normal(message):
        print(f"{lightblue}[{Logger.timestamp()}] {message}")
    @staticmethod
    def other(message):
        print(f"{orange}[{Logger.timestamp()}] {message}")
    @staticmethod
    def error(message):
        print(f"{Fore.RED}[{Logger.timestamp()}] {message}")
    @staticmethod
    def success(message):
        print(f"{Fore.GREEN}[{Logger.timestamp()}] {message}")

# - - - -  - - - - - - - - - - - - - - - - - - -  - - - - - - - -

def get_csv_labels():
    # Open CSV file and return a list containing each value of the first row. Each value is wrapped with curly braces {}
    with open("webhooks.csv", newline='') as input_file:
        csv_file = csv.reader(input_file)
        return [f"{{{label.strip()}}}" for label in next(csv_file)]

def read_csv():
    # Open CSV file and return all of the content in a list (without the first row)
    with open("webhooks.csv", newline='') as input_file:
        csv_file = csv.reader(input_file)
        next(csv_file)
        csv_content = []
        try:
            for row in csv_file:
                csv_content.append(row)
            return csv_content
        except Exception as err:
            Logger.error(f"Error : {err}")

def send_test_webhook(webhook_message):
    # Get test webhook url from env
    TEST_WEBHOOK_URL = os.getenv('TEST_WEBHOOK_URL')
    try:
        # Send webhook message to test webhook
        requests.post(TEST_WEBHOOK_URL, json=webhook_message)
        Logger.success("Successfully sent message to test webhook. Make sure to check it before sending to all webhooks!")
    except Exception as err:
        Logger.error(f"Failed to send test webhook. Error : {err}")
    while True:
        print(Style.RESET_ALL)
        # Verify if user would like to send the message to all of the webhooks in the csv file
        res = input("Send message to all webhooks? (Y/ N) ")
        print("\n")
        if res.lower() == "y" or res.lower() == "yes":
            return True
            break
        elif res.lower() == "n" or res.lower() == "no":
            Logger.other("Successfully cancelled webhook execution!")
            break
        else:
            print("Invalid input. Try again!")

def run(row):
    # Run WebhookSender
    WebhookSender(row)

# - - - -  - - - - - - - - - - - - - - - - - - -  - - - - - - - -

class WebhookSender:
    def __init__(self, row_values):
        self.row_values = row_values
        # Webhook message template
        self.webhook_message = json.load(open("message.json", encoding='utf-8'))
        # Format webhook message
        self.formatted_message = self.format_message()
        # Send formatted webhook
        self.send_webhook()
    
    # 
    def format_message(self):
        def format_value(value):
            # Check if the argument passed in is a string and if { and } are present
            if type(value) is str and "{" in value and "}" in value:
                # Loop through the csv labels. This is the first row of the csv
                for label in csv_labels:
                    # Check if csv label is in value
                    if label in value:
                        # Replace the reference with the coressponding row value in the same index as the csv label that was referenced
                        value = value.replace(label, self.row_values[csv_labels.index(label)])
            return value

        # For better visualization of what is being done here, I recommend viewing multi-level json data.
        # It's also important to understand these data types : str, list, dict
        # I personally visualize a level for each step I have to take to access the keys' value

        # First level, get the keys with a "str" value type
        outer_values_str = list(filter((lambda x: type(self.webhook_message[x]) is str), self.webhook_message))
        # Loop through the first level keys with "str" value type
        for outer_value_str in outer_values_str:
            # Run the value of the key through the format_value function and set its new value to the value returned
            self.webhook_message[outer_value_str] = format_value(self.webhook_message[outer_value_str])
        # Checks if "embeds" is present in the first level
        if 'embeds' in self.webhook_message:
            # Loop through the "embeds" list which are dict (this list is second level)
            for embed_count, embed in enumerate(self.webhook_message['embeds'], 0):
                # Third level, we're now filtering the content inside an individual embed
                # Third level, get the keys with a "str" value type
                embed_outer_values_str = list(filter((lambda x: type(self.webhook_message['embeds'][embed_count][x]) is str), self.webhook_message['embeds'][embed_count]))
                # Third level, get the keys with a dict value type
                embed_outer_values_dict = list(filter((lambda x: type(self.webhook_message['embeds'][embed_count][x]) is dict), self.webhook_message['embeds'][embed_count]))
                # Loop through the third level keys with "str" value type
                for embed_outer_value_str in embed_outer_values_str:
                    # Run the value of the key through the format_value function and set its new value to the value returned
                    self.webhook_message['embeds'][embed_count][embed_outer_value_str] = format_value(self.webhook_message['embeds'][embed_count][embed_outer_value_str])
                # Loop through the third level keys with dict value type
                for embed_inner_value_dict in embed_outer_values_dict:
                    # Loop through the third level keys with "str" value type
                    # There is no check here to see if it is a string. From what I have seen, there can only be str value types in this level
                    for embed_inner_value_str in self.webhook_message['embeds'][embed_count][embed_inner_value_dict]:
                        # Run the value of the key through the format_value function and set its new value to the value returned
                        self.webhook_message['embeds'][embed_count][embed_inner_value_dict][embed_inner_value_str] = format_value(self.webhook_message['embeds'][embed_count][embed_inner_value_dict][embed_inner_value_str])
                # Checks if "fields" is present in the third level ('embeds' > [embed_index] > 'fields')
                if 'fields' in self.webhook_message['embeds'][embed_count]:
                    # Loop through the "fields" list which are dict (this list is fourth level)
                    for field_count, field in enumerate(self.webhook_message['embeds'][embed_count]['fields'], 0):
                        # Fifth level, get the keys with a "str" value type
                        field_inner_values_str = list(filter((lambda x: type(self.webhook_message['embeds'][embed_count]['fields'][field_count][x]) is str), self.webhook_message['embeds'][embed_count]['fields'][field_count]))
                        # Loop through the fifth level keys with "str" value type ('embeds' > [embed_index] > 'fields'> [field_index] > key)
                        for field_inner_value_str in field_inner_values_str:
                            # Run the value of the key through the format_value function and set its new value to the value returned
                            self.webhook_message['embeds'][embed_count]['fields'][field_count][field_inner_value_str] = format_value(self.webhook_message['embeds'][embed_count]['fields'][field_count][field_inner_value_str])
        # Return formatted webhook message. This should have replaced value strings with a {} value referring to data from the csv file. Example : {Name} would be replaced with the rows' unique Name value
        return self.webhook_message

    def send_webhook(self):
        try:
            # Send webhook message to the webhook from self.row_values
            requests.post(self.row_values[csv_labels.index("{Webhook}")], json=self.formatted_message)
            Logger.success("[{}] Successfully sent message to webhook!".format(self.row_values[csv_labels.index("{Name}")]))
        except Exception as err:
            Logger.error(err)
        
# - - - -  - - - - - - - - - - - - - - - - - - -  - - - - - - - -

while True:
    print(Style.RESET_ALL)
    print("What would you like to do?\n")
    print("######################################\n")
    print("[1] Webhook Sender\t\t[2]Exit\n")
    print("######################################\n")
    task = input("Enter Option : ")
    print("\n")
    if task == "1":
        csv_labels = get_csv_labels()
        res = send_test_webhook(json.load(open("message.json", encoding='utf-8')))
        if res:
            csv_content = read_csv()
            threads = []
            try:
                # Loop through csv_content and create/ start a Thread for each row
                for row in csv_content:
                    thread = threading.Thread(target=run, args=(row,))
                    Logger.normal("[{}] Sending webhook message...".format(row[csv_labels.index("{Name}")]))
                    thread.start()
                    threads.append(thread)
                # Wait for all threads to finish
                for x in threads:
                    x.join()
            except Exception as err:
                Logger.error(f"Error occured while running #1 Webhook Sender : {err}")
            Logger.success("Finished Webhook Sender Execution!")
    elif task == "2":
        Logger.other("Comment on my legit check @ https://twitter.com/ayyitsc9")
        Logger.other("Star the repository @ https://github.com/ayyitsc9/mass-discord-webhook-sender")
        Logger.error("Exiting in 5 seconds...")
        time.sleep(5)
        sys.exit()
    else:
        print("Invalid input. Try again!")

# Here is a great resource for visualizing your webhook post before sending it! (Not created by me, credits to the creator)
# https://leovoel.github.io/embed-visualizer/
# Make sure to enable webhook mode if you use the tool above


# Process
# Attempt to send test webhook first, after this ask for verification if they want to send all webhooks
# Format Webhook Data
# Load CSV Headers and Loop through the rest
# Send webhooks (use threading)