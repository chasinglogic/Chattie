# Chattie
## A simple python bot for Telegram who does things and stuff.

### What is Chattie?
Chattie is a chat bot for telegram that makes is easy to add new commands. You can even add new commands while he's running!

### How does it work?
Chattie will listen for all messages in a given chat (either directly with him or in a chat room which you invite him to) and looks for his name.
Because of the way the Telegram Bot API works his name will include the @ sign as seen at the bottom of chattie.py and will assume that whatever word
comes after his name is the name of the command you want to run. I plan on adding "/" command support later but it's not there now.

### How do I add new commands?
All you have to do is create a new python script in commands/ that has a function called run which takes two arguments and returns a string, the first argument is the
bot itsself and the second is the incoming message object from the [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
package. You can read all about that on their github page. If you need to store information you have two options, you can use file based storage as
you want though that can be a little hacky and makes your command less portable. The second method is to store it in the bots inventory field which
is just a normal pyton dict.

tl;dr: Look at one of the existing commands, you must have a run(bot, incoming_message_object) -> String function.
Chattie will send the -> String to the chat room as a message.

### How do I make my own bot using this?
You can fork Chattie and rename the bot by editing chattie.py and at the bottom changing the constructor such that "@Chattie_Bot"
becomes the name of your bot including the @ symbol. You will need make sure that python, git, and virtualenv are installed, use your
distro's package manager to accomplish this an example using my favorite distro [openSUSE](https://opensuse.org) would be:

```bash
sudo zypper in virtualenv python git
```

After that all you need to do is run the following

```bash
git clone (url for your chattie fork) ~/bot
cd ~/bot
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python chattie.py
```

Add the & sign to the end of the last command if you want to run chattie in the background (for example on a server you won't stay connected to.)

When you add commands Chattie will pick them up when he's asked to perform them while running, this means that you don't need to restart Chattie to add
new commands. However if you edit an existing command Chattie won't reload it until you restart him.

### Why the name Chattie?
I'm an alpha nerd and play Dungeons and Dragons, currently I'm playing a Dwarf Tempest Cleric in 5th edition named Chattie.
I love Chattie and his name so that's how I named the bot.

### Contributing

I love getting contributions, well I haven't gotten any yet but I'm sure that I'll love it!

The only thing I ask that if adding a new command that you include a description of it and how to configure it in the PR
(using a module with it's on README would be da bomb, I'm working on this for my own commands now.) If you have an idea for
a command or how we can add multiple backends to Chattie let me know via a Github Issue! I'd love to use Chattie on other chat services.

Open all PR's against the develop branch thanks!

### License Info

Chattie is distributed under the Apache 2.0 License
