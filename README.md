# mass-discord-webhook-sender
Send a customizable message to multiple webhooks with ease


Installation and Set Up
------------
Click Code > Download ZIP > Extract all files to desktop

- Rename the yourname.env file to env
- Put your test webhook url in the .env file using notepad (not required, this is for seeing your webhook message before actually sending it out to everyone)
- Set up message.json. I have already put a template to go off of but you can use this useful tool for formatting purposes. # https://leovoel.github.io/embed-visualizer/
- Set up webhooks.csv. The "Name" and "Webhook" column is REQUIRED. You can add more columns for extra customizability
- If you do not code, I would recommend just deleting the app.py file and running the app.exe file


Customizability
------------

Other than being able to use unicode emojis, other languages and having full control of how the webhook message looks, you can customize it further by adding more columns to the csv file.

For example, you can add a column for 'Password' and then in your message.json you can reference the value of that column for that specific row by putting {Password}. This is case sensitive so make sure to check capitalization! 

CSV File Example
Name,Webhook,Discount Code,Discount Percent,Password
Group1,WebhookHere,Group1SALE,20,GB1
Group2,Webhook2,Group2SALE,15,GB2

If you set the "content" value in message.json to be "Hello users from {Name}! Check out our website @ https://example.com. Password : {Password}\nYou can use {Discount Code} for a {Discount Percent}% off discount on your next order!"

The content would then be converted to be :
"Hello users from Group1! Check out our website @ https://example.com. Password : GB1\nYou can use Group1SALE for a 20% off discount on your next order!"
for Group1 and
"Hello users from Group2! Check out our website @ https://example.com. Password : GB2\nYou can use Group2SALE for a 15% off discount on your next order!"
for Group2!

Other
-----

- Windows Security or your antivirus may flag the .exe file. This is normal. Just make exception for it to run
- Make sure to test thorougly before running the script for sending to a server you don't have delete message perms for!
- Have any questions? DM me on twitter! I will try to get back to everyone


A Note from Me
-------
You are not required to support me in any way but if you would like to do so I will list ways to below! Thank you everyone for giving my script a try and I hope you found it useful ♥

 If you would like to support me, you can do so by :
- Following me on twitter https://twitter.com/ayyitsc9
- Comment on my legit check https://twitter.com/ayyitsc9/status/996240726286479360
- Spread the word to others who may find it useful
- Cashapp $BloomCord
