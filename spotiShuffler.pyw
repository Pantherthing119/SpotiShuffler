import tkinter, spotipy, random, threading, sys, ctypes
import tkinter.messagebox
from tkinter import font, ttk, messagebox
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image, ImageTk

# tkinter setup
MAIN_BG_COLOUR = "#1F1F1F"
MAIN_TEXT_COLOUR = "white"
DROPDOWN_TEXT_COLOUR = "#1F1F1F"
PRESSED_TEXT_COLOUR = "#5DD15B"

window = tkinter.Tk()
window.title("SpotiShuffler")
setGeoInfo = "1000x600" + "+" + str(int(window.winfo_screenwidth()/2) - 500) + "+" + str(int(window.winfo_screenheight()/2) - 350)
window.geometry(setGeoInfo)
window.resizable(False, False)
window.configure(background = MAIN_BG_COLOUR)
icon = Image.open(r"spotify.png")
icon.thumbnail([sys.maxsize, 60], Image.Resampling.LANCZOS)

myappid = 'tkinter.python.test'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
window.iconbitmap(r"SpotiShuffler_Icon.ico")

window.iconphoto(True, ImageTk.PhotoImage(icon))

global FILE_BREAK_CHAR
FILE_BREAK_CHAR = "`|?@"
# use `/¬| as a sequence of charcters to break up the playlist name and the playlist URI in the playlists.txt file. Cannot use standard comma as a seperator as playlists may contain commas in their names. Instead, I have used a random sequence of characters instead as it is very unlikely that this sequence will appear in a playlist name. 

class StatusWindowManager():
    def __init__(self):
        # set up satus window
        self.statusWindow = tkinter.Toplevel(window, background = MAIN_BG_COLOUR)
        self.statusWindow.title("Status Window")
        self.setGeoInfo = "400x300" + "+" + str(int(window.winfo_screenwidth()/2) - 200) + "+" + str(int(window.winfo_screenheight()/2) - 150)
        self.statusWindow.geometry(self.setGeoInfo)
        self.statusWindow.resizable(False, False)
        
        # define frames
        self.gettingLengthsFrame = tkinter.Frame(self.statusWindow, background = MAIN_BG_COLOUR)
        self.fetchingSongsFrame = tkinter.Frame(self.statusWindow, background = MAIN_BG_COLOUR)
        self.addingToQueueFrame = tkinter.Frame(self.statusWindow, background = MAIN_BG_COLOUR)
        
        self.frameManager = FrameManager(self.gettingLengthsFrame)
        
        # format frames
        gettingLengthsLabel = tkinter.Label(self.gettingLengthsFrame, text = "Getting playlist length...", font = font.Font(size=20), bg = MAIN_BG_COLOUR, fg = MAIN_TEXT_COLOUR)
        gettingLengthsLabel.place(relx = .5, rely = .3, anchor = tkinter.CENTER)
        gettingLengthsprogressbar = ttk.Progressbar(self.gettingLengthsFrame, mode="indeterminate")
        gettingLengthsprogressbar.place(relx=.5, rely=.5, anchor = tkinter.CENTER, width=200)
        gettingLengthsprogressbar.start(10)
        
        fetchingSongLabel = tkinter.Label(self.fetchingSongsFrame, text = "Fetching songs...", font = font.Font(size=20), bg = MAIN_BG_COLOUR, fg = MAIN_TEXT_COLOUR)
        fetchingSongLabel.place(relx = .5, rely = .3, anchor = tkinter.CENTER)
        fetchingSongprogressbar = ttk.Progressbar(self.fetchingSongsFrame, mode="indeterminate")
        fetchingSongprogressbar.place(relx=.5, rely=.5, anchor = tkinter.CENTER, width=200)
        fetchingSongprogressbar.start(10)
        
        addingToQueueLabel = tkinter.Label(self.addingToQueueFrame, text = "Adding to queue...", font = font.Font(size=20), bg = MAIN_BG_COLOUR, fg = MAIN_TEXT_COLOUR)
        addingToQueueLabel.place(relx = .5, rely = .3, anchor = tkinter.CENTER)
        addingToQueueprogressbar = ttk.Progressbar(self.addingToQueueFrame, mode="indeterminate")
        addingToQueueprogressbar.place(relx=.5, rely=.5, anchor = tkinter.CENTER, width=200)
        addingToQueueprogressbar.start(10)
        
    def showGettingLengths(self):
        self.frameManager.setPage(self.gettingLengthsFrame)
        
    def showFetchingSongs(self):
        self.frameManager.setPage(self.fetchingSongsFrame)
        
    def showAddingToQueue(self):
        self.frameManager.setPage(self.addingToQueueFrame)
        
    def killStatusWindow(self):
        self.statusWindow.destroy()

