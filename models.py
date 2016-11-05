import pygame
from math import sin, cos, pi, atan, sqrt
SIRINA_EKRANA= 800
VISINA_EKRANA= 600
GRAVITY=0.4

class Healthbar(pygame.sprite.Sprite):
    def __init__(self,zdravje,polozaj):
        super().__init__()
        self.slika=pygame.image.load("Graphics\healthbar.png")
        self.image=self.slika
        self.rect=self.image.get_rect()

        self.sirina=self.slika.get_width()
        self.visina=self.slika.get_height()
        
        self.rect.top= polozaj.bottom +5
        self.rect.x=polozaj.x/2 + self.rect.x/2 - 5
        
    def update(self,zdravje,polozaj,mrtev):
        if mrtev:
            self.kill()
            return None
            
        self.rect.top= polozaj.bottom +5
        self.rect.x=polozaj.x/2 + self.rect.x/2 - 5

        for i in range(self.sirina - int(zdravje/100 * self.sirina)-2):
             for j in range(self.visina-2):
                 self.image.set_at((i+1,j+1), (0,0,255))

class gej(pygame.sprite.Sprite):
    def __init__(self,polozaj, smer):
        super().__init__()
        self.slika=pygame.image.load("Graphics\puscica.png")
        self.image=self.slika
        self.rect=self.image.get_rect()
        self.rect.center=polozaj
        #self.diag=sqrt((self.rect.height-1)**2+(self.rect.width-1)**2)/4
        #self.diag=sqrt((self.diag**2)/2)
        
    def update(self,x,y,center,smer,mrtev):
        self.image=self.slika
        self.image=pygame.transform.rotate(self.image,smer)
        self.rect=self.image.get_rect(center=center)
        #self.rect.x=x-round(abs(sin(smer/90*pi)*self.diag))
        #self.rect.y=y-round(abs(sin(smer/90*pi)*self.diag))
        if mrtev:
            self.kill()
                   
class izstrelek(pygame.sprite.Sprite):
    def __init__(self, polozaj_x, polozaj_y, smer_strela,
                 hitrost_strela,crv_hitrost_x,crv_hitrost_y,ovire=None):
        super().__init__()
        sirina=6
        visina=6
        self.ovire=ovire

        self.slika=pygame.image.load("Graphics\izstrelek.png")
        self.image=self.slika
        self.rect=self.image.get_rect()

        self.rect.x = polozaj_x
        self.rect.y = polozaj_y

        self.hitrost_x = cos(pi*smer_strela/180)*hitrost_strela*20  + crv_hitrost_x
        self.hitrost_y = sin(pi*smer_strela/180)*hitrost_strela*-20 + crv_hitrost_y

    '''    self.smer=atan(self.hitrost_x/self.hitrost_y)*180/pi
        pygame.transform.rotate(self.image,self.smer)'''

    def update(self):
        #ubije metek ce je izven zaslona
        if (self.rect.x >= SIRINA_EKRANA) or (self.rect.x <= 0):
            self.kill()
        if (self.rect.y >= VISINA_EKRANA) or (self.rect.y <= -100):
            self.kill()
        #ubije metek ob trku z tlemi
        if self.ovire:
            trki=pygame.sprite.spritecollide(self,self.ovire,False)
            for ovira in trki:
                #work in progress tle je eksplozija
                self.kill()
        #smer x
        self.rect.x += self.hitrost_x
            #smer y
        self.hitrost_y += GRAVITY
        self.rect.y += self.hitrost_y

        self.image=self.slika
        if self.hitrost_x > 0:
            self.smer=atan(-self.hitrost_y/self.hitrost_x)*180/pi
        elif self.hitrost_x < 0:
            self.smer=atan(-self.hitrost_y/self.hitrost_x)*180/pi + 180
        elif self.hitrost_x == 0:
            self.smer = -90
        self.image=pygame.transform.rotate(self.image,self.smer)

