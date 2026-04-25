import pygame
import random

# 初始化Pygame
pygame.init()

# 屏幕尺寸
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
PLAYER_SIZE = 10
FPS = 10

# 颜色定义
BACKGROUND_COLOR = (30, 30, 30)
SNAKE_COLOR = (50, 200, 50)
FOOD_COLOR = (200, 50, 50)
TEXT_COLOR = (255, 255, 255)

# 创建游戏窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("贪吃蛇")

# 帧率控制
clock = pygame.time.Clock()

# 蛇的初始位置和速度
snake = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
direction = (0, 0)
score = 0
game_over = False
paused = False

# 食物生成函数
def generate_food():
    return (random.randint(0, (SCREEN_WIDTH - PLAYER_SIZE) // PLAYER_SIZE) * PLAYER_SIZE,
            random.randint(0, (SCREEN_HEIGHT - PLAYER_SIZE) // PLAYER_SIZE) * PLAYER_SIZE)

food = generate_food()

# 按钮相关变量
start_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 25, 100, 50)
pause_button_rect = pygame.Rect(SCREEN_WIDTH - 110, 10, 100, 50)

# 游戏主循环
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game_over:
                if start_button_rect.collidepoint(event.pos):
                    # 开始游戏
                    snake = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
                    direction = (0, 0)
                    score = 0
                    game_over = False
                    paused = False
                    food = generate_food()
                elif pause_button_rect.collidepoint(event.pos):
                    # 暂停/恢复游戏
                    paused = not paused
            else:
                # 重新开始游戏
                snake = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
                direction = (0, 0)
                score = 0
                game_over = False
                paused = False
                food = generate_food()

    if not game_over and not paused:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and direction != (0, PLAYER_SIZE):
            direction = (0, -PLAYER_SIZE)
        elif keys[pygame.K_DOWN] and direction != (0, -PLAYER_SIZE):
            direction = (0, PLAYER_SIZE)
        elif keys[pygame.K_LEFT] and direction != (PLAYER_SIZE, 0):
            direction = (-PLAYER_SIZE, 0)
        elif keys[pygame.K_RIGHT] and direction != (-PLAYER_SIZE, 0):
            direction = (PLAYER_SIZE, 0)

        # 移动蛇
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake.insert(0, new_head)

        # 检测是否吃到食物
        if new_head == food:
            score += 10
            food = generate_food()
        else:
            snake.pop()

        # 检测碰撞
        if (new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH or
            new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT or
            new_head in snake[1:]):
            game_over = True

    # 绘制背景
    screen.fill(BACKGROUND_COLOR)

    # 绘制蛇
    for segment in snake:
        pygame.draw.rect(screen, SNAKE_COLOR, (*segment, PLAYER_SIZE, PLAYER_SIZE))

    # 绘制食物
    pygame.draw.rect(screen, FOOD_COLOR, (*food, PLAYER_SIZE, PLAYER_SIZE))

    # 绘制按钮
    if game_over:
        # 显示重新开始按钮
        pygame.draw.rect(screen, TEXT_COLOR, start_button_rect)
        font = pygame.font.SysFont(None, 36)
        text = font.render("重新开始", True, BACKGROUND_COLOR)
        screen.blit(text, (start_button_rect.centerx - text.get_width() // 2, start_button_rect.centery - text.get_height() // 2))
    else:
        # 显示暂停按钮
        pygame.draw.rect(screen, TEXT_COLOR, pause_button_rect)
        font = pygame.font.SysFont(None, 36)
        text = font.render("暂停" if not paused else "开始", True, BACKGROUND_COLOR)
        screen.blit(text, (pause_button_rect.centerx - text.get_width() // 2, pause_button_rect.centery - text.get_height() // 2))

    # 显示分数
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"分数: {score}", True, TEXT_COLOR)
    screen.blit(text, (10, 10))

    # 显示游戏结束信息
    if game_over:
        font = pygame.font.SysFont(None, 48)
        text = font.render(f"游戏结束! 分数: {score}", True, TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

    # 刷新画面
    pygame.display.flip()