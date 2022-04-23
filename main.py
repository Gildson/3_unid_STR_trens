import arcade
import random
import time
import threading
from threading import Lock

class Velocity:
    def __init__(self):
        self.dx = 1
        self.dy = 1

class Point:
    def __init__(self):
        self.x = 0
        self.y = 0

class SizesAngles:
    def __init__(self):
        self.angle = 0
        self.width = 220
        self.height = 220

#Declaro os trilhos
class Trilho:
    def __init__(self):
        self.center = Point()
        self.prop = SizesAngles()

    def draw(self):
        arcade.draw_rectangle_outline(self.center.x, self.center.y, self.prop.width, self.prop.height, self.prop.color,
                                      border_width=5)

#Declaro os trens
class Trem:
    def __init__(self):
        self.center = Point()
        self.prop = SizesAngles()
        self.prop.width = 40
        self.prop.height = 20
        self.vel = Velocity()
        self.state = ""

    def draw(self):
        arcade.draw_rectangle_filled(self.center.x, self.center.y, self.prop.width, self.prop.height, self.prop.color,self.prop.angle)

    def para_direita(self):
        self.center.x += self.vel.dx
        self.prop.angle = 0

    def para_esquerda(self):
        self.center.x -= self.vel.dx
        self.prop.angle = 0

    def para_cima(self):
        self.center.y += self.vel.dy
        self.prop.angle = 90

    def para_baixo(self):
        self.center.y -= self.vel.dy
        self.prop.angle = 90

#Declara os semáforos
mutex1 = threading.Lock()
mutex2 = threading.Lock()
mutex3 = threading.Lock()
mutex4 = threading.Lock()
mutex5 = threading.Lock()

