from pprint import pprint
import urls
from blessed.sequences import Sequence
from blessed.keyboard import Keystroke

class TUI():

    def __init__(self,term,reqVerbs):
        self.term = term
        self.reqVerbs = reqVerbs
        self.leftCol = self.term.width//5
        self.rightCol = (self.term.width//5)*3

    def multiCharInput(self):
        searchQuery = ''
        val = Keystroke('')
        with self.term.cbreak():
            while val.name !='KEY_ENTER':
                val = self.term.inkey()
                if not val.is_sequence:
                   searchQuery+= val
        return searchQuery

    def centr(self,cenStr):
        return self.term.center(cenStr)

    def handleMenuInput(self):
        devices = self.reqVerbs.getRequest(urls.playerURL)
        deviceID = devices['device']['id']

        with self.term.cbreak(),self.term.hidden_cursor():
            choice = self.term.inkey()    

        if  (choice.lower() == 'r'):
            self.reqVerbs.putRequest(urls.resumeURL)
        elif(choice.lower() == 'p'):
            self.reqVerbs.putRequest(urls.pauseURL)
        elif(choice.lower() == 'n'):
            self.reqVerbs.postRequest(urls.nextURL)
        elif(choice.lower() == 'b'):
            self.reqVerbs.postRequest(urls.previousURL)
        elif(choice.lower() == 'v'):
            volume = input('Volume level 0-100: ')
            self.reqVerbs.putRequest(urls.volumeURL,{'volume_percent':volume,'device_id':deviceID})
        elif(choice.lower() == 's'):
            self.searchUI()
        elif(choice.lower() == 'q'):
            exit()

    def handleSearchInput(self):
        with self.term.cbreak(),self.term.hidden_cursor():
            choice = self.term.inkey()   
        if choice.is_sequence:
            pass
        #Artists
        elif  (choice.lower() == 'a'):
            search  = self.multiCharInput()    
            return self.reqVerbs.getRequest(urls.searchURL,{'type':'artist','q':search})
        #Tracks
        elif(choice.lower() == 't'):
            #self.term.move_xy(self.leftCol,15)
            search  = self.multiCharInput()    
            return self.reqVerbs.getRequest(urls.searchURL,{'type':'track','q':search})
        elif(choice.lower() == 'b'):
            return 'B'
        elif(choice.lower() == 'q'):
            exit()

    def printQueryOutput(self,query):
        with self.term.location():
            self.term.move_xy(self.rightCol,0)
            print(self.term.move_x(self.rightCol) +self.term.brown('=========================================='))
            print(self.term.move_x(self.rightCol) +self.term.brown('Search results'))
            print(self.term.move_x(self.rightCol) +self.term.brown('=========================================='))
            for item in query['tracks']['items']:
                song = item['name']
                if len(song) > 30:
                    song = song[:30] + '...'
                artists = '/'.join([artist['name'] for artist in item['artists']])
                if len(artists) > 30:
                    artists = artists[:30] + '...'
                saCombo = self.term.red(song) + ' | ' + self.term.pink(artists) + self.term.normal
                print(self.term.move_x(self.rightCol)+ saCombo)


    def displayUI(self,songInfo):
        songSeq = Sequence(songInfo,self.term)
        print(self.term.clear)
        print(self.term.brown(self.centr('==========================================')))
        print(self.term.pink(self.term.center(songSeq)))
        print(self.term.brown(self.centr('==========================================')))
        print(self.centr(f'{self.term.red_bold}(P){self.term.normal}{self.term.red} pause playback'))
        print(self.centr(f'{self.term.red_bold}(R){self.term.normal}{self.term.red} resume playing'))
        print(self.centr(f'{self.term.red_bold}(N){self.term.normal}{self.term.red} next song '))
        print(self.centr(f'{self.term.red_bold}(B){self.term.normal}{self.term.red} prev song '))
        print(self.centr(f'{self.term.red_bold}(V){self.term.normal}{self.term.red} volume control'))
        print(self.centr(f'{self.term.red_bold}(S){self.term.normal}{self.term.red} search'))
        print(self.centr(f'{self.term.underline_bold_white}Q - quit{self.term.normal}'))
        self.handleMenuInput()


    def searchUI(self):
        print(self.term.clear)
        with self.term.location():
            print(self.term.move_x(self.leftCol) +self.term.brown('=========================================='))
            print(self.term.move_x(self.leftCol) +self.term.brown('Search Menu'))
            print(self.term.move_x(self.leftCol) +self.term.brown('=========================================='))
            print(self.term.move_x(self.leftCol) +f'{self.term.red_bold}(A){self.term.normal}{self.term.red} Search by artist')
            print(self.term.move_x(self.leftCol) +f'{self.term.red_bold}(T){self.term.normal}{self.term.red} Search by track')
            print(self.term.move_x(self.leftCol) +f'{self.term.red_bold}(B){self.term.normal}{self.term.red} Back to main menu')
            print(self.term.move_x(self.leftCol) +f'{self.term.underline_bold_white}Q - quit{self.term.normal}')
        while(True):
            searchQuery = self.handleSearchInput()
            if(searchQuery == 'B'):
                break
            elif searchQuery != None:
                self.printQueryOutput(searchQuery)

