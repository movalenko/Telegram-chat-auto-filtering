from telethon.sync import events
import aiohttp
import re



def create_process(client, chat_id, prompt):
   
    async def process(event):
        client = event.client
        command_chat_id = client.command_chat
        key = client.gpt_key


        headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {key}"
                    }


        async def get_completion(content):
            async with aiohttp.ClientSession() as session:
                async with session.post("https://api.openai.com/v1/chat/completions", headers=headers, json={
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": content}]
                }) as resp:

                    response_json = await resp.json()
                    return response_json["choices"][0]['message']["content"]



        message = event.raw_text

        
        content = f"""
                        {prompt}


                        {message}
                        """

        yes_pattern = re.compile(r'^(?i:yes)\.?.*$')
        no_pattern = re.compile(r'^(?i:no)\.?.*$')


        response = await get_completion(content)


        is_yes = yes_pattern.match(response)
        is_no = no_pattern.match(response)



        if is_yes:
            await event.forward_to(command_chat_id)
            print(f"valid answer {message, response}")
        elif is_no:
            print(f"discarded answer {message, response}")
        else:
            print(f"Unable to determine if it's 'yes' or 'no' {message, response}")



    client.processes[chat_id] = process
    return process


async def show(event):
    #pass a client object 
    client = event.client

    #receive all info on client's dialogs
    dialogs = await client.get_dialogs()

    #creating a string message as list of all group names and its id
    chats = [f"{item.name}:{item.id}" for item in dialogs if item.is_group or item.is_channel]
    result = '\n'.join(chats)

    await event.respond( result)
    print("/list command was received") 


async def add(event):

    client = event.client
    command_chat_id = client.command_chat
    control_list = client.control_list


    #get all dialogs as entities
    dialogs = await client.get_dialogs()
    
    #extract  names and ids of groups and channels only
    ids = [abs(item.id) for item in dialogs if item.is_group or item.is_channel]


    #received second part of your /add ******** message as integer
    parts = event.raw_text.split()
    received_id = int(parts[1])


    #extract prompt part
    prompt = ' '.join(parts[2:])
    print(f"prompt is {prompt}")


    if received_id == command_chat_id:
        await event.respond("you MUST NOT add command_chat_id into control list never. It will lead to endless loop")
    elif received_id in control_list:
        await event.respond("Group or channel already in control list")
    elif received_id in ids:

        control_list.add(received_id)
        await event.respond("A group added into control list")
        print(f"This a updated control list - {control_list}")

        #creates new event handler (callback function)
        client.add_event_handler(create_process(client, received_id, prompt), events.NewMessage(chats = received_id))

    else:
        await event.respond("chat id is not in the list of id's of your groups")


async def remove(event):
    client = event.client
    command_chat_id = client.command_chat
    control_list = client.control_list


    if not control_list:
        await event.respond("Control list is empty")
    else:
        received_id = int(event.raw_text.split()[1])

        if received_id in control_list:
            control_list.remove(received_id)
            await event.respond("group was removed from the control list")

            """i hope it works like that. We have some list of created events. We have two similar event handlers 
             but they listen to different chats. If i specify the id of chat in the arg, will library understand? """
            client.remove_event_handler(client.processes[received_id], events.NewMessage(chats = received_id))
            del client.processes[received_id]
        else:
            await event.respond("id you want to remove is not in control list")

#of course we can just display control list by event.repsond(control_list), but we want to add other data like names of these chats
async def control_list(event):
    client = event.client
    command_chat_id = client.command_chat
    control_list = client.control_list

    if not control_list:
        await event.respond("Control list is empty")
    else:
        dialogs = await client.get_dialogs()
        groups = {item.name: abs(item.id) for item in dialogs if item.is_group or item.is_channel}
        # Filter the groups dictionary based on the control_list
        filtered_groups = {name: id for name, id in groups.items() if id in control_list}

        # Create the string message in the desired format
        message = "\n".join(f"{name}: {id}" for name, id in filtered_groups.items())
        await event.respond(message)

    print(client.list_event_handlers())