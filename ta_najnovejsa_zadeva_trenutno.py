import pygame

SIRINA_EKRANA= 800
VISINA_EKRANA= 600

class izstrelek(pygame.sprite.Sprite):
    def __init__(self, polozaj_x, polozaj_y,ovire=None):
        super().__init__()
        sirina=5
        visina=5

        self.image=pygame.Surface((sirina,visina),pygame.SRCALPHA)
        self.image.fill((0,0,0))
        self.rect=self.image.get_rect()

        self.rect.x = polozaj_x
        self.rect.y = polozaj_y

        self.hitrost_x = 10
        self.hitrost_y = -5

    def update(self):
        self.rect.x += self.hitrost_x
        self.hitrost_y += 0.4
        self.rect.y += self.hitrost_y

class osebek(pygame.sprite.Sprite):
    def __init__(self,ovire=None):
        super().__init__()
        sirina=40
        visina=40
        zdravje=100;

        self.image=pygame.Surface((sirina,visina),pygame.SRCALPHA)
        self.image.fill((238,90,255))
        self.rect=self.image.get_rect()
        self.ovire = ovire
        self.hitrost_x=0
        self.hitrost_y=0
    def update(self):
        #smer X
        self.rect.x += self.hitrost_x
        self.rect.x %= SIRINA_EKRANA
        #smer Y
        if self.hitrost_y<20:
            self.hitrost_y+=0.4
        self.rect.y += self.hitrost_y
        if self.ovire:
            trki=pygame.sprite.spritecollide(self,self.ovire,False)
            for ovira in trki:
                if self.hitrost_y < 0:
                    self.rect.top=ovira.rect.bottom
                if self.hitrost_y > 0:
                    self.rect.bottom=ovira.rect.top
                self.hitrost_y=0

    def pojdi_levo(self):
        self.desno=False;
        self.hitrost_x = -4;
        self.hodim=True
    def pojdi_desno(self):
        self.desno=True;
        self.hitrost_x = 4;
        self.hodim=True;
    def stop(self):
        self.hodim=False;
        self.hitrost_x=0
    def skoci(self):
        self.hitrost_y = -10
        if self.hitrost_y < -20:
            self.hitrost_y = -20
    def ustreli(self): #DODELAT
        
        metek=izstrelek(self.rect.right, self.rect.y)
        self.ovire.add(metek)
        
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
    
    ozadje=zadeva()
    skupina=pygame.sprite.Group()
    skupina.add(ozadje)
    crvi=pygame.sprite.Group()
    crv=osebek(skupina)
    crvi.add(crv)
    ura=pygame.time.Clock()
    konec_zanke=False
    while not konec_zanke:
        ura.tick(60)
        # User input
        for dogodek in pygame.event.get():
            if dogodek.type == pygame.QUIT:
                konec_zanke = True
            elif dogodek.type == pygame.MOUSEBUTTONDOWN:
                crv.ustreli()
            elif dogodek.type == pygame.KEYDOWN:
                if dogodek.key == pygame.K_LEFT:
                    crv.pojdi_levo()
                elif dogodek.key == pygame.K_RIGHT:
                    crv.pojdi_desno()
                elif dogodek.key == pygame.K_UP:
                    crv.skoci()
           #     elif dogodek.key == pygame.MOUSEBUTTON:
            #        crv.ustreli()
            if dogodek.type == pygame.KEYUP:
                if dogodek.key == pygame.K_LEFT and crv.hitrost_x < 0:
                    crv.stop()
                elif dogodek.key == pygame.K_RIGHT and crv.hitrost_x > 0:
                    crv.stop()
        # Zganjaj fiziko
        crvi.update()
        skupina.update()
        # Risanje
        ekran.fill((255,255,255))
        skupina.draw(ekran)
        
        crvi.draw(ekran)
        pygame.display.flip()
    pygame.quit()
main()
