'''
Temp file for testing file handling functions and storing functions not yet implemented. 
Will be deleted once file handling is full implemented. 
'''

global fileBreakChar
fileBreakChar = "`/¬|"

def addNewPlaylist(name, link):
    '''
    adds a new playlist to the playlists.txt file. 
    '''
    try:
        playlistFile = open("playlists.txt", "r")
    except:
        #playlists file does not exist so create the file then re-open it in read mode. 
        playlistFile = open("playlists.txt", "w")
        playlistFile.close()
        playlistFile = open("playlists.txt", "r")
    
    uri = link.split("/")
    uri = uri[len(uri)-1]
    if "?" in uri:
        uri = uri.split("?")[0]

    newLine = name + fileBreakChar + uri + "\n"

    alreadyExists = False
    for line in playlistFile:
        if line == newLine:
            alreadyExists = True
    
    playlistFile.close()
    
    if alreadyExists:
        print("Playlist already exists")
    else:
        playlistFile = open("playlists.txt", "a")
        playlistFile.write(newLine)
        playlistFile.close()   

def removePlaylist(name):
    '''
    removes a playlist from the playlists.txt file. 
    '''
    try:
        playlistFile = open("playlists.txt", "r")
        fileExists = True
    except:
        #file does not exist so do not attempt to delete a playlist
        fileExists =  False

    if fileExists:
        playlistFileContent = []

        for line in playlistFile:
            if line.split(fileBreakChar)[0] != name:
                playlistFileContent.append(line.split(fileBreakChar))
        
        playlistFile.close()

        playlistFile = open("playlists.txt", "w")
        for line in playlistFileContent:
            if line != "\n":
                newLine = line[0] + fileBreakChar + line[1][:-1] + "\n"
                playlistFile.write(newLine)
        
        playlistFile.close()

# added
def getPlaylistIDs():
    '''
    returns a dictionary with key of the playlist name and value of an array of URI and playlist length. 
    this function relies on functions defined in the main spotiShuffler py file.
    '''
    
    try:
        playlistFile = open("playlists.txt", "r")
        playlistIDs = {}
    except:
        #file does not exist so return empty dictionary
        return {}
        
    for line in playlistFile:
        if line != "\n":
            line = line.split(fileBreakChar)
            playlistIDs.update({line[0] : line[1][:-1]})

    playlistFile.close()

    return playlistIDs

# added
def getPlaylistNames():
    '''
    returns an array of strings containing the name of each playlist in the file. 
    '''
    try:
        playlistFile = open("playlists.txt", "r")
    except:
        #file does not exist so return empty array
        return []
    
    playlistNames = []
    for line in playlistFile:
        if line != "\n":
            playlistNames.append(line.split(fileBreakChar)[0])

    return playlistNames

# added
def getURIFromName(playlistName):
    '''
    returns the URI of a playlist as a string from its name
    '''
    playlistFile = open("playlists.txt", "r")

    for line in playlistFile:
        if line != "\n":
            if line == playlistName:
                return line.split(fileBreakChar)[1][:-1]

    playlistFile.close()

    #if execution gets to here, playlist was not found. Return blank string instead. 
    return ""


# Populate playlists.txt with my saved playlists
# addNewPlaylist("Mah Songs", "https://open.spotify.com/playlist/5NAzQpMDTAF7YOZVG3OcEj?si=d24c93975eb74b56")
# addNewPlaylist("Ryans ultimate playlist of absolute zero", "https://open.spotify.com/playlist/5BMLio3vkdkkxdntnr1owH?si=e6011ed49fb446d5")
# addNewPlaylist("Forza Horizon Pulse FH2-4", "https://open.spotify.com/playlist/72OLI4jqcwDjFJ0XWHHSTh?si=9d1ef0250b17489a")
# addNewPlaylist("Bangers and Mash", "https://open.spotify.com/playlist/5aalqdU1aiHnu0Z6SI8R6M?si=1c1381762de442e2")
# addNewPlaylist("white girl music(helldivers2)", "https://open.spotify.com/playlist/55NAlULh1Su7mJNyryfC9d?si=9fe6153c0ac44b9f")
# addNewPlaylist("BANGERS NON_STOP", "https://open.spotify.com/playlist/3kj8qdexDkdH43Qu1YbURe?si=814a9a39a42e49ee")
# addNewPlaylist("ets2", "https://open.spotify.com/playlist/4DFYPrP58uyOFRXo1EqUmi?si=7b3696bdff0f42ec")
# addNewPlaylist("Crusing", "https://open.spotify.com/playlist/1Mv6ID6mj0UUJ3xW6mThtb?si=72ada6c1ced24620")
