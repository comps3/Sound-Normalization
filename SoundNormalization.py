"""
Name: Brian Huynh
Date: 2/11/15
Title: SoundCompress.py
Abstract: The programs accepts WAV or AIF files and performs dynamic range
compression. In essence, it takes the loud sounds of a song and makes it
softer. It also takes softer sounds in the song and increases it volume.

Ideally this program should be used for media files that are 10 seconds
or longer to absorb the effect.

Usage:
File picker window appears to allow users to pick a WAV file. Another
file picker window appears to allow users to name their new WAV file and
the location where the file should be saved.  Once the media player launches,
the user should click on 'Rec Start' button and it will start to record the
compressed media. Once the song is over, the WAV file will be saved in the
location the user specified.

Two files were included in the ZIP to test the program.

Libraries used:
Pyo: http://ajaxsoundstudio.com/software/pyo/
wxPython: http://wxpython.org/
"""

from pyo import *
import wx
import sys

# Buffer size set to 512 bytes to enable smooth audio playback.
mediaServer = Server(buffersize=512).boot()
# Starts up audio callback loop and begin processing
mediaServer.start()

# Launches Operating System file picker and returns the file path of user's selected
def getFilePath():
    app = wx.App(None)
    style = wx.FD_OPEN
    dialog = wx.FileDialog(None, 'Open WAV file', wildcard="All files (*.*)|*.*", style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    else:
        path = None
    dialog.Destroy()
    return path

# Launches Operating System Save File dialog and returns the filename the user
# choose to save it in.
def getSavePath():
	app = wx.App(None)
	saveFileDialog = wx.FileDialog(None, "Save WAV file", "", "","All files (*.*)|*.*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

	if saveFileDialog.ShowModal() == wx.ID_CANCEL:
		return
    # save the current contents in the file
    # this can be done with e.g. wxPython output streams:
    	return saveFileDialog.GetPath()

	if not output_stream.IsOk():
	   wx.LogError("Cannot save current contents in file '%s'."%saveFileDialog.GetPath())
	   return

def compressSong(player, level):
	# Levels of compression effect how effective loud sounds are reduced

	# Low compression: -15
	# Medium compression: -20
	# High compression: -24
	if level == "low":
		compressLevel = -15
	elif level == "medium":
		compressLevel = -20
	elif level == "high":
		compressLevel = -24
	else:
		compressLevel = -24

	"""
	Thres = Theshold
	Threshold reduces level of audio signal if amplitude ever exceeds
	the threshold. The threshold is measured in decibels.

	Ratio determines the amount of decibels above the set threshold.

	Risetime is the time it takes the sound file to reach upper amplitude value.

	Falltime is the time it takes the sound file to reach lower amplitude value.

	Knee determines how quickly the compression ratio increases. The knee
	was set to 1  to give the lister time to adjust to the increased
	volume level.

    Tested with two WAV samples

	"""
    # Initializes SfPlayer with a wav file path and sets the player to loop
	compressSong = Compress(player, thresh=compressLevel, ratio=6, risetime=.01, falltime=.2,knee=1).mix(2).out()
	mediaServer.gui(locals())

if sys.argv[1] == "baseline":
    # Takes file path of the user's selected file
    filePath = getFilePath()
    # Initializes player
    mediaPlayer = SfPlayer(filePath, loop=False).out()
    mediaServer.gui(locals())

elif sys.argv[1] == "compress":
    # Takes file path of the user's selected file
    filePath = getFilePath()
    # Allows users to select where the sound file should be saved
    savePath = getSavePath() + "_compressed.wav"
    # Initializes player
    mediaPlayer = SfPlayer(filePath, loop=False)
    # Passes the file path to the player's recording
    mediaServer.recordOptions(dur=10, filename=savePath, fileformat=0, sampletype=0)
    # Performs compression on the song file
    compressSong(mediaPlayer, "medium")
