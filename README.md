# Telegram-chat-auto-filtering

Mirror all messages from selected channels to one chat via set of webhooks. Selection is performed using chatgpt API.

# Chat Application README

## Instructions

Follow these steps to set up and use the chat application:

1. **Create an Empty Chat**: Begin by creating an empty chat within your chosen platform. Take note of the assigned chat ID, which must be a positive integer. Save this chat ID in the `config.py` file for future reference.

## Available Commands

Below is a list of commands that can be used within the chat application:

- `/list`: This command retrieves a comprehensive list of all your groups and channels, along with their respective IDs.

- `/add <chat_id> <prompt>`: This command involves three key components: the `/add` keyword, the chat's ID, and the desired prompt. Upon execution, this command establishes a process where a callback function listens to the specified chat using the provided chat ID. The inputted prompt is then applied to incoming messages in the chat.

- `/remove <chat_id>`: To terminate a specific process that is actively monitoring a group or channel with the given chat ID, use this command. The associated callback function will be removed, halting the process.

- `/control_list`: Similar to the `/list` command, this function exclusively returns the names of groups and channels that are presently under monitoring by the library.

## Important Notes

- **/list Command Complexity**: The `/list` command warrants careful consideration due to its intricacy. When designing the prompt for this command, ensure that it prompts the GPT model to generate a response that can be interpreted as either "yes" or "no".

Feel free to reach out for any clarifications or further assistance during the setup process!
