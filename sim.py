import math
import matplotlib
matplotlib.use('Qt5Agg')
 
import matplotlib.pyplot as pt
from matplotlib.animation import FuncAnimation
import random
class Pacjent():
    """Klasa reprezentująca pacjenta, może być zdrowy, chory, lub nosicielem, ma swoje współrzędne x,y"""
    
    def __init__(self,czy_zdrowy=True,x=0,y=0,vx=0,vy=0):
        if czy_zdrowy:
            self.status = 'zdrowy'
        else:
            self.status = 'chory'
        if self.status!= 'zdrowy' and self.status!='chory' and self.status!='nosiciel' and self.status!='zmarly' and  self.status!='odporny':
            raise ValueError
        self.x = x
        self.y = y
        self.predkosc_x = vx
        self.predkosc_y = vy
        self.zakx = -1
        self.zaky = -1
        if self.status == 'chory':
            self.t = 1
        elif self.status == 'nosiciel':
            self.t = 1
        else:
            self.t = 101
    def ruch(self):
        """Metoda losowo zmieniająca położenie pacjenta w zależnosci od statusu"""
        
        if self.status == 'chory':
            zasieg = 0.1
            predkosc_maksymalna = 0.1
        elif self.status == 'zmarly':
            zasieg = 0
            predkosc_maksymalna = 0
        else:
            zasieg = 1
            predkosc_maksymalna = 1
        
        self.t+=1
        
        if self.t == 100:
            if self.status == 'nosiciel':
                self.status = 'odporny'
            elif random.uniform(0,1)<0.04:
                self.status = 'zmarly'
            else:
                self.status = 'odporny'
        
        self.predkosc_x = self.predkosc_x + random.uniform(-zasieg,zasieg)
        self.predkosc_y = self.predkosc_y + random.uniform(-zasieg,zasieg)
        if self.predkosc_x > predkosc_maksymalna:
            self.predkosc_x = predkosc_maksymalna
        if self.predkosc_x < -predkosc_maksymalna:
            self.predkosc_x = -predkosc_maksymalna
        if self.predkosc_y > predkosc_maksymalna:
            self.predkosc_y = predkosc_maksymalna   
        if self.predkosc_y < -predkosc_maksymalna:
            self.predkosc_y = -predkosc_maksymalna
        self.x = self.x + self.predkosc_x
        self.y = self.y + self.predkosc_y
        
        
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
                    if math.sqrt((inny.x-p.x)**2+(inny.y-p.y)**2)<1 and (inny.status == 'chory' or inny.status == 'nosiciel'):
                        czy_blisko = True
                        break
                if czy_blisko == True:
                    p.status = random.choice(['chory','nosiciel'])
                    p.t = 0
                    p.zakx = p.x
                    p.zaky = p.y
                    
    def historia_zarazen(self):
        """Metoda wypisauje miejsca i czas zarażeń"""
        lista = []
        for p in self._pacjenci:
            if p.zakx != -1:
                lista.append([p.zakx, p.zaky, p.t])
        return(lista)
    
    def rysuj(self):
        """Metoda rysuje położenie ludzi na planszy"""
        fig, ax = pt.subplots()
        zdr_xs = [p.x for p in self._pacjenci if p.status=='zdrowy']
        zdr_ys = [p.y for p in self._pacjenci if p.status=='zdrowy']
        ch_xs = [p.x for p in self._pacjenci if p.status=='chory']
        ch_ys = [p.y for p in self._pacjenci if p.status=='chory']
        no_xs = [p.x for p in self._pacjenci if p.status=='nosiciel']
        no_ys = [p.y for p in self._pacjenci if p.status=='nosiciel']
        od_xs = [p.x for p in self._pacjenci if p.status=='odporny']
        od_ys = [p.y for p in self._pacjenci if p.status=='odporny']
        zm_xs = [p.x for p in self._pacjenci if p.status=='zmarly']
        zm_ys = [p.y for p in self._pacjenci if p.status=='zmarly']
        ax.plot(zdr_xs, zdr_ys, 'go')
        ax.plot(ch_xs, ch_ys, 'ro')
        ax.plot(no_xs, no_ys, 'yo')
        ax.plot(od_xs, od_ys, 'bo')
        ax.plot(zm_xs, zm_ys, 'ko')

    def animuj(self):
        """Metoda animuje położenie ludzi po upływie czasu"""
        fig, ax = pt.subplots(1,3, figsize=(20,6))
        oznaczenia = ['zdrowi', 'chorzy', 'nosiciele', 'odporni', 'zmarli']
        kolory = ['green', 'red', 'yellow', 'blue', 'black']
        dane = [100,0,0,0,0]
        lines = [ax[0].plot([], [], 'go')[0], ax[0].plot([], [], 'ro')[0], 
                 ax[0].plot([], [], 'yo')[0], ax[0].plot([], [], 'bo')[0],
                 ax[0].plot([], [], 'ko')[0], ax[1].plot([], [], 'g-')[0],
                 ax[1].plot([], [], 'r-')[0], ax[1].plot([], [], 'y-')[0],
                 ax[1].plot([], [], 'b-')[0], ax[1].plot([], [], 'k-')[0]]
        ax[0].set_xlim(0, self._szerokosc)
        ax[0].set_ylim(0, self._wysokosc)
        ax[1].set_xlim(0, 1000)
        ax[1].set_ylim(0,int(len(self._pacjenci)))
        ax[2].pie([])
        x, zdrowidata, chorzydata, nosicieledata, odpornidata, zmarlidata = [], [], [], [], [], []
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
            xodporni = [p.x for p in self._pacjenci if p.status == 'odporny']
            yodporni = [p.y for p in self._pacjenci if p.status == 'odporny']
            xzmarli = [p.x for p in self._pacjenci if p.status == 'zmarly']
            yzmarli = [p.y for p in self._pacjenci if p.status == 'zmarly']
            lines[0].set_data(xzdrowi,yzdrowi)
            lines[1].set_data(xchorzy,ychorzy)
            lines[2].set_data(xnosiciele,ynosiciele)
            lines[3].set_data(xodporni,yodporni)
            lines[4].set_data(xzmarli,yzmarli)
            x.append(frame)
            zdrowidata.append(int(len(xzdrowi)))
            chorzydata.append(int(len(xchorzy)))
            nosicieledata.append(int(len(xnosiciele)))
            odpornidata.append(int(len(xodporni)))
            zmarlidata.append(int(len(xzmarli)))
            lines[5].set_data(x,zdrowidata)
            lines[6].set_data(x,chorzydata)
            lines[7].set_data(x,nosicieledata)
            lines[8].set_data(x,odpornidata)
            lines[9].set_data(x,zmarlidata)
            dane[0]=int(len(xzdrowi))
            dane[1]=int(len(xchorzy))
            dane[2]=int(len(xnosiciele))
            dane[3]=int(len(xodporni))
            dane[4]=int(len(xzmarli))
            ax[2].clear()
            ax[2].pie(dane, labels = oznaczenia, colors = kolory, autopct='%1.0f%%', labeldistance=50)
            ax[2].legend()
            ax[2].axis('equal')
            xzar = []
            yzar = []
            tzar = []
            for zar in self.historia_zarazen():
                xzar.append(zar[0])
                yzar.append(zar[1])
                tzar.append(5000/(zar[2]**2 + 10))
            return lines + [ax[2], ax[0].scatter(xzar, yzar, c = 'cyan', s = tzar)]
        ani = FuncAnimation(fig, update, frames=None, init_func=init, blit=True) 
pop = Populacja(100,100,100)
pop.animuj()
pt.show(block=True)