from getpass import getpass
from os import system,listdir
from . import get_data

def manualAuth():
    userLogin = input('Username: ')
    userPass = getpass()
    return [userLogin, userPass]

def storeSecret(userLogin, userPass):
    secretFilePath = get_data('secret.gpg')
    print('Please enter your GPG user ID (it usually looks like an email address).')
    gpgID = input('GPG ID: ')
    printfCall = 'printf "%s\n%s" "{}" "{}"'.format(userLogin, userPass.replace('$', '\\$'))
    gpgCall = 'gpg -r {} --encrypt > {}'.format(gpgID,secretFilePath)
    systemCall = ' | '.join([printfCall, gpgCall])
    system(systemCall)
    
def resetSecret():
    dataDirPath = get_data('')
    dataDirContent = listdir(dataDirPath)
    if 'secret.gpg' in dataDirContent:
        system('rm {}'.format(dataDirPath + 'secret.gpg'))
    else:
        print('No secret stored.')

# Retrieving secret
def retrieveSecret():
    secretPipePath = get_data('secret')
    secretFilePath = get_data('secret.gpg')
    system('mkfifo {}'.format(secretPipePath))
    system('gpg --decrypt {} > {} &'.format(secretFilePath,secretPipePath))
    with open(secretPipePath, 'r') as secretPipe:
        secret = [secretData.strip() for secretData in secretPipe.readlines()]
    system('rm {}'.format(secretPipePath))
    return secret

def authModule(autoAuth=False):
    dataDirPath = get_data('')
    dataDirContent = listdir(dataDirPath)
    if autoAuth:
        if not 'secret.gpg' in dataDirContent:
            storeSecret(*manualAuth())
        return retrieveSecret()
    else:
        return manualAuth()
    
    
        
        
    
        