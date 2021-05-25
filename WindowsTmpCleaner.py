import ctypes, sys
from os import listdir, remove, system, name, getenv
from os.path import isfile, isdir
from shutil import rmtree
from time import sleep

def isUserAdmin():
  try:
    return ctypes.windll.shell32.IsUserAnAdmin()
  except:
    return False


def deletionError(targetFile, targetDir):
  print(f'\n!> Couldn\'t delete "{targetFile}" in "{targetDir}"')


def handleDirCleanup(targetDir):
  dirFiles = listdir(targetDir)
  for i in range(len(dirFiles)):
    targetFile = f'{targetDir}\\{dirFiles[i]}'
    try:
      if isfile(targetFile):
        remove(targetFile)
        if isfile(targetFile):
          deletionError(targetFile, targetDir)
      elif isdir(targetFile):
        rmtree(targetFile)
        if isdir(targetFile):
          deletionError(targetFile, targetDir)
      else:
        raise Exception('\n!> Undefined object exception.')
    except:
      pass


if name == 'nt':
  system('cls')
  if isUserAdmin():
    targetDirs = [
      f'{getenv("LOCALAPPDATA")}\\Temp',
      'C:\\Windows\\Temp',
      'C:\\Windows\\Prefetch',
      'C:\\Windows\\SoftwareDistribution\\Download'
    ]
    for i in range(len(targetDirs)):
      handleDirCleanup(targetDirs[i])
    print('\n> Temp files were cleaned.')
    sleep(2.5)
  else:
    ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, ' '.join(sys.argv), None, 1)
else:
  print('\n!> Not an Windows OS!')
  input('\nPress any key to continue...')
