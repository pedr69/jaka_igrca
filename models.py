import pygame
from math import sin, cos, pi
SIRINA_EKRANA= 800
VISINA_EKRANA= 600

class gej(pygame.sprite.Sprite):
    def __init__(self,polozaj, smer):
        super().__init__()
        self.slika=pygame.image.load("puscica.png")
        self.image=self.slika
        self.rect=self.image.get_rect()
        self.rect.center=polozaj
        
        #self.smer_prejsnja=45
    def update(self,polozaj,smer):
       # razlika=smer-self.smer_prejsnja
        self.image=self.slika
        
        self.image=pygame.transform.rotate(self.image,smer)
        self.rect.center=polozaj
       # self.smer_prejsnja=smer
            
class izstrelek(pygame.sprite.Sprite):
    def __init__(self, polozaj_x, polozaj_y, smer_strela,
                 hitrost_strela,crv_hitrost_x,crv_hitrost_y,ovire=None):
        super().__init__()
        sirina=5
        visina=5
        self.ovire=ovire

        self.image=pygame.Surface((sirina,visina),pygame.SRCALPHA)
        self.image.fill((0,0,0))
        self.rect=self.image.get_rect()

        self.rect.x = polozaj_x
        self.rect.y = polozaj_y

        self.hitrost_x = cos(pi*smer_strela/180)*hitrost_strela*20  + crv_hitrost_x
        self.hitrost_y = sin(pi*smer_strela/180)*hitrost_strela*-20 + crv_hitrost_y


    def update(self):
        #smer x
        self.rect.x += self.hitrost_x
            #smer y
        self.hitrost_y += 0.4
        self.rect.y += self.hitrost_y
        #ubije metek ce je izven zaslona
        if (self.rect.x >= SIRINA_EKRANA) or (self.rect.x <= 0):
            self.kill();
        if (self.rect.y >= VISINA_EKRANA) or (self.rect.y <= -100):
            self.kill();
        #ubije metek ob trku z tlemi
        if self.ovire:
            trki=pygame.sprite.spritecollide(self,self.ovire,False)
            for ovira in trki:
                #work in progress tle je eksplozija
                self.kill();

class osebek(pygame.sprite.Sprite):
    def __init__(self,ovire=None,metki=None,barva=(0, 179, 60)):
        super().__init__()
        sirina=40
        visina=40
        self.zdravje=100;
        


        self.smer_strela=45
        self.hitrost_strela=0.5
        self.metki=metki;

        #self.image=pygame.Surface((sirina,visina),pygame.SRCALPHA)
        #self.image.fill(barva)
        self.image=pygame.image.load("crv.png")
        self.rect=self.image.get_rect()
        self.ovire = ovire
    
        self.hitrost_x=0
        self.hitrost_y=0
        
        self.ground = False
        self.hodim = False
        #za metek
        self.hitrost_vrtenja=0
        self.hitrost_hitrosti_strela=0


        
    def update(self):
        if self.metki:
            trki = pygame.sprite.spritecollide(self,self.metki,True)
            for metek in trki:
                self.zdravje -= 0
            if self.zdravje <= 0:
                self.kill();
        #smer X
        self.rect.x += self.hitrost_x
        if (self.rect.right > SIRINA_EKRANA):
            self.rect.right = SIRINA_EKRANA;
        if self.rect.x < 0:
            self.rect.x = 0;

        if self.ovire:
            trki=pygame.sprite.spritecollide(self,self.ovire,False)
            for ovira in trki:
                if self.hitrost_x < 0:
                    self.rect.left = ovira.rect.right
               #     self.ground = True
                if self.hitrost_x > 0:
                    self.rect.right = ovira.rect.left
              #      self.ground = True;
                self.hitrost_x = 0



        if self.ground and not self.hodim:
            self.hitrost_x = 0;
            
        #smer Yd
        if 0 == self.hitrost_y:
            self.hitrost_y = 2
        elif self.hitrost_y < 20:
            self.hitrost_y += 0.4
        old_y = self.rect.y
        
            
            
        self.rect.y += self.hitrost_y
        if self.ovire:
            trki=pygame.sprite.spritecollide(self,self.ovire,False)
            for ovira in trki:
                if self.hitrost_y < 0:
                    self.rect.top=ovira.rect.bottom
                if self.hitrost_y > 0:
                    self.rect.bottom=ovira.rect.top
                    self.ground=True;
                self.hitrost_y=0
        # Preveri ce je na tleh
        self.rect.y += 2
        if self.ovire:
            trki=pygame.sprite.spritecollide(self,self.ovire,False)
            if len(trki):
                self.ground=True;
            else:
                self.ground=False;  
        self.rect.y -= 2
        #za metek
        self.smer_strela +=self.hitrost_vrtenja
        self.smer_strela = self.smer_strela % 360;
        self.hitrost_strela += self.hitrost_hitrosti_strela
        if self.hitrost_strela>1:
            self.hitrost_strela = 1
        if self.hitrost_strela < 0:
            self.hitrost_strela = 0
    def pojdi_levo(self):
        if self.ground:
            self.desno=False;
            self.hitrost_x = -4;
            self.hodim=True

    def pojdi_desno(self):
        if self.ground:
            self.desno=True
            self.hitrost_x = 4
            self.hodim=True

    def stop(self):        
        self.hodim=False;
        if self.ground:
            self.hitrost_x=0

    def skoci(self):

        if self.ground:
            self.hitrost_y = -10
            self.ground= False;
                
    def ustreli(self): #DODELAT
        
        posx = cos(-pi*self.smer_strela/180)*34 + self.rect.x + 20
        posy = sin(-pi*self.smer_strela/180)*34 + self.rect.y + 20

        if self.zdravje > 0:
            metek=izstrelek(posx, posy, self.smer_strela,self.hitrost_strela,self.hitrost_x,self.hitrost_y,self.ovire);
            self.metki.add(metek);
        
class zadeva(pygame.sprite.Sprite):
    def __init__(self, x, y, sirina, visina):
        super().__init__()
        self.image=pygame.Surface((sirina, visina))
        self.image.fill((150,150,150))
        self.rect=self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
