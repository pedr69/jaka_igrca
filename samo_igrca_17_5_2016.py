import pygame
from math import sin, cos, pi

SIRINA_EKRANA= 800
VISINA_EKRANA= 600

class izstrelek(pygame.sprite.Sprite):
    def __init__(self, polozaj_x, polozaj_y,smer_strela,hitrost_strela,crv_hitrost_x,crv_hitrost_y,ovire=None):
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
        if (self.rect.x > SIRINA_EKRANA) or (self.rect.x < 0):
            self.kill();
        if (self.rect.y > VISINA_EKRANA) or (self.rect.y < -100):
            self.kill();
        #ubije metek ob trku z tlemi
        if self.ovire:
            trki=pygame.sprite.spritecollide(self,self.ovire,False)
            for ovira in trki:
                #work in progress tle je eksplozija
                self.kill();

class osebek(pygame.sprite.Sprite):
    def __init__(self,ovire=None,metki=None):
        super().__init__()
        sirina=40
        visina=40
        zdravje=100;

        self.smer_strela=45
        self.hitrost_strela=0.5
        self.metki=metki;

        self.image=pygame.Surface((sirina,visina),pygame.SRCALPHA)
        self.image.fill((238,90,255))
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
        #smer X
        self.rect.x += self.hitrost_x
        if (self.rect.right > SIRINA_EKRANA):
            self.rect.right = SIRINA_EKRANA;
        if self.rect.x < 0:
            self.rect.x = 0;

        if self.ground and not self.hodim:
            self.hitrost_x = 0;
            
        #smer Y
        if self.hitrost_y<20 and (not self.ground):
            self.hitrost_y+=0.4
        
            
            
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
                
        #za metek
        self.smer_strela +=self.hitrost_vrtenja
        self.smer_strela = self.smer_strela % 360;
        self.hitrost_strela += self.hitrost_hitrosti_strela
    def pojdi_levo(self):
        if self.ground:
            self.desno=False;
            self.hitrost_x = -4;
            self.hodim=True
    def pojdi_desno(self):
        if self.ground:
            self.desno=True;
            self.hitrost_x = 4;
            self.hodim=True;
    def stop(self):        
        self.hodim=False;
        if self.ground:
            self.hitrost_x=0
    def skoci(self):
        if self.ground:
            self.hitrost_y = -10
            self.ground= False;
            if self.hitrost_y < -20:
                self.hitrost_y = -20
    def ustreli(self): #DODELAT
        
        metek=izstrelek(self.rect.right, self.rect.y,self.smer_strela,self.hitrost_strela,self.hitrost_x,self.hitrost_y,self.ovire)
        self.metki.add(metek)
        
class zadeva(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.Surface((SIRINA_EKRANA,VISINA_EKRANA/4))
        self.image.fill((150,150,150))
        self.rect=self.image.get_rect()
        self.rect.x=0
        self.rect.y=3*VISINA_EKRANA/4


def main():
    ekran=pygame.display.set_mode([SIRINA_EKRANA,VISINA_EKRANA])
    pygame.display.set_caption("legendarna igrca")

    ozadje=zadeva()
    skupina=pygame.sprite.Group()
    skupina.add(ozadje)
    metki=pygame.sprite.Group()
    crvi=pygame.sprite.Group()
    crv=osebek(skupina,metki)
    crvi.add(crv)
    ura=pygame.time.Clock()
    konec_zanke=False
    while not konec_zanke:
        ura.tick(60)
        # User input
        for dogodek in pygame.event.get():
            if dogodek.type == pygame.QUIT:
                konec_zanke = True
            elif dogodek.type == pygame.KEYDOWN:
                if dogodek.key == pygame.K_a:
                    crv.pojdi_levo()
                elif dogodek.key == pygame.K_SPACE:
                    crv.ustreli()
                elif dogodek.key == pygame.K_d:                                                  
                    crv.pojdi_desno()
                elif dogodek.key == pygame.K_w:
                    crv.skoci()
                elif dogodek.key == pygame.K_LEFT:
                    crv.hitrost_vrtenja = 1;
                elif dogodek.key == pygame.K_RIGHT:
                    crv.hitrost_vrtenja = -1;
                elif dogodek.key == pygame.K_UP:
                    crv.hitrost_hitrosti_strela = 0.01
                elif dogodek.key == pygame.K_DOWN:
                    crv.hitrost_hitrosti_strela = -0.01
            if dogodek.type == pygame.KEYUP:
                if dogodek.key == pygame.K_a and crv.hitrost_x < 0:
                    crv.stop()
                elif dogodek.key == pygame.K_d and crv.hitrost_x > 0:
                    crv.stop()
                elif dogodek.key == pygame.K_UP or dogodek.key == pygame.K_DOWN: 
                    crv.hitrost_hitrosti_strela = 0
                elif dogodek.key == pygame.K_LEFT or dogodek.key == pygame.K_RIGHT:
                    crv.hitrost_vrtenja = 0
            if dogodek.type == pygame.MOUSEBUTTONDOWN:
                crv.ustreli(); #za debug
    
        # Zganjaj fiziko
        crvi.update()
        skupina.update()
        metki.update()
        # Risanje
        ekran.fill((255,255,255))
        
        skupina.draw(ekran) #narise ozadje
        crvi.draw(ekran) #narise crve
        metki.draw(ekran); #narise metke
        
        pygame.display.flip()
        #debug
        
        print("crv.hitrost_y: "+str(crv.hitrost_y));
        print("crv.hitrost_x: "+str(crv.hitrost_x));
    pygame.quit()
main()
