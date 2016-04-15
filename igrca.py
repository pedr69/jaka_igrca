import pygame

SIRINA_EKRANA= 800
VISINA_EKRANA= 600

class osebek(pygame.sprite.Sprite):
    def __init__(self,ovire=None):
        super().__init__()
        sirina=40
        visina=40

        self.image=pygame.Surface((sirina,visina),pygame.SRCALPHA)
        self.image.fill((238,90,255))
        self.rect=self.image.get_rect()

        self.hitrost_x=0
        self.hitrost_y=0
    def update(self):
        #smer X
        #smer Y
        if self.hitrost<20:
            self.hitrost_y+=0.4
        self.rect_y += self.hitrost_y
        self.rect_y %= VISINA_EKRANA
        if self.ovire:
            trki=pygame.spritecollide(self,self.ovire,False)
            for ovira in trki:
                if self.hitrost_y < 0:
                    self.rect.top=ovira.rect.bottom
                if self.hitrost_x > 0:
                    self.rect.bottom=ovira.rect.top
                self.hitrost_y=0

        def pojdi_levo(self):
            self.desno=False;
            self.hitrost_x = -4;
            self.hodim=true
        def pojdi_desno(self):
            self.desno=True;
            self.hitrost_x = 4;
            self.hodim=True;
        def stop(self):
            self.hodim=False;
            self.hitrost_x=0
        def skoci(self):
            self.hitrost_y -=10
        
class zadeva(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.Surface((SIRINA_EKRANA,VISINA_EKRANA/2))
        self.image.fill((150,150,150))
        self.rect=self.image.get_rect()
        self.rect.x=0
        self.rect.y=VISINA_EKRANA/2

def main():
    ekran=pygame.display.set_mode([SIRINA_EKRANA,VISINA_EKRANA])
    ekran.fill((255,255,255))
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
        for dogodek in pygame.event.get():
            if dogodek.type== pygame.QUIT:
                konec_zanke=True
        
        skupina.draw(ekran)
        crvi.draw(ekran)
        pygame.display.flip()
    pygame.quit()
main()
