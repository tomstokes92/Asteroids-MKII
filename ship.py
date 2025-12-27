# ship.py
import math
import pygame


def wrap_pos(x: float, y: float, w: int, h: int) -> tuple[float, float]:
    return (x % w, y % h)


def rotate_point(px: float, py: float, angle_rad: float) -> tuple[float, float]:
    ca = math.cos(angle_rad)
    sa = math.sin(angle_rad)
    return (px * ca - py * sa, px * sa + py * ca)


class Ship:
    def __init__(self, x: float, y: float):
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(0, 0)

        # Angle in radians (0 means facing right). We'll treat "forward" as angle direction.
        self.angle = 0.0  # start facing up

        # Tuning
        self.turn_speed = math.radians(320)     # radians/sec
        self.thrust_accel = 380.0              # pixels/sec^2
        self.reverse_accel = 220.0              # reverse weaker
        self.max_speed = 520.0                  # pixels/sec
        self.friction = 0.99                  # velocity multiplier per frame-ish (we'll dt-adjust below)

        # Size scale for goose drawing
        self.thrusting = False
        self.reversing = False
        
        self.base_image = pygame.image.load("./sprites/goose_sprite.png").convert_alpha()
        SCALE = 0.1
        w = int(self.base_image.get_width() * SCALE)
        h = int(self.base_image.get_height() * SCALE)
        self.base_image = pygame.transform.smoothscale(self.base_image, (w, h))   
        self.image = self.base_image
        self.rect = self.image.get_rect(center=(x, y))
        self.radius = self.image.get_width() * 0.4


    def forward_vector(self) -> pygame.Vector2:
        # Forward is the direction the ship faces
        return pygame.Vector2(math.cos(self.angle), math.sin(self.angle))

    def update(self, dt: float, keys, screen_w: int, screen_h: int):
        self.thrusting = False
        self.reversing = False

        # Rotate
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.angle -= self.turn_speed * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.angle += self.turn_speed * dt

        fwd = self.forward_vector()

        # Forward thrust
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vel += fwd * (self.thrust_accel * dt)
            self.thrusting = True

        # Reverse thrust (backwards)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vel -= fwd * (self.reverse_accel * dt)
            self.reversing = True

        # Clamp speed
        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)

        # Friction (dt-adjust)
        friction_dt = self.friction ** (dt * 60.0)
        self.vel *= friction_dt

        # Move + wrap
        self.pos += self.vel * dt
        self.pos.x %= screen_w
        self.pos.y %= screen_h

        # drift
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_a] or keys[pygame.K_d]:
            self.vel *= 0.995


    def draw(self, surface: pygame.Surface):
    # Pygame rotates CCW, so negate degrees
        self.image = pygame.transform.rotozoom(
            self.base_image,
            -math.degrees(self.angle),
            1.0
        )
        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        surface.blit(self.image, self.rect)
    def draw_thrust(self, surface):
        if not self.thrusting:
            return

        # Tail offset in local space (behind the sprite)
        offset = pygame.Vector2(-self.base_image.get_width() * 0.5, 0)
        offset.rotate_ip_rad(self.angle)

        puff_pos = self.pos + offset

        pygame.draw.circle(surface, (230, 230, 255), puff_pos, 10)
