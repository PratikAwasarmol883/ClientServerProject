from tkinter import*
from socket import*
import _thread
#initialize server connection
def initialize_server():
    '''Initialize Socket'''
    s = socket(AF_INET, SOCK_STREAM)
    '''Initiaze Socket'''
    host = 'localhost' #to use betn devices in the same network eg:192.168.1.5
    port=1234 #we can use any port here as we has more than 65000+ port
    
    
    #connect to server
    s.connect((host,port))
    return s

def update_chat(msg,state):
    global chatlog
    chatlog.config(state=NORMAL)
    #update the message in the window
    if state==0:
        chatlog.insert(END,'You: '+msg)
    else:
        chatlog.insert(END,'OTHER: '+msg)
    chatlog.config(state=DISABLED)
    #to show the latest messages
    chatlog.yview(END)



def send():
    global textbox
    #get the message
    msg=textbox.get("0.0",END)
    
    #update the chatlog
    update_chat(msg,0)
    
    #send a message
    s.send(msg.encode('ascii'))
    textbox.delete("0.0",END)


#function to send message

def recieve():
    while 1:
        try:
            data = s.recv(1024)
            msg = data.decode('ascii')
            if msg != "":
                update_chat(msg,1)
        except:
            pass




def GUI():
    global chatlog
    global textbox
    '''Initialize Tkinter Object'''
    gui=Tk()
    
    '''Must have title Window.'''
    gui.title(" Client Chat ")
    
    '''It Must Have Geometry.ie. Proper Size.'''
    gui.geometry("380x430")
    

    '''Text Space To Display Message.'''
    chatlog = Text(gui, bg='white' ,width='50' ,height='8')#We have used gui because we want that chatlog to open in gui window
    chatlog.config(state=DISABLED)
    '''Chatlog it is Gui widget it will help to display text on the Window and user can Edit it.
    setting Chatlog as Text we will be able to manipulate the chat content, scrolling, or disabling editing'''
    
    '''Button To send Message: '''
    sendButton = Button(gui , bg='orange',fg = 'red',text='SEND',command=send)
    
    '''TextBox To Type Message.'''
    textbox = Text(gui, bg = 'white')
    
    '''Where To place Component on the Axis '''
    chatlog.place(x='6',y='6',height=386,width=370)
    textbox.place(x=6 ,y=401 , height=20 , width=265)
    sendButton.place(x=300, y=401 , height=20 , width=50 )
    
        #create a thread to capture messages continuosly
    _thread.start_new_thread(recieve,())
    
    '''It will not close  the window after 1st Execution. it will keep the window in loop.'''
    gui.mainloop()

if __name__ == "__main__":
    chatbox=textbox=None
    s = initialize_server()
    GUI()