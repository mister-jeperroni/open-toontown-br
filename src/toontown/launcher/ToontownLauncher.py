import os
import sys
import time
import types
from otp.launcher.LauncherBase import LauncherBase
from otp.otpbase import OTPLauncherGlobals
from pandac.libpandaexpressModules import *
from toontown.toonbase import TTLocalizer

class ToontownLauncher(LauncherBase):
    GameName = 'Toontown'
    LauncherPhases = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    TmpOverallMap = [15, 16, 17, 18, 19, 20, 21, 21, 22,
                     23, 24, 25, 24]
    RegistryKey = 'Software\\Disney\\Disney Online\\Toontown'
    ForegroundSleepTime = 0.01
    Localizer = TTLocalizer
    VerifyFiles = 1
    DecompressMultifiles = True
    
    def __init__(self):
        if sys.argv[2] == 'Phase2.py':
            sys.argv = sys.argv[:1] + sys.argv[3:]
        
        if ((len(sys.argv) == 5) or (len(sys.argv) == 6)):
            self.gameServer = sys.argv[2]
            self.accountServer = sys.argv[3]
            self.testServerFlag = int(sys.argv[4])
        else:
            print ('Error: Launcher: incorrect number of parameters')
            sys.exit()
        self.toontownBlueKey = 'TOONTOWN_BLUE'
        self.toontownPlayTokenKey = 'TOONTOWN_PLAYTOKEN'
        self.launcherMessageKey = 'LAUNCHER_MESSAGE'
        self.game1DoneKey = 'GAME1_DONE'
        self.game2DoneKey = 'GAME2_DONE'
        self.tutorialCompleteKey = 'TUTORIAL_DONE'
        self.toontownRegistryKey = 'Software\\Disney\\Disney Online\\Toontown'
        if self.testServerFlag:
            self.toontownRegistryKey = '%s%s' % (self.toontownRegistryKey, 'Test')
        self.toontownRegistryKey = '%s%s' % (self.toontownRegistryKey, self.getProductName())
        LauncherBase.__init__(self)
        self.webAcctParams = 'WEB_ACCT_PARAMS'
        self.parseWebAcctParams()
        self.mainLoop()

    def getValue(self, key, default=None):
        try:
            return self.getRegistry(key, default)
        except:
            return self.getRegistry(key)

    def setValue(self, key, value):
        self.setRegistry(key, value)

    def getVerifyFiles(self):
        return 1

    def getTestServerFlag(self):
        return self.testServerFlag

    def getGameServer(self):
        return self.gameServer

    def getLogFileName(self):
        return 'toontown'

    def parseWebAcctParams(self):
        s = config.GetString('fake-web-acct-params', '')
        if not s:
            s = self.getRegistry(self.webAcctParams)
        self.setRegistry(self.webAcctParams, '')
        l = s.split('&')
        length = len(l)
        dict = {}
        for index in range(0, len(l)):
            args = l[index].split('=')
            if len(args) == 3:
                name, value = args[-2:]
                dict[name] = int(value)
            elif len(args) == 2:
                name, value = args
                dict[name] = int(value)

        self.secretNeedsParentPasswordKey = 1                
        if dict.has_key('secretsNeedsParentPassword'):
            self.secretNeedsParentPasswordKey = 1 and dict['secretsNeedsParentPassword']
        else:
            self.notify.warning('no secretNeedsParentPassword token in webAcctParams')
        self.notify.info('secretNeedsParentPassword = %d' % self.secretNeedsParentPasswordKey)

        self.chatEligibleKey = 0
        if dict.has_key('chatEligible'):
            self.chatEligibleKey = 1 and dict['chatEligible']
        else:
            self.notify.warning('no chatEligible token in webAcctParams')
        self.notify.info('chatEligibleKey = %d' % self.chatEligibleKey)

    def getBlue(self):
        blue = self.getValue(self.toontownBlueKey)
        self.setValue(self.toontownBlueKey, '')
        if blue == 'NO BLUE':
            blue = None
        return blue

    def getPlayToken(self):
        playToken = self.getValue(self.toontownPlayTokenKey)
        self.setValue(self.toontownPlayTokenKey, '')
        if playToken == 'NO PLAYTOKEN':
            playToken = None
        return playToken

    def setRegistry(self, name, value):
        if not self.WIN32:
            return
        t = type(value)
        if (t == types.IntType):
            WindowsRegistry.setIntValue(self.toontownRegistryKey, name, value)
        elif (t == types.StringType):
            WindowsRegistry.setStringValue(self.toontownRegistryKey, name, value)
        else:
            self.notify.warning('setRegistry: Invalid type for registry value: ' + repr(value))

    def getRegistry(self, name, missingValue = None):
        self.notify.info('getRegistry%s' % ((name, missingValue),))
        if not self.WIN32:
            if (missingValue == None):
                missingValue = ''
            value = os.environ.get(name, missingValue)
            try:
                value = int(value)
            except:
                pass
            return value
        t = WindowsRegistry.getKeyType(self.toontownRegistryKey, name, WindowsRegistry.RlUser)
        if t == WindowsRegistry.TInt:
            if (missingValue == None):
                missingValue = 0
            return WindowsRegistry.getIntValue(self.toontownRegistryKey, name, 
                                               missingValue, WindowsRegistry.RlUser)
        elif t == WindowsRegistry.TString:
            if missingValue == None:
                missingValue = ''
            return WindowsRegistry.getStringValue(self.toontownRegistryKey, name, 
                                                  missingValue, WindowsRegistry.RlUser)
        else:
            return missingValue
        return

    def getCDDownloadPath(self, origPath, serverFilePath):
        return '%s/%s%s/CD_%d/%s' % (origPath, self.ServerVersion, self.ServerVersionSuffix, self.fromCD, serverFilePath)

    def getDownloadPath(self, origPath, serverFilePath):
        return '%s/%s%s/%s' % (origPath, self.ServerVersion, self.ServerVersionSuffix, serverFilePath)

    def getPercentPatchComplete(self, bytesWritten):
        if self.totalPatchDownload:
            return LauncherBase.getPercentPatchComplete(self, bytesWritten)
        else:
            return 0

    def hashIsValid(self, serverHash, hashStr):
        return serverHash.setFromDec(hashStr) or serverHash.setFromHex(hashStr)

    def launcherMessage(self, msg):
        LauncherBase.launcherMessage(self, msg)
        self.setRegistry(self.launcherMessageKey, msg)

    def getAccountServer(self):
        return self.accountServer

    def setTutorialComplete(self):
        self.setRegistry(self.tutorialCompleteKey, 0)

    def getTutorialComplete(self):
        return self.getRegistry(self.tutorialCompleteKey, 0)

    def getGame2Done(self):
        return self.getRegistry(self.game2DoneKey, 0)

    def setPandaErrorCode(self, code):
        self.pandaErrorCode = code
        if self.WIN32:
            self.notify.info('setting panda error code to %s' % (code))
            exitCode2exitPage = {
                (OTPLauncherGlobals.ExitEnableChat): 'chat',
                (OTPLauncherGlobals.ExitSetParentPassword): 'setparentpassword',
                (OTPLauncherGlobals.ExitPurchase): 'purchase'}
            if code in exitCode2exitPage:
                self.setRegistry('EXIT_PAGE', exitCode2exitPage[code])
                self.setRegistry(self.PandaErrorCodeKey, 0)
            else:
                self.setRegistry(self.PandaErrorCodeKey, code)
        else:
            LauncherBase.setPandaErrorCode(self, code)

    def getNeedPwForSecretKey(self):
        return self.secretNeedsParentPasswordKey

    def getParentPasswordSet(self):
        return self.chatEligibleKey

    def MakeNTFSFilesGlobalWriteable(self, pathToSet = None ):
        if not self.WIN32:
            return
        LauncherBase.MakeNTFSFilesGlobalWriteable(self, pathToSet)

    def startGame(self):
        try:
            os.remove('Phase3.py')
        except: pass
        
        import Phase3
        self.newTaskManager()
        from direct.showbase.EventManagerGlobal import eventMgr
        eventMgr.restart()
        from toontown.toonbase import ToontownStart
