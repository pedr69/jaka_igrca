import pygame
from math import sin, cos, pi
from models import SIRINA_EKRANA, VISINA_EKRANA, zadeva, osebek, izstrelek


def main():
    pygame.font.init()
    ekran=pygame.display.set_mode([SIRINA_EKRANA,VISINA_EKRANA])
    pygame.display.set_caption("legendarna igrca")

    ozadje = zadeva(0, 3*VISINA_EKRANA/4, SIRINA_EKRANA,VISINA_EKRANA/4)
    ploscad = zadeva(50, 350, 200, 20)
    ploscad2= zadeva(500, 50, 1, 3000)

    skupina=pygame.sprite.Group()
    skupina.add(ozadje)
    skupina.add(ploscad)
    #skupina.add(ploscad2)
    metki=pygame.sprite.Group()
    crvi=pygame.sprite.Group()
    crv=osebek(skupina,metki)
    crvi.add(crv)
    crv2 = osebek(skupina,metki,(255, 0, 102))
    ura=pygame.time.Clock()
    crvi.add(crv2)
    konec_zanke=False


    font = pygame.font.Font(None, 36)
    text = font.render("ground: "+str(crv.ground), 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = ekran.get_rect().centerx
    while not konec_zanke:
        ura.tick(60)
        # User input
        for dogodek in pygame.event.get():
            if dogodek.type == pygame.QUIT:
                konec_zanke = True
            elif dogodek.type == pygame.KEYDOWN:
                # Player 1
                if dogodek.key == pygame.K_a:
                    crv.pojdi_levo()
                elif dogodek.key == pygame.K_SPACE:
                    crv.ustreli()
                elif dogodek.key == pygame.K_d:                                                  
                    crv.pojdi_desno()
                elif dogodek.key == pygame.K_w:
                    crv.skoci()
                elif dogodek.key == pygame.K_h:
                    crv.hitrost_vrtenja = 1;
                elif dogodek.key == pygame.K_k:
                    crv.hitrost_vrtenja = -1;
                elif dogodek.key == pygame.K_u:
                    crv.hitrost_hitrosti_strela = 0.01
                elif dogodek.key == pygame.K_j:
                    crv.hitrost_hitrosti_strela = -0.01
                # Player 2
                if dogodek.key == pygame.K_LEFT:
                    crv2.pojdi_levo()
                elif dogodek.key == pygame.K_KP0:
                    crv2.ustreli()
                elif dogodek.key == pygame.K_RIGHT:                                                  
                    crv2.pojdi_desno()
                elif dogodek.key == pygame.K_UP:
                    crv2.skoci()
                elif dogodek.key == pygame.K_KP1:
                    crv2.hitrost_vrtenja = 1;
                elif dogodek.key == pygame.K_KP3:
                    crv2.hitrost_vrtenja = -1;
                elif dogodek.key == pygame.K_KP5:
                    crv2.hitrost_hitrosti_strela = 0.01
                elif dogodek.key == pygame.K_KP2:
                    crv2.hitrost_hitrosti_strela = -0.01
            if dogodek.type == pygame.KEYUP:
                # Player 1
                if dogodek.key == pygame.K_a and crv.hitrost_x < 0:
                    crv.stop()
                elif dogodek.key == pygame.K_d and crv.hitrost_x > 0:
                    crv.stop()
                elif dogodek.key == pygame.K_u or dogodek.key == pygame.K_j: 
                    crv.hitrost_hitrosti_strela = 0
                elif dogodek.key == pygame.K_h or dogodek.key == pygame.K_k:
                    crv.hitrost_vrtenja = 0
                # Player 2
                if dogodek.key == pygame.K_LEFT and crv2.hitrost_x < 0:
                    crv2.stop()
                elif dogodek.key == pygame.K_RIGHT and crv2.hitrost_x > 0:
                    crv2.stop()   
                elif dogodek.key == pygame.K_KP5 or dogodek.key == pygame.K_KP2: 
                    crv2.hitrost_hitrosti_strela = 0
                elif dogodek.key == pygame.K_KP1 or dogodek.key == pygame.K_KP3:
                    crv2.hitrost_vrtenja = 0
            if dogodek.type == pygame.MOUSEBUTTONDOWN:
                crv.ustreli()
            
        # Zganjaj fiziko
        crvi.update()
        skupina.update()
        metki.update()
        # Risanje
        ekran.fill((255,255,255))
        text = font.render("ground: "+str(crv.ground), 1, (10, 10, 10))
        ekran.blit(text, textpos)
        skupina.draw(ekran) #narise ozadje
        crvi.draw(ekran) #narise crve
        metki.draw(ekran); #narise metke
        
        pygame.display.flip()
       # print("crv.hitrost_x: "+str(crv.hitrost_x));
    pygame.quit()
main()