class Game(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.held_keys = set()
        self.trilhos = []
        self.create_trilho()
        self.trens = []
        self.create_train()
        self.amarelo_vel_x = 0
        self.amarelo_vel_y = 0
        self.azul_vel_x = 0
        self.azul_vel_y = 0
        self.vermelho_vel_x = 0
        self.vermelho_vel_y = 0

        #Coloco cada trem em uma thread
        self.t_a = threading.Thread(target=self.t_amarelo)
        self.t_z = threading.Thread(target=self.t_azul)
        self.t_v = threading.Thread(target=self.t_vermelho)
        self.t_a.start()
        self.t_z.start()
        self.t_v.start()

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Q : + TREM AMARELO", start_x=800, start_y=500, font_size=14, color=arcade.color.YELLOW)
        arcade.draw_text("W : + TREM AZUL", start_x=800, start_y=475, font_size=14, color=arcade.color.BLUE)
        arcade.draw_text("E : + TREM VERMELHO", start_x=800, start_y=450, font_size=14, color=arcade.color.RED)

        arcade.draw_text("A : - TREM AMARELO", start_x=1025, start_y=500, font_size=14, color=arcade.color.YELLOW)
        arcade.draw_text("S : - TREM AZUL", start_x=1025, start_y=475, font_size=14, color=arcade.color.BLUE)
        arcade.draw_text("D : - TREM VERMELHO", start_x=1025, start_y=450, font_size=14, color=arcade.color.RED)

        arcade.draw_text("VELOCIDADE PERMITIDA ENTRE 0 E 220 KM/H", start_x=800, start_y=350, font_size=14, color=arcade.color.WHITE)

        arcade.draw_text("TREM AMARELO", start_x=800, start_y=250, font_size=18, color=arcade.color.YELLOW)
        arcade.draw_text(str((self.trem_amarelo.vel.dx + self.trem_amarelo.vel.dy) * 20) + " km/h", start_x=800, start_y=225, font_size=18, color=arcade.color.YELLOW)

        arcade.draw_text("TREM AZUL", start_x=1050, start_y=250, font_size=18, color=arcade.color.BLUE)
        arcade.draw_text(str((self.trem_azul.vel.dx + self.trem_azul.vel.dy) * 20) + " km/h", start_x=1050, start_y=225, font_size=18, color=arcade.color.BLUE)

        arcade.draw_text("TREM VERMELHO", start_x=800, start_y=150, font_size=18, color=arcade.color.RED)
        arcade.draw_text(str((self.trem_vermelho.vel.dx + self.trem_vermelho.vel.dy) * 20) + " km/h", start_x=800, start_y=125, font_size=18, color=arcade.color.RED)

        for trem in self.trens:
            trem.draw()

        for trilho in self.trilhos:
            trilho.draw()

    #Cria os trens
    def create_train(self):
        self.trem_amarelo = Trem()
        self.trem_amarelo.center.x = 400
        self.trem_amarelo.center.y = 510
        self.trem_amarelo.prop.color = arcade.color.YELLOW

        self.trens.append(self.trem_amarelo)

        self.trem_azul = Trem()
        self.trem_azul.center.x = 600
        self.trem_azul.center.y = 510
        self.trem_azul.prop.color = arcade.color.BLUE

        self.trens.append(self.trem_azul)

        self.trem_vermelho = Trem()
        self.trem_vermelho.center.x = 525
        self.trem_vermelho.center.y = 65
        self.trem_vermelho.prop.color = arcade.color.RED

        self.trens.append(self.trem_vermelho)

    #cria os trilhos
    def create_trilho(self):
        self.trilho_amarelo = Trilho()
        self.trilho_amarelo.center.x = 400
        self.trilho_amarelo.center.y = 400
        self.trilho_amarelo.prop.color = arcade.color.LIGHT_YELLOW
        self.trilho_amarelo.draw()

        self.trilho_azul = Trilho()
        self.trilho_azul.center.x = 625
        self.trilho_azul.center.y = 400
        self.trilho_azul.prop.color = arcade.color.LIGHT_BLUE
        self.trilho_azul.draw()

        self.trilho_vermelho = Trilho()
        self.trilho_vermelho.center.x = 512
        self.trilho_vermelho.center.y = 175
        self.trilho_vermelho.prop.color = arcade.color.LIGHT_RED_OCHRE
        self.trilho_vermelho.prop.width = 445
        self.trilho_vermelho.draw()

        self.trilhos.append(self.trilho_amarelo)
        self.trilhos.append(self.trilho_azul)
        self.trilhos.append(self.trilho_vermelho)

    #parte dos comandos das velocidades
    def on_key_press(self, key, modifiers):
        if key == arcade.key.Q:
            self.amarelo_vel_x += 0.25
            self.amarelo_vel_y += 0.25
            if self.amarelo_vel_x >= 10:
                self.amarelo_vel_x = 10
            if self.amarelo_vel_y >= 10:
                self.amarelo_vel_y = 10

        if key == arcade.key.W:
            self.azul_vel_x += 0.25
            self.azul_vel_y += 0.25
            if self.azul_vel_x >= 10:
                self.azul_vel_x = 10
            if self.azul_vel_y >= 10:
                self.azul_vel_y = 10

        if key == arcade.key.E:
            self.vermelho_vel_x += 0.25
            self.vermelho_vel_y += 0.25
            if self.vermelho_vel_x >= 10:
                self.vermelho_vel_x = 10
            if self.vermelho_vel_y >= 10:
                self.vermelho_vel_y = 10

        if key == arcade.key.A:
            self.amarelo_vel_x -= 0.25
            self.amarelo_vel_y -= 0.25
            if self.amarelo_vel_x >= -1:
                self.amarelo_vel_x = -1
            if self.amarelo_vel_y >= -1:
                self.amarelo_vel_y = -1

        if key == arcade.key.S:
            self.azul_vel_x -= 0.25
            self.azul_vel_y -= 0.25
            if self.azul_vel_x >= -1:
                self.azul_vel_x = -1
            if self.azul_vel_y >= -1:
                self.azul_vel_y = -1

        if key == arcade.key.D:
            self.vermelho_vel_x -= 0.25
            self.vermelho_vel_y -= 0.25
            if self.vermelho_vel_x >= -1:
                self.vermelho_vel_x = -1
            if self.vermelho_vel_y >= -1:
                self.vermelho_vel_y = -1

    def update_velocidade_amarelo(self):
        return self.amarelo_vel_x, self.amarelo_vel_y

    def update_velocidade_azul(self):
        return self.azul_vel_x, self.azul_vel_y

    def update_velocidade_vermelho(self):
        return self.vermelho_vel_x, self.vermelho_vel_y

    #Trem amarelo
    def t_amarelo(self):
        while (1):
            if self.trem_amarelo.center.y > 509:
                self.L2(self.amarelo_vel_x, self.amarelo_vel_y)
            if self.trem_amarelo.center.x >= 509 and (self.trem_amarelo.center.y >= 291 and self.trem_amarelo.center.y <= 510):
                mutex1.acquire()
                mutex2.acquire()
                self.L3(self.trem_amarelo, self.amarelo_vel_x, self.amarelo_vel_y)
                mutex1.release()
            if self.trem_amarelo.center.y < 288 and (self.trem_amarelo.center.x <= 512 and self.trem_amarelo.center.x >= 290):
                self.L4(self.trem_amarelo, self.amarelo_vel_x, self.amarelo_vel_y)
                mutex2.release()
            if self.trem_amarelo.center.x <= 291 and (self.trem_amarelo.center.y >= 288 and self.trem_amarelo.center.y < 510):
                self.L1(self.amarelo_vel_x, self.amarelo_vel_y)

            time.sleep(0.03)

    #trem azul
    def t_azul(self):
        while (1):
            if self.trem_azul.center.y > 509:
                self.L5(self.azul_vel_x, self.azul_vel_y)
            if self.trem_azul.center.x >= 733 and (self.trem_azul.center.y <= 510 and self.trem_azul.center.y >= 289):
                self.L6(self.azul_vel_x, self.azul_vel_y)
            if self.trem_azul.center.y <= 290 and (self.trem_azul.center.x >= 514 and self.trem_azul.center.x <= 733):

                mutex3.acquire()
                self.L7(self.trem_azul, self.azul_vel_x, self.azul_vel_y)
                mutex3.release()
            if self.trem_azul.center.x <= 510 and (self.trem_azul.center.y >= 288 and self.trem_azul.center.y <= 509):
                mutex1.acquire()
                self.L3(self.trem_azul,self.azul_vel_x, self.azul_vel_y)
                mutex1.release()
            time.sleep(0.03)

    #trem vermelho
    def t_vermelho(self):
        while (1):
            if self.trem_vermelho.center.y > 291:
                if self.trem_vermelho.center.x <= 511:
                    mutex2.acquire()
                    mutex3.acquire()
                    self.L4(self.trem_vermelho, self.vermelho_vel_x, self.vermelho_vel_y)
                    mutex2.release()
                if self.trem_vermelho.center.x >= 511 and self.trem_vermelho.center.x <= 733:
                    self.L7(self.trem_vermelho, self.vermelho_vel_x, self.vermelho_vel_y)
                    mutex3.release()

            if self.trem_vermelho.center.y < 66 and (self.trem_vermelho.center.x > 290):
                self.L9(self.vermelho_vel_x, self.vermelho_vel_y)

            if self.trem_vermelho.center.x > 733 and (self.trem_vermelho.center.y >= 65 and self.trem_vermelho.center.y < 510):
                self.L8(self.vermelho_vel_x, self.vermelho_vel_y)

            elif self.trem_vermelho.center.x <= 291 and (self.trem_vermelho.center.y >= 65 and self.trem_vermelho.center.y < 510):
                self.L10(self.vermelho_vel_x, self.vermelho_vel_y)
            time.sleep(0.03)

    #Trilho 1
    def L1(self,vel_x,vel_y):
        self.trem_amarelo.center.x = 291
        self.trem_amarelo.vel.dx = 0
        self.trem_amarelo.vel.dy = 1 + self.amarelo_vel_y
        self.trem_amarelo.state = "L1"
        self.trem_amarelo.para_cima()

    #Trilho 2
    def L2(self, vel_x, vel_y):
        vel_x, vel_y = self.update_velocidade_amarelo()
        self.trem_amarelo.center.y = 510
        self.trem_amarelo.vel.dy = 0
        self.trem_amarelo.vel.dx = 1 + self.amarelo_vel_x
        self.trem_amarelo.state = "L2"
        self.trem_amarelo.para_direita()

    #Trilho 3
    def L3(self, trem, vel_x, vel_y):
        while (trem.center.y >= 288 and trem.center.y <= 510):
            if (trem.prop.color == arcade.color.YELLOW):
                vel_x, vel_y = self.update_velocidade_amarelo()
                trem.center.x = 509
                trem.vel.dx = 0
                trem.vel.dy = 1 + self.amarelo_vel_y
                trem.state = "L3"
                trem.para_baixo()
            else:
                vel_x, vel_y = self.update_velocidade_azul()
                trem.center.x = 509
                trem.vel.dx = 0
                trem.vel.dy = 1 + self.azul_vel_y
                trem.state = "L3"
                trem.para_cima()
            time.sleep(0.02)

    #Trilho 4
    def L4(self,trem, vel_x, vel_y):
        while (trem.center.x <= 511 and trem.center.x >= 291):
            if (trem.prop.color == arcade.color.RED):
                vel_x, vel_y = self.update_velocidade_vermelho()
                trem.center.y = 288
                trem.vel.dx = 1 + self.vermelho_vel_x
                trem.vel.dy = 0
                trem.state = "L4"
                trem.para_direita()
            else:
                vel_x, vel_y = self.update_velocidade_amarelo()
                trem.center.y = 288
                trem.vel.dx = 1 + self.amarelo_vel_x
                trem.vel.dy = 0
                trem.state = "L4"
                trem.para_esquerda()
            time.sleep(0.02)

    #Trilho 5
    def L5(self, vel_x, vel_y):
        vel_x, vel_y = self.update_velocidade_azul()
        self.trem_azul.center.y = 510
        self.trem_azul.vel.dx = 1 + self.azul_vel_x
        self.trem_azul.vel.dy = 0
        self.trem_azul.state = "L5"
        self.trem_azul.para_direita()

    #Trilho 6
    def L6(self, vel_x, vel_y):
        vel_x, vel_y = self.update_velocidade_azul()
        self.trem_azul.center.x = 733
        self.trem_azul.vel.dx = 0
        self.trem_azul.vel.dy = 1 + self.azul_vel_y
        self.trem_azul.state = "L6"
        self.trem_azul.para_baixo()

    #Trilho 7
    def L7(self, trem, vel_x, vel_y):
        while (trem.center.x <= 733 and trem.center.x >= 511):
            if (trem.prop.color == arcade.color.BLUE):
                vel_x, vel_y = self.update_velocidade_azul()
                trem.center.y = 288
                trem.vel.dx = 1 + self.azul_vel_x
                trem.vel.dy = 0
                trem.state = "L7"
                trem.para_esquerda()
            else:
                vel_x, vel_y = self.update_velocidade_vermelho()
                trem.center.y = 288
                trem.vel.dx = 1 + self.vermelho_vel_x
                trem.vel.dy = 0
                trem.state = "L4"
                trem.para_direita()
            time.sleep(0.02)

    #Trilho 8
    def L8(self, vel_x, vel_y):
        vel_x, vel_y = self.update_velocidade_vermelho()
        self.trem_vermelho.center.x = 734
        self.trem_vermelho.vel.dx = 0
        self.trem_vermelho.vel.dy = 1 + self.vermelho_vel_y
        self.trem_vermelho.state = "L8"
        self.trem_vermelho.para_baixo()

    #Trilho 9
    def L9(self, vel_x, vel_y):
        vel_x, vel_y = self.update_velocidade_vermelho()
        self.trem_vermelho.center.y = 65
        self.trem_vermelho.vel.dx = 1 + self.vermelho_vel_x
        self.trem_vermelho.vel.dy = 0
        self.trem_vermelho.state = "L9"
        self.trem_vermelho.para_esquerda()

    #Trilho 10
    def L10(self, vel_x, vel_y):
        vel_x, vel_y = self.update_velocidade_vermelho()
        self.trem_vermelho.center.x = 291
        self.trem_vermelho.vel.dx = 0
        self.trem_vermelho.vel.dy = 1 + self.vermelho_vel_y
        self.trem_vermelho.state = "L10"
        self.trem_vermelho.para_cima()

    def on_key_release(self, key: int, modifiers: int):
        if key in self.held_keys:
            self.held_keys.remove(key)

window = Game(1250, 550)
arcade.run()