class FrameManager():
    def __init__(self, startFrame):
        self.currentFrame = startFrame
        self.currentFrame.pack(expand = True, fill = "both")

    def setPage(self, newFrame):
        self.currentFrame.pack_forget()
        self.currentFrame = newFrame
        self.currentFrame.pack(expand = True, fill = "both")
        


# function to allow addToQueue to be executed using threading
def threadedAddToQueue():
    thread = threading.Thread(target=addToQueue) 
    thread.start()

# code to get the value of the dropdown and use this to add 75 random songs from the selected playlist to the users queue
def addToQueue():
    currentPlaylist = dropdown.get()
    if currentPlaylist == "":
        messagebox.showerror("Warning", "Please choose a playlist.")
    else:
        # spotipy app data
        # username = "ddm9kv6312dcqxu9ijwke2x3j"
        clientID = "42ef47bdf0d342cca3fa7773040df34a"
        clientSecret = "c62e82d279064fab82ab819e8426392c"
        redirect_uri = "https://localhost:8888/callback"

        # initialise spotipy
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=clientID, client_secret=clientSecret, redirect_uri=redirect_uri, scope="user-library-read user-read-playback-state user-modify-playback-state"))

        def threadedGettingLengths():
            thread = threading.Thread(target=statusWindowManager.showGettingLengths) 
            thread.start()
        
        def threadedFetchingSongs():
            thread = threading.Thread(target=statusWindowManager.showFetchingSongs)
            thread.start()
            
        def threadedAddingToQueue():
            thread = threading.Thread(target=statusWindowManager.showAddingToQueue) 
            thread.start()
            
        statusWindowManager = StatusWindowManager()
        

        threadedGettingLengths()

        # format - playlist name : playlist id
        def getPlaylistIDs():
            '''
            returns a dictionary with key of the playlist name and value of an array of URI and playlist length. 
            this function relies on functions defined in the main spotiShuffler py file.
            '''
            
            try:
                playlistFile = open("playlists.txt", "r")
                playlistIDs = {}
            except:
                # file does not exist so return empty dictionary
                return {}
                
            for line in playlistFile:
                if line != "\n":
                    line = line.split(FILE_BREAK_CHAR)
                    playlistIDs.update({line[0] : line[1][:-1]})

            playlistFile.close()

            return playlistIDs

        playlistIDs = getPlaylistIDs()

        track_uris = []

        def get_playlist_length(playlist_id):
            total_tracks = 0
            offset = 0

            while True:
                response = sp.playlist_items(playlist_id, offset=offset, fields='total,items(track.id)')
                total_tracks += len(response['items'])
                offset += len(response['items'])

                # Break the loop if there are no more items to fetch
                if len(response['items']) == 0:
                    break

            return total_tracks
        
        def getURIFromName(playlistName):
            '''
            returns the URI of a playlist as a string from its name
            '''
            playlistFile = open("playlists.txt", "r")

            for line in playlistFile:
                if line != "\n":
                    if line.split(FILE_BREAK_CHAR)[0] == playlistName:
                        return line.split(FILE_BREAK_CHAR)[1][:-1]

            playlistFile.close()

            # if execution gets to here, playlist was not found. Return blank string instead. 
            return ""

        currentPlaylistName = dropdown.get() # string for the name of the selected playlist
        currentPlaylistURI = getURIFromName(currentPlaylistName)
        currentPlaylistLength = get_playlist_length(currentPlaylistURI)


        threadedFetchingSongs()


        # create list of the uri of all tracks in the given playlist
        # need for loop and ofset as playlist_tracks() can only get 100 tracks at a time but can have an ofset of where to start in the playlist
        if currentPlaylistLength > 100:
            ofset = 0
            for ofset in range(0, (currentPlaylistLength//100)):
                ofset *= 100
                offsetTrack_uris = sp.playlist_tracks(playlist_id=playlistIDs.get(currentPlaylist), offset=ofset)["items"]
                for i in range(0,100):
                    try: 
                        new_uri = offsetTrack_uris[i]["track"]["uri"]
                        track_uris.append(new_uri)
                    except Exception:
                        pass

            if currentPlaylistLength%100 != 0: # deal remaining songs after the last mulitple of 100 [e.g., the last 56 songs of a 156 song playlist]
                ofset += 100
                offsetTrack_uris = sp.playlist_tracks(playlist_id=playlistIDs.get(currentPlaylist), offset=ofset)["items"]
                upperRange = currentPlaylistLength%100
                for i in range(0, upperRange):
                    try:
                        new_uri = offsetTrack_uris[i]["track"]["uri"]
                        track_uris.append(new_uri)
                    except Exception:
                        pass
        else: # needed for playlists less than 100 songs
            track_uris = sp.playlist_tracks(playlist_id=playlistIDs.get(currentPlaylist))["items"]
            for i in range(0,currentPlaylistLength):
                try: 
                    new_uri = track_uris[i]["track"]["uri"]
                    track_uris.append(new_uri)
                except Exception:
                    pass

        # shuffles list of uri's ready to be added to queue
        shuffled_uris = track_uris
        random.shuffle(shuffled_uris)
        shuffled_uris = shuffled_uris[0:min(75, currentPlaylistLength)]


        threadedAddingToQueue()


        # add the shuffled playlist to the queue
        for uri in shuffled_uris:
            try:
                sp.add_to_queue(uri)
            except TypeError:
                pass
        
        statusWindowManager.killStatusWindow()
        messagebox.showinfo("Success", "Successfully added shuffled songs from " + currentPlaylist + " to queue")

def sortStrList(strList):
    mappingDict = {}
    for item in strList:
        mappingDict.update({item : item.lower()})
    
    lowerCaseList = []
    for key in mappingDict:
        lowerCaseList.append(mappingDict.get(key))

    lowerCaseList.sort()
    
    sortedList = []
    for item in lowerCaseList:
        for key in mappingDict:
            if item == mappingDict.get(key).lower():
                sortedList.append(key)
                break
    
    return sortedList

def getPlaylistNames():
    '''
    returns an array of strings containing the name of each playlist in the file. 
    '''
    try:
        playlistFile = open("playlists.txt", "r")
    except:
        # file does not exist so return empty array
        return []
    
    playlistNames = []
    for line in playlistFile:
        if line != "\n":
            playlistNames.append(line.split(FILE_BREAK_CHAR)[0])

    return playlistNames

def quit():
    window.destroy()

window.option_add('*TCombobox*Listbox.background', PRESSED_TEXT_COLOUR)
window.option_add('*TCombobox*Listbox.foreground', MAIN_BG_COLOUR)
style = ttk.Style()
style.theme_create('SpotiShuffler', settings = 
                   {'TCombobox':
                    {'configure': 
                     {'selectbackground': PRESSED_TEXT_COLOUR,
                     'fieldbackground': PRESSED_TEXT_COLOUR,
                     'background': MAIN_BG_COLOUR,
                     'selectforeground' : MAIN_BG_COLOUR,
                     'arrowcolor' : MAIN_TEXT_COLOUR}
                    }
                   })
style.theme_use('SpotiShuffler') 

# UI organisation setup
playlistSelectFrame = tkinter.Frame(window, background = MAIN_BG_COLOUR)
playlistManagementFrame = tkinter.Frame(window, background = MAIN_BG_COLOUR)

frameManager = FrameManager(playlistSelectFrame)

# playlist select page UI
welcomeLabel = tkinter.Label(playlistSelectFrame, text = "Welcome to SpotiShuffler", font = font.Font(size=25), bg = MAIN_BG_COLOUR, fg = MAIN_TEXT_COLOUR)
selectionLabel = tkinter.Label(playlistSelectFrame, text = "Please select a playlist", font = font.Font(size=20), bg = MAIN_BG_COLOUR, fg = MAIN_TEXT_COLOUR)
welcomeLabel.place(relx = .5, rely = .15, anchor = tkinter.CENTER)
selectionLabel.place(relx = .5, rely = .3, anchor = tkinter.CENTER)

options = getPlaylistNames()
options = sortStrList(options)

global dropdown
dropdown = ttk.Combobox(playlistSelectFrame, values = options, state = "readonly", width = 32, font = font.Font(size=13), justify = "center", background = MAIN_BG_COLOUR, foreground = DROPDOWN_TEXT_COLOUR)
dropdownSelectButton = tkinter.Button(playlistSelectFrame, text = "Add shuffled songs to queue", command = threadedAddToQueue,font = font.Font(size=15), bg = MAIN_BG_COLOUR, fg = MAIN_TEXT_COLOUR, activebackground = PRESSED_TEXT_COLOUR)
dropdown.place(relx = .5, rely = .4, anchor = tkinter.CENTER)
dropdownSelectButton.place(relx = .5, rely = .5, anchor = tkinter.CENTER)

playlistManagementButton = tkinter.Button(playlistSelectFrame, text = "Manage Playlists", command = lambda: frameManager.setPage(playlistManagementFrame),font = font.Font(size=15), bg = MAIN_BG_COLOUR, fg = MAIN_TEXT_COLOUR, activebackground = PRESSED_TEXT_COLOUR)
playlistManagementButton.place(relx = .5, rely = .65, anchor = tkinter.CENTER)

quitButton = tkinter.Button(playlistSelectFrame, text = "Quit", command = quit,font = font.Font(size=15), bg = MAIN_BG_COLOUR, fg = MAIN_TEXT_COLOUR, activebackground = PRESSED_TEXT_COLOUR)
quitButton.place(relx = .5, rely = .8, anchor = tkinter.CENTER)


def updateDropdown():
    global dropdown
    dropdown.place_forget()
    
    options = getPlaylistNames()
    options = sortStrList(options)
    
    dropdown = ttk.Combobox(playlistSelectFrame, values = options, state = "readonly", width = 32, font = font.Font(size=13), justify = "center", background = MAIN_BG_COLOUR, foreground = DROPDOWN_TEXT_COLOUR)
    dropdown.place(relx = .5, rely = .4, anchor = tkinter.CENTER)

def addNewPlaylist(name, link):
    '''
    adds a new playlist to the playlists.txt file. 
    '''
    try:
        playlistFile = open("playlists.txt", "r")
    except:
        # playlists file does not exist so create the file then re-open it in read mode. 
        playlistFile = open("playlists.txt", "w")
        playlistFile.close()
        playlistFile = open("playlists.txt", "r")
    
    uri = link.split("/")
    uri = uri[len(uri)-1]
    if "?" in uri:
        uri = uri.split("?")[0]

    newLine = name + FILE_BREAK_CHAR + uri + "\n"

    alreadyExists = False
    for line in playlistFile:
        if line == newLine:
            alreadyExists = True
    
    playlistFile.close()
    
    if alreadyExists:
        messagebox.showerror(title = "Error", message = "This playlist already exists. ")
    else:
        playlistFile = open("playlists.txt", "a")
        playlistFile.write(newLine)
        playlistFile.close()

        messagebox.showinfo(title = "Success", message = "Successfully added playlist. ")
        updateDropdown()


def removePlaylist(name):
    '''
    removes a playlist from the playlists.txt file. 
    '''
    try:
        playlistFile = open("playlists.txt", "r")
        fileExists = True
    except:
        # file does not exist so do not attempt to delete a playlist
        messagebox.showerror(title = "Error", message = "Cannot find any saved playlists. Please add a playlist first. ")
        fileExists =  False

    if fileExists:
        playlistFileContent = []

        for line in playlistFile:
            if line.split(FILE_BREAK_CHAR)[0] != name:
                playlistFileContent.append(line.split(FILE_BREAK_CHAR))
        
        playlistFile.close()

        playlistFile = open("playlists.txt", "w")
        for line in playlistFileContent:
            if line != "\n":
                newLine = line[0] + FILE_BREAK_CHAR + line[1][:-1] + "\n"
                playlistFile.write(newLine)
        
        playlistFile.close()
        
        # completed removing a playlist
        messagebox.showinfo(title = "success", message = "Successfully deleted playlist. ")
        updateDropdown()

# Manage playlists UI
# Add and remove playlist functions
def addPlaylistCommand():
    # get name and link from entry objects
    playlistName = newPlaylistNameEntry.get()
    playlistLink = newPlaylistLinkEntry.get()
    
    # validate link
    if "https://open.spotify.com/playlist/" in playlistLink:
        # add playlist
        addNewPlaylist(playlistName, playlistLink)
    else:
        messagebox.showerror(title = "Error", message = "Please enter a valid Spotify playlist link. ")

def removePlaylistCommand():
    # get name from entry objects
    playlistName = removePlaylistNameEntry.get()

    #make sure the playlist can be deleted
    if playlistName in getPlaylistNames():
        # confirm user wants to remove this playlist
        confirmDelete = messagebox.askokcancel(title = "Are you sure?", message = "Are you sure you want to delete this playlist? \nThis action cannot be undone. ")
        
        # remove playlist
        if confirmDelete:
            removePlaylist(playlistName)
    else:
        errorMessage = "Cannot find playlist called " + playlistName
        messagebox.showerror(title = "Error", message = errorMessage)

# title UI and back button
backToPlaylistSelectLabel = tkinter.Button(playlistManagementFrame, text = "Back", command = lambda: frameManager.setPage(playlistSelectFrame),font = font.Font(size=15), bg = MAIN_BG_COLOUR, fg = MAIN_TEXT_COLOUR, activebackground = PRESSED_TEXT_COLOUR)
backToPlaylistSelectLabel.place(relx = 0.05, rely = 0.05, anchor = tkinter.CENTER)

playlistManagerLabel = tkinter.Label(playlistManagementFrame, text = "Manage Playlists", font = font.Font(size=25), bg = MAIN_BG_COLOUR, fg = MAIN_TEXT_COLOUR)
playlistManagerLabel.place(relx = .5, rely = .1, anchor = tkinter.CENTER)

# adding playlist UI
addPlaylistsLabel = tkinter.Label(playlistManagementFrame, text = "Add a new playlist", font = font.Font(size=20), bg = MAIN_BG_COLOUR, fg = MAIN_TEXT_COLOUR)
addPlaylistsLabel2 = tkinter.Label(playlistManagementFrame, text = "To add a new playlist, please enter the name of the playlist and the spotify link to the playlist:", font = font.Font(size=16), bg = MAIN_BG_COLOUR, fg = MAIN_TEXT_COLOUR)
newPlaylistNameLabel = tkinter.Label(playlistManagementFrame, text = "Playlist name: ", font = font.Font(size=14), bg = MAIN_BG_COLOUR, fg = MAIN_TEXT_COLOUR)
newPlaylistNameEntry = tkinter.Entry(playlistManagementFrame, justify = "center", font = font.Font(size = 12, weight = "normal"), width = 25, bg = PRESSED_TEXT_COLOUR, fg = "black")
newPlaylistLinkLabel = tkinter.Label(playlistManagementFrame, text = "Playlist link: ", font = font.Font(size=14), bg = MAIN_BG_COLOUR, fg = MAIN_TEXT_COLOUR)
newPlaylistLinkEntry = tkinter.Entry(playlistManagementFrame, justify = "center", font = font.Font(size = 12, weight = "normal"), width = 25, bg = PRESSED_TEXT_COLOUR, fg = "black")
addPlaylistButton = tkinter.Button(playlistManagementFrame, text = "Add Playlist", command = addPlaylistCommand,font = font.Font(size=15), bg = MAIN_BG_COLOUR, fg = MAIN_TEXT_COLOUR, activebackground = PRESSED_TEXT_COLOUR)
addPlaylistsLabel.place(relx = 0.5, rely = 0.2, anchor = tkinter.CENTER)
addPlaylistsLabel2.place(relx = 0.5, rely = 0.27, anchor = tkinter.CENTER)
newPlaylistNameLabel.place(relx = 0.35, rely = 0.33, anchor = tkinter.CENTER)
newPlaylistNameEntry.place(relx = 0.35, rely = 0.38, anchor = tkinter.CENTER, relheight = 0.045)
newPlaylistLinkLabel.place(relx = 0.65, rely = 0.33, anchor = tkinter.CENTER)
newPlaylistLinkEntry.place(relx = 0.65, rely = 0.38, anchor = tkinter.CENTER, relheight = 0.045)
addPlaylistButton.place(relx = 0.5, rely = 0.47, anchor = tkinter.CENTER)

# removing playlist UI
removePlaylistLabel = tkinter.Label(playlistManagementFrame, text = "Remove an existing playlist", font = font.Font(size=20), bg = MAIN_BG_COLOUR, fg = MAIN_TEXT_COLOUR)
removePlaylistLabel2 = tkinter.Label(playlistManagementFrame, text = "To remove an existing playlist, please enter the name of the playlist:", font = font.Font(size=16), bg = MAIN_BG_COLOUR, fg = MAIN_TEXT_COLOUR)
removePlaylistNameLabel = tkinter.Label(playlistManagementFrame, text = "Playlist name: ", font = font.Font(size=14), bg = MAIN_BG_COLOUR, fg = MAIN_TEXT_COLOUR)
removePlaylistNameEntry = tkinter.Entry(playlistManagementFrame, justify = "center", font = font.Font(size = 12, weight = "normal"), width = 25, bg = PRESSED_TEXT_COLOUR, fg = "black")
removePlaylistButton = tkinter.Button(playlistManagementFrame, text = "Remove Playlist", command = removePlaylistCommand,font = font.Font(size=15), bg = MAIN_BG_COLOUR, fg = MAIN_TEXT_COLOUR, activebackground = PRESSED_TEXT_COLOUR)
removePlaylistLabel.place(relx = 0.5, rely = 0.6, anchor = tkinter.CENTER)
removePlaylistLabel2.place(relx = 0.5, rely = 0.67, anchor = tkinter.CENTER)
removePlaylistNameLabel.place(relx = 0.5, rely = 0.73, anchor = tkinter.CENTER)
removePlaylistNameEntry.place(relx = 0.5, rely = 0.78, anchor = tkinter.CENTER, relheight = 0.045)
removePlaylistButton.place(relx = 0.5, rely = 0.87, anchor = tkinter.CENTER)

frameManager.setPage(playlistSelectFrame)

window.mainloop()
