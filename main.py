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
        self.color = arcade.color.BLUE

class Trilho:
    def __init__(self):
        self.center = Point()
        self.prop = SizesAngles()

    def draw(self):
        arcade.draw_rectangle_outline(self.center.x, self.center.y, self.prop.width, self.prop.height, self.prop.color,
                                      border_width=3)

class Trem:
    def __init__(self):
        self.center = Point()
        self.prop = SizesAngles()
        self.prop.width = 50
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
        self.verde_vel_x = 0
        self.verde_vel_y = 0
        self.roxo_vel_x = 0
        self.roxo_vel_y = 0
        self.amarelo_vel_x = 0
        self.amarelo_vel_y = 0
        self.azul_vel_x = 0
        self.azul_vel_y = 0

        self.t_v = threading.Thread(target=self.t_verde)
        self.t_r = threading.Thread(target=self.t_roxo)
        self.t_a = threading.Thread(target=self.t_amarelo)
        self.t_z = threading.Thread(target=self.t_azul)
        self.t_v.start()
        self.t_r.start()
        self.t_a.start()
        self.t_z.start()

    def update(self, delta_time):
        print("{}, {}".format(self.trem_azul.center.x, self.trem_azul.center.y))

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Q : + TREM VERDE", start_x=900, start_y=500, font_size=14, color=arcade.color.WHITE)
        arcade.draw_text("W : + TREM ROXO", start_x=900, start_y=475, font_size=14, color=arcade.color.WHITE)
        arcade.draw_text("E : + TREM AMARELO", start_x=900, start_y=450, font_size=14, color=arcade.color.WHITE)
        arcade.draw_text("R : + TREM AZUL", start_x=900, start_y=425, font_size=14, color=arcade.color.WHITE)

        arcade.draw_text("A : - TREM VERDE", start_x=1100, start_y=500, font_size=14, color=arcade.color.WHITE)
        arcade.draw_text("S : - TREM ROXO", start_x=1100, start_y=475, font_size=14, color=arcade.color.WHITE)
        arcade.draw_text("D : - TREM AMARELO", start_x=1100, start_y=450, font_size=14, color=arcade.color.WHITE)
        arcade.draw_text("F : - TREM AZUL", start_x=1100, start_y=425, font_size=14, color=arcade.color.WHITE)

        arcade.draw_text("VELOCIDADE PERMITIDA ENTRE 0 E 220 KM/H", start_x=900, start_y=350, font_size=14, color=arcade.color.WHITE)

        arcade.draw_text("TREM VERDE", start_x=900, start_y=300, font_size=18, color=arcade.color.GREEN)
        arcade.draw_text(str((self.trem_verde.vel.dx + self.trem_verde.vel.dy) * 20) + "km/h", start_x=900, start_y=275, font_size=18, color=arcade.color.GREEN)

        arcade.draw_text("TREM ROXO", start_x=1150, start_y=300, font_size=18, color=arcade.color.PURPLE)
        arcade.draw_text(str((self.trem_roxo.vel.dx + self.trem_roxo.vel.dy) * 20) + "km/h", start_x=1150, start_y=275, font_size=18, color=arcade.color.PURPLE)

        arcade.draw_text("TREM AMARELO", start_x=900, start_y=175, font_size=18, color=arcade.color.YELLOW)
        arcade.draw_text(str((self.trem_amarelo.vel.dx + self.trem_amarelo.vel.dy) * 20) + "km/h", start_x=900, start_y=150, font_size=18, color=arcade.color.YELLOW)

        arcade.draw_text("TREM AZUL", start_x=1150, start_y=300, font_size=18, color=arcade.color.BLUE)
        arcade.draw_text(str((self.trem_azul.vel.dx + self.trem_azul.vel.dy) * 20) + "km/h", start_x=1150, start_y=150, font_size=18, color=arcade.color.BLUE)

        for trem in self.trens:
            trem.draw()

        for trilho in self.trilhos:
            trilho.draw()

    def create_train(self):
        self.trem_verde = Trem()
        self.trem_verde.center.x = 300
        self.trem_verde.center.y = 510
        self.trem_verde.prop.color = arcade.color.GREEN

        self.trens.append(self.trem_verde)

        self.trem_roxo = Trem()
        self.trem_roxo.center.x = 525
        self.trem_roxo.center.y = 510
        self.trem_roxo.prop.color = arcade.color.PURPLE

        self.trens.append(self.trem_roxo)

        self.trem_amarelo = Trem()
        self.trem_amarelo.center.x = 750
        self.trem_amarelo.center.y = 510
        self.trem_amarelo.prop.color = arcade.color.YELLOW

        self.trens.append(self.trem_amarelo)

        self.trem_azul = Trem()
        self.trem_azul.center.x = 525
        self.trem_azul.center.y = 65
        self.trem_azul.prop.color = arcade.color.BLUE

        self.trens.append(self.trem_azul)

    def create_trilho(self):
        self.trilho_verde = Trilho()
        self.trilho_verde.center.x = 300
        self.trilho_verde.center.y = 400
        self.trilho_verde.prop.color = arcade.color.LIGHT_GREEN
        self.trilho_verde.draw()

        self.trilho_roxo = Trilho()
        self.trilho_roxo.center.x = 525
        self.trilho_roxo.center.y = 400
        self.trilho_roxo.prop.color = arcade.color.LIGHT_PASTEL_PURPLE
        self.trilho_roxo.draw()

        self.trilho_amarelo = Trilho()
        self.trilho_amarelo.center.x = 750
        self.trilho_amarelo.center.y = 400
        self.trilho_amarelo.prop.color = arcade.color.LIGHT_YELLOW
        self.trilho_amarelo.draw()

        self.trilho_azul = Trilho()
        self.trilho_azul.center.x = 525
        self.trilho_azul.center.y = 175
        self.trilho_azul.prop.color = arcade.color.LIGHT_BLUE
        self.trilho_azul.prop.width = 670
        self.trilho_azul.draw()

        self.trilhos.append(self.trilho_verde)
        self.trilhos.append(self.trilho_amarelo)
        self.trilhos.append(self.trilho_roxo)
        self.trilhos.append(self.trilho_azul)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.Q:
            self.verde_vel_x += 0.25
            self.verde_vel_y += 0.25
            if self.verde_vel_x >= 10:
                self.verde_vel_x = 10
            if self.verde_vel_y >= 10:
                self.verde_vel_y = 10

        if key == arcade.key.W:
            self.roxo_vel_x += 0.25
            self.roxo_vel_y += 0.25
            if self.roxo_vel_x >= 10:
                self.roxo_vel_x = 10
            if self.roxo_vel_y >= 10:
                self.roxo_vel_y = 10

        if key == arcade.key.E:
            self.amarelo_vel_x += 0.25
            self.amarelo_vel_y += 0.25
            if self.amarelo_vel_x >= 10:
                self.amarelo_vel_x = 10
            if self.amarelo_vel_y >= 10:
                self.amarelo_vel_y = 10

        if key == arcade.key.R:
            self.azul_vel_x += 0.25
            self.azul_vel_y += 0.25
            if self.azul_vel_x >= 10:
                self.azul_vel_x = 10
            if self.azul_vel_y >= 10:
                self.azul_vel_y = 10

        if key == arcade.key.A:
            self.verde_vel_x -= 0.25
            self.verde_vel_y -= 0.25
            if self.verde_vel_x >= -1:
                self.verde_vel_x = -1
            if self.verde_vel_y >= -1:
                self.verde_vel_y = -1

        if key == arcade.key.S:
            self.roxo_vel_x -= 0.25
            self.roxo_vel_y -= 0.25
            if self.roxo_vel_x >= -1:
                self.roxo_vel_x = -1
            if self.roxo_vel_y >= -1:
                self.roxo_vel_y = -1

        if key == arcade.key.D:
            self.amarelo_vel_x -= 0.25
            self.amarelo_vel_y -= 0.25
            if self.amarelo_vel_x >= -1:
                self.amarelo_vel_x = -1
            if self.amarelo_vel_y >= -1:
                self.amarelo_vel_y = -1

        if key == arcade.key.F:
            self.azul_vel_x -= 0.25
            self.azul_vel_y -= 0.25
            if self.azul_vel_x >= -1:
                self.azul_vel_x = -1
            if self.azul_vel_y >= -1:
                self.azul_vel_y = -1

    def update_velocidade_verde(self):
        return self.verde_vel_x, self.verde_vel_y

    def update_velocidade_roxo(self):
        return self.roxo_vel_x, self.roxo_vel_y

    def update_velocidade_amarelo(self):
        return self.amarelo_vel_x, self.amarelo_vel_y

    def update_velocidade_azul(self):
        return self.azul_vel_x, self.azul_vel_y

    def t_verde(self):
        while (1):

            if self.trem_verde.center.y > 509:
                self.L2(self.verde_vel_x, self.verde_vel_y)

            if self.trem_verde.center.x >= 410 and (self.trem_verde.center.y >= 291 and self.trem_verde.center.y <= 510):
                mutex2.acquire()
                mutex1.acquire()
                self.L3(self.trem_verde, self.verde_vel_x, self.verde_vel_y)
                mutex1.release()

            if self.trem_verde.center.y <= 291 and (self.trem_verde.center.x <= 412 and self.trem_verde.center.x >= 191):
                self.L4(self.trem_verde, self.verde_vel_x, self.verde_vel_y)
                mutex2.release()

            if self.trem_verde.center.x <= 191 and (self.trem_verde.center.y >= 288 and self.trem_verde.center.y < 510):
                self.L1(self.verde_vel_x, self.verde_vel_y)

            time.sleep(0.03)

    def t_roxo(self):
        while (1):
            if self.trem_roxo.center.y > 509:
                self.L7(self.roxo_vel_x, self.roxo_vel_y)

            if self.trem_roxo.center.x >= 633 and (self.trem_roxo.center.y <= 510 and self.trem_roxo.center.y >= 289):
                mutex4.acquire()
                self.L5(self.trem_roxo, self.roxo_vel_x, self.roxo_vel_y)
                mutex3.acquire()
                mutex4.release()

            if self.trem_roxo.center.y <= 289 and (self.trem_roxo.center.x >= 414 and self.trem_roxo.center.x <= 638):
                mutex1.acquire()
                self.L6(self.trem_roxo, self.roxo_vel_x, self.roxo_vel_y)
                mutex3.release()

            if self.trem_roxo.center.x <= 415 and (self.trem_roxo.center.y < 510):
                self.L3(self.trem_roxo,self.roxo_vel_x, self.roxo_vel_y)
                mutex1.release()

            time.sleep(0.03)

    def t_amarelo(self):
        while (1):

            if self.trem_amarelo.center.y > 509:
                self.L8(self.roxo_vel_x, self.roxo_vel_y)

            if self.trem_amarelo.center.x >= 859 and (self.trem_amarelo.center.y >= 289):
                self.L9(self.amarelo_vel_x, self.amarelo_vel_y)

            if (self.trem_amarelo.center.y <= 289) and (self.trem_amarelo.center.x <= 860 and self.trem_amarelo.center.x >= 637):
                mutex4.acquire()
                mutex5.acquire()
                self.L10(self.trem_amarelo, self.amarelo_vel_x, self.amarelo_vel_y)

            elif self.trem_amarelo.center.x <= 638 and (self.trem_amarelo.center.y >= 288 and self.trem_amarelo.center.y < 510):
                mutex5.release()
                self.L5(self.trem_amarelo, self.amarelo_vel_x, self.amarelo_vel_y)
                mutex4.release()

            time.sleep(0.03)

    def t_azul(self):
        while (1):
            if self.trem_azul.center.y > 287:
                if self.trem_azul.center.x <= 414:
                    mutex2.acquire()
                    self.L4(self.trem_azul, self.azul_vel_x, self.azul_vel_y)
                    mutex2.release()
                if self.trem_azul.center.x >= 413 and self.trem_azul.center.x <= 637:
                    mutex5.acquire()
                    mutex3.acquire()
                    self.L6(self.trem_azul, self.azul_vel_x, self.azul_vel_y)
                    mutex3.release()
                if self.trem_azul.center.x >= 636:
                    self.L10(self.trem_azul, self.azul_vel_x, self.azul_vel_y)
                    mutex5.release()

            if self.trem_azul.center.x > 859 and self.trem_azul.center.y >= 66:
                self.L12(self.azul_vel_x, self.azul_vel_y)

            if self.trem_azul.center.y < 66 and self.trem_azul.center.x >= 191:
                self.L13(self.azul_vel_x, self.azul_vel_y)

            elif self.trem_azul.center.x < 191 and self.trem_azul.center.y < 288:
                self.L11(self.azul_vel_x, self.azul_vel_y)

            time.sleep(0.03)

    def L1(self,vel_x,vel_y):
        self.trem_verde.center.x = 190
        self.trem_verde.vel.dx = 0
        self.trem_verde.vel.dy = 1 + self.verde_vel_y
        self.trem_verde.state = "L1"
        self.trem_verde.para_cima()

    def L2(self, vel_x, vel_y):
        vel_x, vel_y = self.update_velocidade_verde()
        self.trem_verde.center.y = 510
        self.trem_verde.vel.dy = 0
        self.trem_verde.vel.dx = 1 + vel_x
        self.trem_verde.state = "L2"
        self.trem_verde.para_direita()

    def L3(self, trem, vel_x, vel_y):
        while (trem.center.y >= 288 and trem.center.y <= 511):
            if (trem.prop.color == arcade.color.GREEN):
                vel_x, vel_y = self.update_velocidade_verde()
                trem.center.x = 412
                trem.vel.dx = 0
                trem.vel.dy = 1 + vel_y
                trem.state = "L3"
                trem.para_baixo()
            else:
                vel_x, vel_y = self.update_velocidade_roxo()
                trem.center.x = 412
                trem.vel.dx = 0
                trem.vel.dy = 1 + vel_y
                trem.state = "L3"
                trem.para_cima()
            time.sleep(0.02)

    def L4(self,trem, vel_x, vel_y):
        while (trem.center.x <= 413 and trem.center.x >= 189):
            if (trem.prop.color == arcade.color.BLUE):
                vel_x, vel_y = self.update_velocidade_azul()
                trem.center.y = 288
                trem.vel.dx = 1 + vel_x
                trem.vel.dy = 0
                trem.state = "L4"
                trem.para_direita()
            else:
                vel_x, vel_y = self.update_velocidade_verde()
                trem.center.y = 288
                trem.vel.dx = 1 + vel_x
                trem.vel.dy = 0
                trem.state = "L4"
                trem.para_esquerda()
            time.sleep(0.02)

    def L5(self, trem, vel_x, vel_y):
        while (trem.center.y >= 288 and trem.center.y <= 511):
            if (trem.prop.color == arcade.color.YELLOW):
                vel_x, vel_y = self.update_velocidade_amarelo()
                trem.center.x = 636
                trem.vel.dx = 0
                trem.vel.dy = 1 + vel_y
                trem.state = "L5"
                trem.para_cima()
            else:
                vel_x, vel_y = self.update_velocidade_roxo()
                trem.center.x = 637
                trem.vel.dx = 0
                trem.vel.dy = 1 + vel_y
                trem.state = "L5"
                trem.para_baixo()
            time.sleep(0.02)

    def L6(self, trem, vel_x, vel_y):
        i = 637
        j = 411
        while (trem.center.x <= i and trem.center.x >= j):
            if (trem.prop.color == arcade.color.PURPLE):
                j = 411
                vel_x, vel_y = self.update_velocidade_roxo()
                self.trem_roxo.center.y = 288
                self.trem_roxo.vel.dx = 1 + self.roxo_vel_x
                self.trem_roxo.vel.dy = 0
                self.trem_roxo.state = "L6"
                self.trem_roxo.para_esquerda()
            else:
                j = 189
                vel_x, vel_y = self.update_velocidade_azul()
                self.trem_azul.center.y = 288
                self.trem_azul.vel.dx = 1 + self.azul_vel_x
                self.trem_azul.vel.dy = 0
                self.trem_azul.state = "L6"
                self.trem_azul.para_direita()
            time.sleep(0.02)

    def L7(self, vel_x, vel_y):
        vel_x, vel_y = self.update_velocidade_roxo()
        self.trem_roxo.center.y = 510
        self.trem_roxo.vel.dx = 1 + vel_x
        self.trem_roxo.vel.dy = 0
        self.trem_roxo.state = "L7"
        self.trem_roxo.para_direita()

    def L8(self, vel_x, vel_y):
        vel_x, vel_y = self.update_velocidade_amarelo()
        self.trem_amarelo.center.y = 510
        self.trem_amarelo.vel.dx = 1 + vel_x
        self.trem_amarelo.vel.dy = 0
        self.trem_amarelo.state = "L8"
        self.trem_amarelo.para_direita()

    def L9(self, vel_x, vel_y):
        vel_x, vel_y = self.update_velocidade_amarelo()
        self.trem_amarelo.center.x = 860
        self.trem_amarelo.vel.dx = 0
        self.trem_amarelo.vel.dy = 1 + self.amarelo_vel_y
        self.trem_amarelo.state = "L9"
        self.trem_amarelo.para_baixo()

    def L10(self, trem, vel_x, vel_y):
        i = 860
        j = 637
        while (trem.center.x <= i and trem.center.x >= j):
            if (trem.prop.color == arcade.color.YELLOW):
                i = 860
                j = 637
                vel_x, vel_y = self.update_velocidade_amarelo()
                trem.center.y = 288
                trem.vel.dx = 1 + vel_x
                trem.vel.dy = 0
                trem.state = "L10"
                trem.para_esquerda()
            else:
                j = 637
                vel_x, vel_y = self.update_velocidade_azul()
                trem.center.y = 288
                trem.vel.dx = 1 + vel_x
                trem.vel.dy = 0
                trem.state = "L4"
                trem.para_direita()
            time.sleep(0.02)

    def L11(self, vel_x, vel_y):
        vel_x, vel_y = self.update_velocidade_azul()
        self.trem_azul.center.x = 190
        self.trem_azul.vel.dx = 0
        self.trem_azul.vel.dy = 1 + vel_y
        self.trem_azul.state = "L11"
        self.trem_azul.para_cima()

    def L12(self, vel_x, vel_y):
        vel_x, vel_y = self.update_velocidade_azul()
        self.trem_azul.center.x = 860
        self.trem_azul.vel.dx = 0
        self.trem_azul.vel.dy = 1 + vel_y
        self.trem_azul.state = "L12"
        self.trem_azul.para_baixo()

    def L13(self, vel_x, vel_y):
        vel_x, vel_y = self.update_velocidade_azul()
        self.trem_azul.center.y = 65
        self.trem_azul.vel.dx = 1 + vel_x
        self.trem_azul.vel.dy = 0
        self.trem_azul.state = "L13"
        self.trem_azul.para_esquerda()

    def on_key_release(self, key: int, modifiers: int):
        if key in self.held_keys:
            self.held_keys.remove(key)


window = Game(1400, 550)
arcade.run()