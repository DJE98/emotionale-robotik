import os

import pygame
from robot import Robot

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

WIDTH, HEIGHT = 320, 240


from cli import print_emotions


class OwnRobot(Robot):
    emotion = "Neutral"
    old_emotion = []
    changed_emotions = False

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Own Robot")

        self.soundboard = {
            # https://freesound.org/people/SergeQuadrado/sounds/637070/
            "Surprise": pygame.mixer.Sound("sound/surprise.wav"),
            # https://freesound.org/people/igroglaz/sounds/633228/
            "Happiness": pygame.mixer.Sound("sound/nice.wav"),
        }

    def update(self, image, emotions):
        print(self.emotion)
        self.decide_emotion(emotions)
        self.update_emotion_changed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        self.draw_face()
        self.make_sound()
        self.old_emotion = self.emotion

    def decide_emotion(self, emotions):
        if len(emotions) != 0:
            self.emotion = emotions[0]
        if self.emotion == "Contempt":
            self.emotion = "Neutral"

    def update_emotion_changed(self):
        self.changed_emotions = self.old_emotion != self.emotion

    def draw_face(self):
        self.screen.fill(WHITE)
        self.draw_head()
        self.draw_eyes()
        self.draw_mouth()
        pygame.display.flip()

    def draw_head(self):
        pygame.draw.circle(self.screen, BLACK, (WIDTH // 2, HEIGHT // 2), 120)

    def draw_eyes(self):
        eye_x_distance = 60
        eye_y_distance = 40
        eye_size = 20
        eye_color = WHITE

        if self.emotion == "Surprise":
            eye_y_distance = 20
            eye_size = 30
        if self.emotion == "Fear" or self.emotion == "Sadness":
            eye_y_distance = 50
        if self.emotion == "Anger":
            eye_color = RED

        pygame.draw.circle(
            self.screen,
            eye_color,
            (WIDTH // 2 - eye_x_distance, HEIGHT // 2 - eye_y_distance),
            eye_size,
        )
        pygame.draw.circle(
            self.screen,
            eye_color,
            (WIDTH // 2 + eye_x_distance, HEIGHT // 2 - eye_y_distance),
            eye_size,
        )

    def draw_mouth(self):
        mouth_rect = (WIDTH // 2 - 90, HEIGHT // 2, 180, 60)
        if self.emotion == "Happiness":
            pygame.draw.arc(self.screen, WHITE, mouth_rect, 3.14, 2 * 3.14, 10)
        if self.emotion == "Fear" or self.emotion == "Sadness":
            pygame.draw.arc(self.screen, WHITE, mouth_rect, 0, 3.14, 10)
        if self.emotion == "Anger":
            pygame.draw.line(
                self.screen,
                RED,
                (WIDTH // 2 - 90, HEIGHT // 2 + 30),
                (WIDTH // 2 + 90, HEIGHT // 2 + 30),
                10,
            )
        if self.emotion == "Neutral" or self.emotion == "Surprise":
            pygame.draw.line(
                self.screen,
                WHITE,
                (WIDTH // 2 - 90, HEIGHT // 2 + 30),
                (WIDTH // 2 + 90, HEIGHT // 2 + 30),
                10,
            )

    def make_sound(self):
        if (
            self.emotion == "Surprise" or self.emotion == "Happiness"
        ) and self.changed_emotions:
            pygame.mixer.Sound.play(self.soundboard[self.emotion])