class osebek(pygame.sprite.Sprite):
    def __init__(self,ovire=None,metki=None,barva=(0, 179, 60)):
        super().__init__()
        sirina=40
        visina=40
        self.zdravje=100

        
        self.mrtev=False
        self.zadnjiskok=True
        self.dokoncnomrtev=False

        self.smer_strela=45
        self.hitrost_strela=0.5
        self.metki=metki

        #self.image=pygame.Surface((sirina,visina),pygame.SRCALPHA)
        #self.image.fill(barva)
        self.image=pygame.image.load("Graphics\crv.png")
        self.rect=self.image.get_rect()
        self.ovire = ovire

        self.izstrelek=pygame.image.load("Graphics\izstrelek.png")
        
        self.hitrost_x=0
        self.hitrost_y=0
        
        self.ground = False
        self.hodim = False
        #za metek
        self.hitrost_vrtenja=0
        self.hitrost_hitrosti_strela=0


        
    def update(self):
        if self.rect.y > VISINA_EKRANA:
            self.kill()
            self.dokoncnomrtev=True
        if self.mrtev and self.zadnjiskok:
            self.hitrost_y= -10
            self.zadnjiskok=False
            
        

        
        if not self.mrtev:
            if self.metki:
                trki = pygame.sprite.spritecollide(self,self.metki,True)
                for metek in trki:
                    self.zdravje -= 5
                if self.zdravje <= 0:
                    self.mrtev=True
            #smer X
            self.rect.x += self.hitrost_x
            if (self.rect.right > SIRINA_EKRANA):
                self.rect.right = SIRINA_EKRANA
            if self.rect.x < 0:
                self.rect.x = 0

            if self.ovire:
                trki=pygame.sprite.spritecollide(self,self.ovire,False)
                for ovira in trki:
                    if self.hitrost_x < 0:
                        self.rect.left = ovira.rect.right
                   #     self.ground = True
                    if self.hitrost_x > 0:
                        self.rect.right = ovira.rect.left
                  #      self.ground = True
                    self.hitrost_x = 0



        if not self.hodim:
            self.hitrost_x = 0
        if 0 == self.hitrost_y:
            self.hitrost_y = 2
        if self.hitrost_y < 20:
            self.hitrost_y += GRAVITY
        self.rect.y += self.hitrost_y

        
        if not self.mrtev:
            if self.ovire:
                trki=pygame.sprite.spritecollide(self,self.ovire,False)
                for ovira in trki:
                    if self.hitrost_y < 0:
                        self.rect.top=ovira.rect.bottom
                    if self.hitrost_y > 0:
                        self.rect.bottom=ovira.rect.top
                        self.ground=True
                    self.hitrost_y=0
                    
            # Preveri ce je na tleh
            self.rect.y += 2
            if self.ovire:
                trki=pygame.sprite.spritecollide(self,self.ovire,False)
                if len(trki):
                    self.ground=True
                else:
                    self.ground=False  
            self.rect.y -= 2
            
            #za metek
            self.smer_strela +=self.hitrost_vrtenja
            self.smer_strela = self.smer_strela % 360
            self.hitrost_strela += self.hitrost_hitrosti_strela
            if self.hitrost_strela>1:
                self.hitrost_strela = 1
            if self.hitrost_strela < 0:
                self.hitrost_strela = 0
    def pojdi_levo(self):
        if not self.mrtev:
            self.desno=False
            self.hitrost_x = -4
            self.hodim=True

    def pojdi_desno(self):
        if not self.mrtev:
            self.desno=True
            self.hitrost_x = 4
            self.hodim=True

    def stop(self):        
        self.hodim=False
        self.hitrost_x=0

    def skoci(self):
        if self.ground and not self.mrtev:
            self.hitrost_y = -10
            self.ground= False
                
    def ustreli(self): #DODELAT
        if not self.mrtev:
            posx = cos(-pi*self.smer_strela/180)*28 + self.rect.x + self.image.get_width() /2 - self.izstrelek.get_width()/2
            posy = sin(-pi*self.smer_strela/180)*28 + self.rect.y + self.image.get_height()/2 - self.izstrelek.get_height()/2

            metek=izstrelek(posx, posy, self.smer_strela,self.hitrost_strela,self.hitrost_x,self.hitrost_y,self.ovire)
            self.metki.add(metek)
        
class zadeva(pygame.sprite.Sprite):
    def __init__(self, x, y, sirina, visina):
        super().__init__()
        self.image=pygame.Surface((sirina, visina))
        self.image.fill((150,150,150))
        self.rect=self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
