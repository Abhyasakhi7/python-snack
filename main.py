import pygame
import random
import sys
import math

pygame.init()

CELL_SIZE = 30
GRID_W, GRID_H = 20, 16
SCREEN_W, SCREEN_H = CELL_SIZE * GRID_W, CELL_SIZE * GRID_H + 80

SPEED_OPTIONS = [
    ("Santai", 6),
    ("Normal", 10),
    ("Ngebut", 15),
    ("Gokil", 22),
]
DEFAULT_SPEED_INDEX = 1

BG_COLOR = (255, 248, 220)
HEADER_COLOR = (255, 105, 180)
SNAKE_BODY_COLOR = (60, 200, 90)
SNAKE_BODY_COLOR2 = (100, 230, 130)
SNAKE_HEAD_COLOR = (30, 150, 60)
GRID_LINE = (240, 225, 190)
TEXT_COLOR = (80, 30, 90)
GAMEOVER_BG = (255, 220, 230)

FOOD_EMOJIS = ["🍕", "🍔", "🍩", "🍪", "🍇", "🌮", "🍎", "🧀"]
FUNNY_EAT_MESSAGES = [
    "NYAM NYAM! Ularnya doyan banget!",
    "Glek! Satu lagi masuk perut karet!",
    "Ularnya bilang: 'ENAK BANGET INI!'",
    "Perut ular makin panjang, bukan makin buncit!",
    "Level kekenyangan: LEGENDARY",
    "Ular: 'Masih muat kok, tenang aja'",
    "Suapan sultan buat si ular!",
    "Krauk! Makanan gak sempat teriak.",
]
FUNNY_GAMEOVER_MESSAGES = [
    "Waduh, ularnya nyungsep sendiri!",
    "GG WP, ularnya pusing tujuh keliling.",
    "Ular ini butuh kacamata kayaknya...",
    "Nabrak mulu, mirip kayak parkir mobil temenmu.",
    "Ularnya pensiun dini hari ini.",
    "Skill issue? Kayaknya iya.",
    "Ular: 'Aku cuma pengen rebahan doang tadi...'",
]
FUNNY_MENU_TAGLINES = [
    "Ular ini belum sarapan dari kemarin...",
    "Awas, ularnya lagi ngambek kalau kelamaan nunggu!",
    "100% bebas ular beracun, cuma laper doang.",
    "Rekor dunia makan terbanyak, siapa berani pecahin?",
    "Ular vs Tembok: siapa yang menang? (spoiler: tembok)",
]

pygame.font.init()
FONT_BIG = pygame.font.SysFont("segoeuiemoji,arial", 40, bold=True)
FONT_MED = pygame.font.SysFont("segoeuiemoji,arial", 26, bold=True)
FONT_SMALL = pygame.font.SysFont("segoeuiemoji,arial", 20)
FONT_EMOJI = pygame.font.SysFont("segoeuiemoji,applecoloremoji,notocoloremoji,arial", CELL_SIZE)

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Snake Kocak - Ular mu lapar euy!")
clock = pygame.time.Clock()


def random_food_pos(snake_body):
    while True:
        pos = (random.randint(0, GRID_W - 1), random.randint(0, GRID_H - 1))
        if pos not in snake_body:
            return pos


