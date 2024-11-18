import pygame
import random
import numpy as np

# Inicializar pygame
pygame.init()

# Configuración de pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Genético")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Parámetros del juego
GRAVITY = 1.2
POPULATION_SIZE = 10
MUTATION_RATE = 0.1
GENERATION = 1

# Clase Dino
class Dino:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT - 60
        self.width = 40
        self.height = 40
        self.vel_y = 0
        self.jumping = False
        self.alive = True
        self.distance = 0
        # "Cerebro" del dinosaurio: pesos aleatorios
        self.brain = np.random.rand(2)

    def jump(self):
        if not self.jumping:
            self.vel_y = -20
            self.jumping = True

    def move(self):
        if self.jumping:
            self.y += self.vel_y
            self.vel_y += GRAVITY
            if self.y >= SCREEN_HEIGHT - 60:
                self.y = SCREEN_HEIGHT - 60
                self.jumping = False

    def decide(self, cactus_x, cactus_width):
        # Entrada: distancia al cactus
        input1 = cactus_x - self.x
        # Entrada: tamaño del cactus
        input2 = cactus_width
        # Decisión basada en el "cerebro"
        decision = np.dot([input1, input2], self.brain)
        if decision > 100:  # Umbral arbitrario para decidir saltar
            self.jump()

# Clase Cactus
class Cactus:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.y = SCREEN_HEIGHT - 60
        self.width = random.randint(20, 50)
        self.height = 50
        self.speed = 5

    def move(self):
        self.x -= self.speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH
            self.width = random.randint(20, 50)

# Algoritmo Genético
def select_parents(population):
    # Selección por aptitud (los mejores tienen más peso)
    fitness = np.array([dino.distance for dino in population])
    fitness /= fitness.sum()
    parents = np.random.choice(population, size=2, p=fitness)
    return parents

def crossover(parent1, parent2):
    # Promedio de los cerebros de los padres
    child_brain = (parent1.brain + parent2.brain) / 2
    return child_brain

def mutate(brain):
    # Alterar aleatoriamente los pesos con probabilidad MUTATION_RATE
    if random.random() < MUTATION_RATE:
        brain += np.random.normal(0, 0.1, size=brain.shape)
    return brain


# Función principal
def main():
    global GENERATION
    population = [Dino() for _ in range(POPULATION_SIZE)]
    cactus = Cactus()
    clock = pygame.time.Clock()

    while True:
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, (cactus.x, cactus.y, cactus.width, cactus.height))  # Dibujar cactus

        for dino in population:
            if dino.alive:
                dino.decide(cactus.x, cactus.width)
                dino.move()
                dino.distance += 1
                pygame.draw.rect(screen, BLACK, (dino.x, dino.y, dino.width, dino.height))  # Dibujar dinosaurio

                # Colisión
                if dino.x + dino.width > cactus.x and dino.x < cactus.x + cactus.width:
                    if dino.y + dino.height > cactus.y:
                        dino.alive = False

        # Movimiento del cactus
        cactus.move()

        # Si todos los dinosaurios murieron
        if not any(dino.alive for dino in population):
            # Nueva generación
            GENERATION += 1
            next_population = []
            for _ in range(POPULATION_SIZE):
                parent1, parent2 = select_parents(population)
                child = Dino()
                child.brain = mutate(crossover(parent1, parent2))
                next_population.append(child)
            population = next_population
            cactus = Cactus()

        # Mostrar generación
        font = pygame.font.Font(None, 36)
        text = font.render(f"Generación: {GENERATION}", True, BLACK)
        screen.blit(text, (10, 10))

        pygame.display.update()
        clock.tick(30)

# Iniciar el juego
main()
