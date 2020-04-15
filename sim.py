import math
import matplotlib
matplotlib.use('Qt5Agg')
 
import matplotlib.pyplot as pt
from matplotlib.animation import FuncAnimation
import random
class Pacjent():
    """Klasa reprezentująca pacjenta, może być zdrowy, chory, lub nosicielem, ma swoje współrzędne x,y"""
    
    def __init__(self,czy_zdrowy=True,x=0,y=0):
        if czy_zdrowy:
            self.status = 'zdrowy'
        else:
            self.status = 'chory'
        self.x = x
        self.y = y
    def ruch(self):
        """Metoda losowo zmieniająca położenie pacjenta w zależnosci od statusu"""
        
        if self.status != 'chory':
            zasieg = 1
        else:
            zasieg = 0.1
            
        self.x = self.x + random.uniform(-zasieg,zasieg)
        self.y = self.y + random.uniform(-zasieg,zasieg)
    def __str__(self):
        return "Pacjent     " + self.status + " @ " + str(self.x) + " x " + str(self.y)
class Populacja():
    """Klasa reprezentująca populację n ludzi na obszarze wysokosc x szerokosc"""
    
    def __init__(self, n, wysokosc=100, szerokosc=100):
        self._pacjenci = []
        self._wysokosc = wysokosc
        self._szerokosc = szerokosc
        
        for i in range(n):
            zdrowy = random.choices([True,False],[80,20])[0]
            x = random.uniform(0,szerokosc)
            y = random.uniform(0,wysokosc)
            self._pacjenci.append(Pacjent(zdrowy,x,y))
            
    def __str__(self):
        s = ""
        for p in self._pacjenci:
            s += str(p) + "\n"
        return s
    
    @property
    def wysokosc(self):
        return self._wysokosc
    
    @property
    def szerokosc(self):
        return self._szerokosc
    
    @wysokosc.setter
    def wysokosc(self,y):
        if y<0:
            return ValueError
        else:
            if y < self._wysokosc:
                for p in self._pacjenci:
                    if p.y > y:
                        p.y = y
            self._wysokosc = y
    
    @szerokosc.setter
    def wysokosc(self,x):
        if x<0:
            return ValueError
        else:
            if x < self._szerokosc:
                for p in self._pacjenci:
                    if p.x > x:
                        p.x = x
            self._szerokosc = x
    
    
    def ruch(self):
        """Metoda losowo zmieniająca położenie wszystkich ludzi w populacji"""
        for p in self._pacjenci:
            p.ruch()
            if p.x>self._szerokosc:
                p.x = p.x-self._szerokosc
            if p.x<0:
                p.x = self._szerokosc-p.x
            if p.y>self._wysokosc:
                p.y = p.y-self._wysokosc
            if p.y<0:
                p.y = self._szerokosc-p.y
            if p.status == 'zdrowy':
                czy_blisko = False
                for inny in self._pacjenci:
                    if math.sqrt((inny.x-p.x)**2+(inny.y-p.y)**2)<1 and inny.status != 'zdrowy':
                        czy_blisko = True
                        break
                if czy_blisko == True:
                    p.status = random.choice(['chory','nosiciel'])
                    
    def rysuj(self):
        """Metoda rysuje położenie ludzi na planszy"""
        fig, ax = pt.subplots()
        zdr_xs = [p.x for p in self._pacjenci if p.status=='zdrowy']
        zdr_ys = [p.y for p in self._pacjenci if p.status=='zdrowy']
        ch_xs = [p.x for p in self._pacjenci if p.status=='chory']
        ch_ys = [p.y for p in self._pacjenci if p.status=='chory']
        ax.plot(zdr_xs, zdr_ys, 'go')
        ax.plot(ch_xs, ch_ys, 'ro')

    def animuj(self):
        """Metoda animuje położenie ludzi po upływie czasu"""
        fig, ax = pt.subplots(ncols=2)
        lines = [ax[0].plot([], [], 'go')[0], ax[0].plot([], [], 'ro')[0], 
                 ax[0].plot([], [], 'yo')[0], ax[1].plot([],[],'g-')[0],
                 ax[1].plot([],[],'r-')[0], ax[1].plot([],[],'y-')[0]]
        ax[0].set_xlim(0, self._szerokosc)
        ax[0].set_ylim(0, self._wysokosc)
        ax[1].set_xlim(0, 1000)
        ax[1].set_ylim(0,int(len(self._pacjenci)))
        x, zdrowidata, chorzydata, nosicieledata = [], [], [], []
        def init():
            for line in lines:
                line.set_data([],[])
            return lines
        def update(frame):
            self.ruch()
            xzdrowi = [p.x for p in self._pacjenci if p.status == 'zdrowy']
            yzdrowi = [p.y for p in self._pacjenci if p.status == 'zdrowy']
            xchorzy = [p.x for p in self._pacjenci if p.status == 'chory']
            ychorzy = [p.y for p in self._pacjenci if p.status == 'chory']
            xnosiciele = [p.x for p in self._pacjenci if p.status == 'nosiciel']
            ynosiciele = [p.y for p in self._pacjenci if p.status == 'nosiciel']
            lines[0].set_data(xzdrowi,yzdrowi)
            lines[1].set_data(xchorzy,ychorzy)
            lines[2].set_data(xnosiciele,ynosiciele)
            x.append(frame)
            zdrowidata.append(int(len(xzdrowi)))
            chorzydata.append(int(len(xchorzy)))
            nosicieledata.append(int(len(xnosiciele)))
            lines[3].set_data(x,zdrowidata)
            lines[4].set_data(x,chorzydata)
            lines[5].set_data(x,nosicieledata)
            return lines
        ani = FuncAnimation(fig, update, frames=None, init_func=init, blit=True)       
pop = Populacja(100,100,100)
pop.animuj()
pt.show(block=True)