class Game:
    def __init__(self):
        self.state = "menu"
        self.menu_tagline = random.choice(FUNNY_MENU_TAGLINES)
        self.menu_wobble = 0
        self.speed_index = DEFAULT_SPEED_INDEX
        self.reset()

    def reset(self):
        cx, cy = GRID_W // 2, GRID_H // 2
        self.snake = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.food = random_food_pos(self.snake)
        self.food_emoji = random.choice(FOOD_EMOJIS)
        self.score = 0
        self.game_over = False
        self.message = "Ayo geser-geser, kasih makan ularnya!"
        self.message_timer = 0
        self.gameover_text = ""
        self.wobble = 0

    @property
    def current_fps(self):
        return SPEED_OPTIONS[self.speed_index][1]

    def handle_input(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        if self.state == "menu":
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.speed_index = (self.speed_index - 1) % len(SPEED_OPTIONS)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.speed_index = (self.speed_index + 1) % len(SPEED_OPTIONS)
            elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                self.reset()
                self.state = "playing"
            return

        if self.state == "gameover":
            if event.key == pygame.K_r:
                self.reset()
                self.state = "playing"
            elif event.key == pygame.K_m:
                self.state = "menu"
                self.menu_tagline = random.choice(FUNNY_MENU_TAGLINES)
            return

        if event.key == pygame.K_w and self.direction != (0, 1):
            self.next_direction = (0, -1)
        elif event.key == pygame.K_s and self.direction != (0, -1):
            self.next_direction = (0, 1)
        elif event.key == pygame.K_a and self.direction != (1, 0):
            self.next_direction = (-1, 0)
        elif event.key == pygame.K_d and self.direction != (-1, 0):
            self.next_direction = (1, 0)

    def update(self):
        self.menu_wobble += 1

        if self.state != "playing":
            return
        if self.game_over:
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        if (
            new_head[0] < 0 or new_head[0] >= GRID_W
            or new_head[1] < 0 or new_head[1] >= GRID_H
            or new_head in self.snake
        ):
            self.game_over = True
            self.state = "gameover"
            self.gameover_text = random.choice(FUNNY_GAMEOVER_MESSAGES)
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.food = random_food_pos(self.snake)
            self.food_emoji = random.choice(FOOD_EMOJIS)
            self.message = random.choice(FUNNY_EAT_MESSAGES)
            self.message_timer = 30
        else:
            self.snake.pop()

        if self.message_timer > 0:
            self.message_timer -= 1
        else:
            self.message = "Terus gerak, jangan bengong ularnya laper mulu!"

        self.wobble += 1

    def draw_header(self):
        pygame.draw.rect(screen, HEADER_COLOR, (0, 0, SCREEN_W, 80))
        title = FONT_MED.render(f"Snake Kocak  |  Skor: {self.score}", True, (255, 255, 255))
        screen.blit(title, (14, 10))
        msg_surf = FONT_SMALL.render(self.message, True, (255, 255, 230))
        screen.blit(msg_surf, (14, 46))

    def draw_grid(self):
        for x in range(GRID_W):
            for y in range(GRID_H):
                rect = pygame.Rect(x * CELL_SIZE, 80 + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, GRID_LINE, rect, 1)

    def draw_snake(self):
        for i, (x, y) in enumerate(self.snake):
            wob = int(2 * math.sin(self.wobble * 0.3 + i))
            rect = pygame.Rect(
                x * CELL_SIZE + 2, 80 + y * CELL_SIZE + 2 + wob, CELL_SIZE - 4, CELL_SIZE - 4
            )
            color = SNAKE_HEAD_COLOR if i == 0 else (
                SNAKE_BODY_COLOR if i % 2 == 0 else SNAKE_BODY_COLOR2
            )
            pygame.draw.rect(screen, color, rect, border_radius=10)

            if i == 0:
                cx = x * CELL_SIZE + CELL_SIZE // 2
                cy = 80 + y * CELL_SIZE + CELL_SIZE // 2 + wob
                eye_offset = 6
                pygame.draw.circle(screen, (255, 255, 255), (cx - eye_offset, cy - 4), 4)
                pygame.draw.circle(screen, (255, 255, 255), (cx + eye_offset, cy - 4), 4)
                pygame.draw.circle(screen, (0, 0, 0), (cx - eye_offset, cy - 4), 2)
                pygame.draw.circle(screen, (0, 0, 0), (cx + eye_offset, cy - 4), 2)
                if not self.game_over:
                    pygame.draw.arc(
                        screen, (0, 0, 0),
                        (cx - 7, cy - 2, 14, 10), math.pi, 2 * math.pi, 2
                    )

    def draw_food(self):
        x, y = self.food
        cx = x * CELL_SIZE + CELL_SIZE // 2
        cy = 80 + y * CELL_SIZE + CELL_SIZE // 2
        bounce = int(4 * abs(math.sin(self.wobble * 0.4)))
        emoji_surf = FONT_EMOJI.render(self.food_emoji, True, (0, 0, 0))
        rect = emoji_surf.get_rect(center=(cx, cy - bounce))
        screen.blit(emoji_surf, rect)

    def draw_gameover(self):
        overlay = pygame.Surface((SCREEN_W, SCREEN_H))
        overlay.set_alpha(230)
        overlay.fill(GAMEOVER_BG)
        screen.blit(overlay, (0, 0))

        title = FONT_BIG.render("GAME OVER!", True, (200, 30, 60))
        screen.blit(title, title.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 - 90)))

        funny = FONT_MED.render(self.gameover_text, True, TEXT_COLOR)
        screen.blit(funny, funny.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 - 30)))

        score_txt = FONT_MED.render(f"Skor akhir kamu: {self.score}", True, TEXT_COLOR)
        screen.blit(score_txt, score_txt.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 20)))

        hint = FONT_SMALL.render("Tekan R untuk main lagi, M buat ke menu, ESC buat kabur", True, TEXT_COLOR)
        screen.blit(hint, hint.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 70)))

    def draw_menu(self):
        screen.fill(BG_COLOR)

        deco_y = 120
        for i in range(8):
            wob = int(10 * math.sin(self.menu_wobble * 0.1 + i * 0.6))
            cx = 120 + i * 55
            color = SNAKE_HEAD_COLOR if i == 0 else (
                SNAKE_BODY_COLOR if i % 2 == 0 else SNAKE_BODY_COLOR2
            )
            pygame.draw.circle(screen, color, (cx, deco_y + wob), 22)
            if i == 0:
                pygame.draw.circle(screen, (255, 255, 255), (cx - 6, deco_y + wob - 4), 5)
                pygame.draw.circle(screen, (255, 255, 255), (cx + 6, deco_y + wob - 4), 5)
                pygame.draw.circle(screen, (0, 0, 0), (cx - 6, deco_y + wob - 4), 2)
                pygame.draw.circle(screen, (0, 0, 0), (cx + 6, deco_y + wob - 4), 2)

        title = FONT_BIG.render("SNAKE KOCAK", True, HEADER_COLOR)
        screen.blit(title, title.get_rect(center=(SCREEN_W // 2, deco_y + 90)))

        tagline = FONT_SMALL.render(self.menu_tagline, True, TEXT_COLOR)
        screen.blit(tagline, tagline.get_rect(center=(SCREEN_W // 2, deco_y + 140)))

        play_color = (60, 200, 90)
        btn_w, btn_h = 260, 60
        btn_rect = pygame.Rect(0, 0, btn_w, btn_h)
        btn_rect.center = (SCREEN_W // 2, deco_y + 220)
        pygame.draw.rect(screen, play_color, btn_rect, border_radius=16)
        play_txt = FONT_MED.render("SPASI untuk Main!", True, (255, 255, 255))
        screen.blit(play_txt, play_txt.get_rect(center=btn_rect.center))

        speed_label_y = deco_y + 285
        speed_name, speed_fps = SPEED_OPTIONS[self.speed_index]
        speed_title = FONT_SMALL.render("Kecepatan Ular (panah kiri/kanan)", True, TEXT_COLOR)
        screen.blit(speed_title, speed_title.get_rect(center=(SCREEN_W // 2, speed_label_y)))

        chip_gap = 14
        chip_h = 40
        chip_widths = []
        chip_surfs = []
        for name, _ in SPEED_OPTIONS:
            surf = FONT_SMALL.render(name, True, (255, 255, 255))
            chip_surfs.append(surf)
            chip_widths.append(surf.get_width() + 28)

        total_w = sum(chip_widths) + chip_gap * (len(SPEED_OPTIONS) - 1)
        start_x = SCREEN_W // 2 - total_w // 2
        chip_y = speed_label_y + 26

        x = start_x
        for idx, (name, fps) in enumerate(SPEED_OPTIONS):
            w = chip_widths[idx]
            chip_rect = pygame.Rect(x, chip_y, w, chip_h)
            is_selected = idx == self.speed_index
            bg_color = (255, 105, 180) if is_selected else (210, 200, 190)
            pygame.draw.rect(screen, bg_color, chip_rect, border_radius=14)
            if is_selected:
                pygame.draw.rect(screen, (120, 30, 80), chip_rect, 3, border_radius=14)
            label_color = (255, 255, 255) if is_selected else (90, 80, 75)
            label = FONT_SMALL.render(name, True, label_color)
            screen.blit(label, label.get_rect(center=chip_rect.center))
            x += w + chip_gap

        instr_lines = [
            "Kontrol: W A S D",
            "R = ulang setelah kalah   |   M = balik ke menu   |   ESC = kabur",
        ]
        for j, line in enumerate(instr_lines):
            surf = FONT_SMALL.render(line, True, TEXT_COLOR)
            screen.blit(surf, surf.get_rect(center=(SCREEN_W // 2, chip_y + chip_h + 26 + j * 28)))

        pygame.display.flip()

    def draw(self):
        if self.state == "menu":
            self.draw_menu()
            return

        screen.fill(BG_COLOR)
        self.draw_grid()
        self.draw_food()
        self.draw_snake()
        self.draw_header()
        if self.state == "gameover":
            self.draw_gameover()
        pygame.display.flip()


def main():
    game = Game()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            game.handle_input(event)

        game.update()
        game.draw()
        clock.tick(game.current_fps)


if __name__ == "__main__":
    main()