# Chattie

A Python bot framework inspired by Hubot.

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Chattie](#chattie)
    - [How do I make my own bot using this?](#how-do-i-make-my-own-bot-using-this)
    - [Core Concepts](#core-concepts)
        - [Tricks, Commands, and Handlers](#tricks-commands-and-handlers)
            - [An Example Trick:](#an-example-trick)
            - [How do I add new tricks and handlers?](#how-do-i-add-new-tricks-and-handlers)
            - [Persistent storage for tricks and handlers](#persistent-storage-for-tricks-and-handlers)
        - [Connectors](#connectors)
    - [Why the name Chattie?](#why-the-name-chattie)
        - [Contributing](#contributing)
        - [License Info](#license-info)

<!-- markdown-toc end -->


## How do I make my own bot using this?

First install chattie using `pip3 install chattie` you then will have access to
the chattie cli which is used to generate and run bots.

To create a new bot run `chattie new my_bot_name`. This will make a new
directory with the bot name and generate a few files to help you get started!

Chattie comes with 3 connectors at this time and I'm constantly trying to add
more:

- Matrix: https://matrix.org/
  - `pip3 install chattie[matrix]`
- Telegram: https://telegram.org/
  - `pip3 install chattie[telegram]`
- Terminal: A REPL you can use for testing your bot!


From there you can start by adding [tricks](#tricks) and [handlers](#handlers)
to build your own bot!

## Core Concepts

Chattie has 4 core concepts around which it's built:

- Handlers -- Receive all non-command messages in a room
- Tricks -- Things that Chattie bots can do
- Commands -- Trigger words for tricks
- Connectors -- Let Chattie bots talk to different services

### Tricks, Commands, and Handlers

Tricks and handlers are just functions which take two arguments and `**kwargs`,
the current instance of the `chattie.Bot` class and the text of the
incoming message as an array split on spaces. The `**kwargs` argument allows
connectors to send additional meta data. It is not strictly necessary for
functioning tricks or handlers but allows you to specialize your bot for your
preferred backend. For more information on what extra metadata is available see
the documentation for the appropriate Connector.

#### An Example Trick:

```python
# If we recieve the message: "chattie my_new_trick some stuff"
def my_new_trick(bot, msg, **kwargs):
	print(msg) # prints ['my_new_trick', 'some', 'stuff']
	print(bot) # prints info about the currently running bot instance
	return "" # responds to the chat room with whatever string is
			  # returned here
```

Handlers follow the exact same signature however they can optionally
return `None` which will send nothing back to the chat room. This is
useful for things like audit logging or catching inside jokes!

All tricks will automatically be added to Chattie's `help` command and
if the trick has a docstring it will be included in the help output
prettified for the users viewing pleasure.

So Chattie can pick up your new tricks you have to assign them to
commands, the way you do this is to have a global variable named
`commands` in your module that is a dictionary of trigger words to
tricks. For our example above it would look like this:

```python
commands = {
	'my_new_trick': my_new_trick
}
```

What's cool is you can assign multiple commands to the same trick:

```python
commands = {
	'my_new_trick': my_new_trick,
	'new_trick': my_new_trick
}
```

Chattie when initialized will automatically pull this variable in and
add it to it's known commands.

Handlers operate much the same way, but since there is no trigger word
for a handler you simply export an array of the handlers you want to
register in the global variable `handlers`:

```python
handlers = [
	a_new_handler,
	some_other_handler
]
```

Chattie will take care of the rest!

#### How do I add new tricks and handlers?

There are two ways to write new tricks and handlers, if you think your
tricks or handlers will be useful to a wider audience then you can
either submit them as a PR to this repo **or** you can create a Python
package using setuptools and entry_points. If you're unsure of what
that means you can
go [here](http://setuptools.readthedocs.io/en/latest/setuptools.html)
for an explanation of setuptools and entry\_points or look in
the
[examples directory](https://github.com/chasinglogic/Chattie/tree/master/examples) where
I have a few example packages setup for you to reference.

Additionally when you create a bot using `chattie new bot_name` there
will be two Python modules created for you named tricks, and
handlers. You can write any tricks or handlers that are local to your
bot in these modules and as long as they are exported as described
above Chattie will pick those up when that bot is running.

#### Persistent storage for tricks and handlers

The final concern you may have is how to maintain some state on your bot? For
example registered rooms for a given handler, to make this simple Chattie has an
"inventory". The inventory is an object that implements the `Inventory`
interface. This simply is `get(key)` which returns the value at `key` and
`set(key, value)` which sets `key` to `value`. The default inventory is a JSON
file backed inventory so it should work anywhere you run Chattie. More complex
Inventories are available if you have a need and as always using `entry_points`
can write and package your own. An example of inventory usage would be this
handler:

```python
def arch_linux_counter(bot, msg, **kwargs):
	text = ' '.join(msg)
	if 'arch' in msg.lower() and 'linux' in msg.lower():
		counter = bot.inventory.get('arch_linux_counter')
		counter += 1
		bot.inventory.set('arch_linux_counter', counter)
		# Send a congratulatory message for extolling the virtues of
		# the Arch Linux Master Race!
		return "Congratulations on talking about Arch Linux! This is"
			" the %dth time it's been talked about around this bot!" % counter
	# Don't send a message
	return None

handlers = [
	arch_linux_counter
]
```

### Connectors

The final concept used in Chattie is that of the Connector. A
Connector is a class which implements the Connector interface that allows
Chattie to connect to a given backend. Often this is a chat service but can
also be any text stream such as stdin/stdout or even Twitter!

The Connector class definition varies wildly based on the backend it's
connecting to but the interface it must implement is:

```python
class Connector:
    """The base interface that must be implemented by a backend."""

	def __init__(self, bot):
		"""Bot is an instance of the Bot class"""
		self.bot = bot

	def listen(self):
		"""Should connect and listen to incoming messages from the backend service.

		When an incoming message is parsed should send the text of the message
        to self.bot.parse_message (the Bot class' parse_message method)
		"""
		pass
```

For example connectors you can see the included
connectors
[here](https://github.com/chasinglogic/Chattie/tree/master/src/chattie/connectors)

The Connector class must be globally exported from the base import
path of your module.

Just like Tricks and Handlers, Chattie picks up connectors available
using entry\_points, specifically the `chattie.plugins.connectors`
entry point. This means that you can write your own connectors and
distribute them as pypi packages, however if you write a Connector I'd
be very happy to include it in the standard distribution so send me a
Pull Request!

## Why the name Chattie?

It's based on the movie Chappie, whose main character is a robot who
gains emotions and befriends some humans. I thought the pun was worthy.

### Contributing

The basics:

1. Fork it! :fork_and_knife:
2. Create an issue describing what you're working on.
3. Create your feature branch: `git checkout -b my-new-feature`
4. Commit your changes: `git commit -am 'Add some feature'`
5. Push to the branch: `git push origin my-new-feature`
6. :fire: Submit a pull request :D :fire:

All pull requests should go to the develop branch not master. Thanks!

### License Info

Chattie is distributed under the Apache 2.0 License
