''' HAPTCHA V2: Free for all group chat without account system. '''
''' CLIENT '''

''' Importing required modules '''
import socket as sckt
import tkinter as tk
try:
    import thread as thrd
except:
    import _thread as thrd

''' Defining required constants '''
BYTE_LIMIT = 2048
SERVER_LOCATION = '40.87.45.53'
SERVER_PORT = 12024
READY_COMMAND = '$READY$'
LEAVE_COMMAND = '$LEAVE$'

''' Defining required functions '''
# This function updates the chatbox
def update_chat():
    # Tell server that chatbox is ready
    client_socket.send(READY_COMMAND.encode())
    # Wait for messages from server and display them
    try:
        while True:
            server_message = client_socket.recv(BYTE_LIMIT).decode()
            chat_box.config(state = 'normal')
            chat_box.insert(tk.END, server_message + '\n\n')
            chat_box.see('end')
            chat_box.config(state = 'disabled')
            continue
    except:
        thrd.exit()
    return

# This function sends a message to the server as well as displays it on the chat
def send_msg(event):
    user_message = client_msg_box.get()
    
    # No need to entertain blank message
    if (len(user_message)==0):
        return
    
    # Display user message
    chat_box.config(state = 'normal')
    chat_box.insert(tk.END, 'You:> ' + user_message + '\n\n')
    client_msg_box.delete(0, tk.END)
    chat_box.see('end')
    chat_box.config(state = 'disabled')

    # Send user message
    client_socket.send(user_message.encode())
    return

''' The main program '''
# Creating the socket (IPv4, TCP)
client_socket = sckt.socket(sckt.AF_INET, sckt.SOCK_STREAM)
try:    
    client_socket.connect((SERVER_LOCATION, SERVER_PORT))
except:
    print('Server Unavailable...\nExiting...')
    thrd.exit()

# Getting name from the user and sending to server
user_name = ''
while(len(user_name)==0):
    user_name = input('Enter name for use in chat: ')
    continue

client_socket.send(user_name.encode())

# Setting up chat window
print('Opening chat window...')

# Creating the chat window and its widgets
chat_window = tk.Tk()
chat_window.title('HAPTCHA V2.0')
chat_frame = tk.Frame(master = chat_window, relief = tk.RIDGE, borderwidth = 5)
chat_label = tk.Label(master = chat_frame, text = 'Chat:')
chat_box = tk.Text(master = chat_frame)
client_msg_label = tk.Label(master = chat_frame, text = 'Your Message:')
client_msg_box = tk.Entry(master = chat_frame)

# Packing the widgets into chat window
chat_frame.pack(fill = tk.BOTH, expand = True)
chat_label.pack(fill = tk.BOTH, expand = True)
chat_box.pack(fill = tk.BOTH, expand = True)
chat_box.config(state = 'disabled')
client_msg_label.pack(fill = tk.BOTH, expand = True)
client_msg_box.pack(fill = tk.BOTH, expand = True)

# Starting new thread to update window
chat_update_thread = thrd.start_new_thread(update_chat, ())

# Setting up enter key to send message
client_msg_box.bind('<Return>', send_msg)

# Starting chat window event loop
chat_window.mainloop()

# Cleanup
client_socket.send(LEAVE_COMMAND.encode())
client_socket.close()
print('Closing...')
