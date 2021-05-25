import tkinter as tk
from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from os import remove, sep
from os.path import join, expanduser

# pytube3 is outdated so, in your terminal, copy n paste the commands below.
# pip uninstall pytube pytube3 pytubeX
# pip install git+https://github.com/nficano/pytube

class YoutubeToPc(tk.Frame):
  def __init__(self, master=None):
    super().__init__(master)
    self.master = master
    self.pack()
    self.environmentProps()
    self.usrDownloadPath = join(expanduser('~'), 'Downloads')
    self.tmpVideoFilePath = f'{self.usrDownloadPath}{sep}tmpVidFile.mp4'
    self.tmpAudioFilePath = f'{self.usrDownloadPath}{sep}tmpAudFile.mp4'


  def handleDLToMp4(self):
    try:
      appStatus.set('[1/2] Downloading...')
      root.update()
      getYTVideo = YouTube(ytLink.get())
      composedFilePath = f'{self.usrDownloadPath}{sep}{getYTVideo.title}.mp4'
      getYTVideo.streams.filter(adaptive=True, type='video').first().download(self.usrDownloadPath, filename='tmpVidFile')
      getYTVideo.streams.filter(adaptive=True, type='audio').first().download(self.usrDownloadPath, filename='tmpAudFile')
      tmpVideoFile = VideoFileClip(self.tmpVideoFilePath)
      tmpAudioFile = AudioFileClip(self.tmpAudioFilePath)
      appStatus.set('[2/2] Converting & mounting file...')
      ytLink.set('This step may take some minutes')
      root.update()
      mountClip = tmpVideoFile.set_audio(tmpAudioFile)
      mountClip.write_videofile(composedFilePath, fps=30)
      tmpVideoFile.close()
      tmpAudioFile.close()
      remove(self.tmpVideoFilePath)
      remove(self.tmpAudioFilePath)
      appStatus.set('Done!')
      ytLink.set('Check your "Downloads" directory.')
      root.update()
    except Exception as e:
      print(e)
      appStatus.set('Whoops, something went wrong!')
      ytLink.set(value='Invalid link!')
      root.update()


  def handleDLToMp3(self):
    try:
      appStatus.set('[1/2] Downloading...')
      root.update()
      getYTVideo = YouTube(ytLink.get())
      audioFilePath = f'{self.usrDownloadPath}{sep}{getYTVideo.title}.mp3'
      getYTVideo.streams.first().download(self.usrDownloadPath, filename='tmpAudFile')
      tmpAudioFile = VideoFileClip(self.tmpAudioFilePath)
      appStatus.set('[2/2] Converting & mounting file...')
      ytLink.set('It\'ll finish in a sec.')
      root.update()
      mountAudio = tmpAudioFile.audio.write_audiofile(audioFilePath)
      tmpAudioFile.close()
      remove(self.tmpAudioFilePath)
      appStatus.set('Done!')
      ytLink.set('Check your "Downloads" directory.')
      root.update()
    except Exception as e:
      print(e)
      appStatus.set('Whoops, something went wrong!')
      ytLink.set(value='Invalid link!')
      root.update()


  def environmentProps(self):
    self.formatStatus = tk.Label(self, textvariable=appStatus, font=('helvetica', 10))
    self.formatStatus.pack(pady=3)
    self.formatLinkField = tk.Entry(self, textvariable=ytLink, width=35)
    self.formatLinkField.pack(pady=3)
    self.formatDownMp4Button = tk.Button(self, text='Download .MP4 format', fg='blue', font=('helvetica', 11, 'bold'), command=self.handleDLToMp4)
    self.formatDownMp4Button.pack(pady=3)
    self.formatDownMp3Button = tk.Button(self, text='Download .MP3 format', fg='blue', font=('helvetica', 11, 'bold'), command=self.handleDLToMp3)
    self.formatDownMp3Button.pack(pady=3)
    self.formatQuitButton = tk.Button(self, text='     Exit     ', fg='red', font=('helvetica', 10, 'bold'), command=self.master.destroy)
    self.formatQuitButton.pack(pady=5)
    self.formatInfoLabel = tk.Label(self, text='Made by felpshn', fg='grey', font=('helvetica', 9))
    self.formatInfoLabel.pack(pady=3)


if __name__ == '__main__':
  root = tk.Tk()
  root.title('Youtube 2 PC')
  root.geometry('280x190')
  root.resizable(0, 0)
  appStatus = tk.StringVar()
  appStatus.set('Enter a YouTube link below')
  ytLink = tk.StringVar()
  app = YoutubeToPc(master=root)
  app.mainloop()
