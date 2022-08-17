from Functions import *
from random import randrange as random
from math import pi, sqrt, exp, sin, cos, atan2


class Movable:
    def __init__(self, image, x_offset, y_offset, x_vel, y_vel, mass, max_vel, max_acc, charge, fuel):
        # Extract Fields
        self.x_pos = x_offset
        self.y_pos = y_offset
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.mass = mass
        self.max_vel = max_vel
        self.max_acc = max_acc
        self.charge = charge
        self.fuel = fuel
        self.image = image
        # Implicit Fields
        self.width = None
        self.height = None
        self.radius = None
        self.thrust = None
        self.drag_coeff = None
        self.set_size(image)
        self.set_thrust()
        self.set_drag_coeff()
        # Set Other Fields
        self.age = 0
        self.x_thrust = 0
        self.y_thrust = 0
        self.x_force = 0
        self.y_force = 0
        self.x_shield = 0
        self.y_shield = 0
        self.d_const = 0
        self.i = 0
        self.j = 1
        self.bounce = 1
        self.clip = True
        self.color = WHITE

    def set_size(self, object_image):
        self.width = object_image.get_width()
        self.height = object_image.get_height()
        self.radius = sqrt(self.width * self.height / pi)

    def set_spawn(self):
        x_offset = random(int(self.width / 2), int(SCREEN_WIDTH - self.width / 2))
        y_offset = random(int(self.height / 2), int(SCREEN_HEIGHT - self.height / 2))
        return x_offset, y_offset

    def set_thrust(self):
        self.thrust = self.max_acc * self.max_vel * self.mass

    def set_drag_coeff(self):
        self.drag_coeff = self.thrust / self.max_vel

    def get_direction(self, target):
        i = target.x_pos - self.x_pos
        j = target.y_pos - self.y_pos
        r = sqrt(i ** 2 + j ** 2)
        if not (i == 0 and j == 0):
            i = i / r
            j = j / r
        return i, j, r

    def do_ability(self, items, space):
        pass

    def get_thrust(self, target, left, right, up, down):
        self.x_thrust = 0
        self.y_thrust = 0

    def do_physics(self, drag_const):
        self.age += TIME_STEP
        time_step_per_mass = TIME_STEP / (self.mass + 1e-10)  # Prevent Dividing by Zero
        self.x_vel = (self.x_vel + (self.x_thrust + self.x_force + self.x_shield) * time_step_per_mass) / \
                     (1 + (drag_const + self.drag_coeff) * time_step_per_mass)
        self.y_vel = (self.y_vel + (self.y_thrust + self.y_force + self.y_shield) * time_step_per_mass) / \
                     (1 + (drag_const + self.drag_coeff) * time_step_per_mass)

    def move(self):
        self.x_pos += self.x_vel * TIME_STEP
        if self.x_pos - self.width / 2 < 0:
            if self.clip:
                self.x_pos += SCREEN_WIDTH
            else:
                self.x_pos = self.width / 2
                self.x_vel *= -self.bounce
        elif self.x_pos + self.width / 2 > SCREEN_WIDTH:
            if self.clip:
                self.x_pos -= SCREEN_WIDTH
            else:
                self.x_pos = SCREEN_WIDTH - self.width / 2
                self.x_vel *= -self.bounce
        self.y_pos += self.y_vel * TIME_STEP
        if self.y_pos - self.height / 2 < 0:
            if self.clip:
                self.y_pos += SCREEN_HEIGHT
            else:
                self.y_pos = self.height / 2
                self.y_vel *= -self.bounce
        elif self.y_pos + self.height / 2 > SCREEN_HEIGHT:
            if self.clip:
                self.y_pos -= SCREEN_HEIGHT
            else:
                self.y_pos = SCREEN_HEIGHT - self.height / 2
                self.y_vel *= -self.bounce

    def get_hits(self, items, del_indexes):
        return items, del_indexes

    def draw(self):
        game().blit(self.image, (self.x_pos - self.height / 2, SCREEN_HEIGHT - (self.y_pos + self.height / 2)))

    def destroy(self):
        DESTROY_SOUND.play()


class Player(Movable):
    def __init__(self):
        image = PLAYER_IMAGE
        x_offset = SCREEN_WIDTH / 2
        y_offset = SCREEN_HEIGHT / 2
        x_vel = 0
        y_vel = 0
        mass = 100
        max_vel = PLAYER_VEL
        max_acc = PLAYER_ACC
        charge = 0
        fuel = 300
        super().__init__(image, x_offset, y_offset, x_vel, y_vel, mass, max_vel, max_acc, charge, fuel)
        self.clip = False
        self.discharge = False
        self.shields_discharge_rate = SHIELDS_DISCHARGE_RATE
        self.shields_radius = 500 * SCREEN_SCALE
        self.g_const = G_CONSTANT
        self.ability = 0

    def do_ability(self, items, space):
        self.x_shield = 0
        self.y_shield = 0
        drag_const = 0
        if space and self.charge > 0:
            self.discharge = True
            self.charge -= self.shields_discharge_rate * TIME_STEP
            if self.charge < 0:
                self.charge = 0
            if self.ability == 0:
                drag_const = 100
            else:
                self.shields_force(items)
        else:
            self.discharge = False
            drag_const = 0
            for item in items:
                item.x_shield = 0
                item.y_shield = 0
        return drag_const

    def shields_force(self, items):
        for item in items:
            if not (self is item):
                i, j, r = self.get_direction(item)
                if r < self.shields_radius:
                    x_shield = self.g_const * i * item.mass / r ** 2
                    y_shield = self.g_const * j * item.mass / r ** 2
                    item.x_shield = x_shield
                    item.y_shield = y_shield
                    self.x_shield -= x_shield
                    self.y_shield -= y_shield
                else:
                    item.x_shield = 0
                    item.y_shield = 0

    def get_thrust(self, target, left, right, up, down):
        if left:
            i = -1
        elif right:
            i = 1
        else:
            i = 0
        if down:
            j = -1
        elif up:
            j = 1
        else:
            j = 0
        if self.fuel > 0 and (i**2+j**2) > 0:
            self.fuel -= TIME_STEP
            if self.fuel < 0:
                self.fuel = 0
            self.x_thrust = i * self.thrust
            self.y_thrust = j * self.thrust
        else:
            self.x_thrust = 0
            self.y_thrust = 0

    def get_hits(self, items, del_indexes):
        for k, bullet in enumerate(items):
            if not(isinstance(bullet, Player)) and not(isinstance(bullet, Enemy)):
                i, j, r = self.get_direction(bullet)
                if r < self.radius + bullet.radius:
                    if (bullet.charge > 0 and self.charge == 100) or (bullet.mass < 0 and self.mass == 100):
                        pass
                    else:
                        if bullet.charge > 0:
                            self.charge += bullet.charge
                            if self.charge > 100:
                                self.charge = 100
                        else:
                            self.mass -= bullet.mass
                            if self.mass > 100:
                                self.mass = 100
                            elif self.mass < 0:
                                self.mass = 0
                        print(f'Bullet {k} hit ship {self}!')
                        bullet.destroy()
                        del_indexes.append(k)
            elif bullet is self:
                self_index = k
        if self.mass <= 0:
            print(f'{self} destroyed!')
            self.destroy()
            del_indexes.append(self_index)
        return items, del_indexes

    def draw(self):
        super().draw()
        if self.discharge:
            SHIELDS_SOUND.play()
            shield_brightness = int(self.charge * 2.55)
            if self.ability == 0:
                pygame.draw.circle(game(), (0, 0, shield_brightness),
                                   (self.x_pos, SCREEN_HEIGHT - self.y_pos), 3*self.radius, 10)
            else:
                pygame.draw.circle(game(), (shield_brightness, shield_brightness, 0),
                                   (self.x_pos, SCREEN_HEIGHT - self.y_pos), 3 * self.radius, 10)


class Enemy(Movable):
    def __init__(self, mass=20):
        image = ENEMY_IMAGE
        self.set_size(image)
        x_offset, y_offset = self.set_spawn()
        x_vel = 0
        y_vel = 0
        mass = mass
        max_vel = ENEMY_VEL
        max_acc = ENEMY_ACC
        charge = 0
        fuel = 300
        super().__init__(image, x_offset, y_offset, x_vel, y_vel, mass, max_vel, max_acc, charge, fuel)
        self.clip = False
        self.skill = 100
        self.shields_radius = 1.5 * self.radius
        self.g_const = G_CONSTANT

    def do_ability(self, items, space):
        self.x_force = 0
        self.y_force = 0
        for item in items:
            if isinstance(item, Player):
                self.shields_force([item])

    def shields_force(self, items):
        for item in items:
            if not (self is item):
                i, j, r = self.get_direction(item)
                if r < self.shields_radius:
                    x_force = self.g_const * i * item.mass / r ** 2
                    y_force = self.g_const * j * item.mass / r ** 2
                    item.x_force = x_force
                    item.y_force = y_force
                    self.x_force -= x_force
                    self.y_force -= y_force
                else:
                    item.x_force = 0
                    item.y_force = 0

    def get_thrust(self, target, left, right, up, down):
        if self.fuel > TIME_STEP:
            self.fuel -= TIME_STEP
            if self.fuel < 0:
                self.fuel = 0
            i, j, r = self.get_direction(target)
            self.x_thrust = i * self.thrust
            self.y_thrust = j * self.thrust
        else:
            self.x_thrust = 0
            self.y_thrust = 0

    def get_hits(self, items, del_indexes):
        for k, bullet in enumerate(items):
            if isinstance(bullet, Cannon) or isinstance(bullet, Rocket) or isinstance(bullet, Missile):
                i, j, r = self.get_direction(bullet)
                if bullet.check_hits:
                    if r < self.radius + bullet.radius:
                        self.mass -= bullet.mass
                        if self.mass < 0:
                            self.mass = 0
                        print(f'Bullet {k} hit ship {self}!')
                        bullet.destroy()
                        del_indexes.append(k)
                else:
                    if r > self.radius + bullet.radius:
                        bullet.check_hits = True
            elif bullet is self:
                self_index = k
        if self.mass <= 0:
            print(f'{self} destroyed!')
            self.destroy()
            del_indexes.append(self_index)
        return items, del_indexes

    def destroy(self):
        DESTROY_SOUND.play()


class Projectile(Movable):
    def __init__(self, target, creator, image, x_offset, y_offset, x_vel, y_vel, mass, max_vel, max_acc, charge, fuel):
        self.target = target
        self.creator = creator
        super().__init__(image, x_offset, y_offset, x_vel, y_vel, mass, max_vel, max_acc, charge, fuel)
        self.launch = False
        self.check_hits = False
        self.guess = 0.1
        self.init_vel = None
        # Get Implicit Properties
        self.skill = 0
        self.set_skill(creator)

    def aim(self, target):
        def residual(time, dist, u, v, init_vel, mass, drag, thrust):
            res = thrust / drag * (1 + mass / (drag * time) * (exp(-time * drag / mass) - 1)) + \
                  init_vel * mass / (drag * time) * (1 - exp(-time * drag / mass)) - \
                  sqrt(u ** 2 + (v + dist / time) ** 2)
            return res
        dx = target.x_pos - self.x_pos
        dy = target.y_pos - self.y_pos
        d = sqrt(dx * dx + dy * dy)
        alpha = atan2(dy, dx)
        i = dx / d
        j = dy / d
        x_vel = target.x_vel - self.x_vel
        y_vel = target.y_vel - self.y_vel
        vx = x_vel * i + y_vel * j
        vy = x_vel * j - y_vel * i
        tol = 1e-6
        t = self.guess
        for k in range(25):
            r = residual(t, d, vx, vy, self.init_vel, self.mass, self.drag_coeff, self.thrust)
            rn = residual(t + tol, d, vx, vy, self.init_vel, self.mass, self.drag_coeff, self.thrust)
            if rn - r != 0:
                dx = - r * tol / (rn - r)
            else:
                print('Dividing by zero????')
                beta = 0
                break
            t = t + dx
            if t <= 0:
                t = tol
            elif t > 10:
                t = 10
            if abs(dx) < tol:
                beta = atan2(vy, vx + d / t)
                break
        else:
            print('Cannot Aim???')
            beta = 0
        self.guess = t
        theta = alpha - self.skill / 100 * beta
        self.i = cos(theta)
        self.j = sin(theta)

    def set_skill(self, creator):
        self.skill = creator.skill + SKILL_SPREAD * random(-creator.skill, 100 - creator.skill)


class Cannon(Projectile):
    def __init__(self, target, creator):
        image = CANNON_IMAGE
        x_offset = creator.x_pos
        y_offset = creator.y_pos
        x_vel = 0
        y_vel = 0
        mass = CANNON_MASS
        max_vel = CANNON_VEL
        max_acc = CANNON_ACC
        charge = 0
        fuel = 0
        super().__init__(target, creator, image, x_offset, y_offset, x_vel, y_vel, mass, max_vel, max_acc, charge, fuel)
        print(self.skill)
        self.delay = 0
        self.init_vel = CANNON_VEL
        self.aim(target)
        self.x_vel = self.i * self.init_vel
        self.y_vel = self.j * self.init_vel
        CANNON_SOUND.play()

    def get_thrust(self, target, left, right, up, down):
        self.x_thrust = 0
        self.y_thrust = 0

    def destroy(self):
        CANNON_HIT_SOUND.play()
        game().blit(CANNON_EXPLOSION_IMAGE, (self.x_pos - self.height / 2, SCREEN_HEIGHT -
                                             (self.y_pos + self.height / 2)))
        pygame.display.update()


class Rocket(Projectile):
    def __init__(self, target, creator):
        image = ROCKET_IMAGE
        x_offset = creator.x_pos
        y_offset = creator.y_pos
        x_vel = 1.5 * creator.x_vel
        y_vel = 1.5 * creator.y_vel
        mass = ROCKET_MASS
        max_vel = ROCKET_VEL
        max_acc = ROCKET_ACC
        charge = 0
        fuel = 0.25
        super().__init__(target, creator, image, x_offset, y_offset, x_vel, y_vel, mass, max_vel, max_acc, charge, fuel)
        self.delay = 0
        self.init_vel = 0
        self.aim(target)
        ROCKET_SOUND.play()

    def get_thrust(self, target, left, right, up, down):
        if self.fuel > 0 and self.age >= self.delay:
            self.fuel -= TIME_STEP
            if self.fuel < 0:
                self.fuel = 0
            self.x_thrust = self.i * self.thrust
            self.y_thrust = self.j * self.thrust
        else:
            self.x_thrust = 0
            self.y_thrust = 0

    def draw(self):
        if sqrt(self.x_thrust ** 2 + self.y_thrust ** 2) > 0:
            rotated_image = self.image.copy()
        else:
            rotated_image = ROCKET_IMAGE_NO_THRUST.copy()
        angle = 180/3.14159*atan2(self.j, self.i) - 90
        rotated_image = pygame.transform.rotate(rotated_image, angle)
        game().blit(rotated_image, (self.x_pos - self.height / 2, SCREEN_HEIGHT - (self.y_pos + self.height / 2)))

    def destroy(self):
        CANNON_HIT_SOUND.play()
        game().blit(ROCKET_EXPLOSION_IMAGE, (self.x_pos - self.height / 2, SCREEN_HEIGHT -
                                             (self.y_pos + self.height / 2)))
        pygame.display.update()


class Missile(Projectile):
    def __init__(self, target, creator):
        image = MISSILE_IMAGE
        x_offset = creator.x_pos
        y_offset = creator.y_pos
        x_vel = 0
        y_vel = 0
        mass = MISSILE_MASS
        max_vel = MISSILE_VEL
        max_acc = MISSILE_ACC
        charge = 0
        fuel = 10
        super().__init__(target, creator, image, x_offset, y_offset, x_vel, y_vel, mass, max_vel, max_acc, charge, fuel)
        self.delay = 1
        self.init_vel = 0
        MISSILE_SOUND.play()

    def get_thrust(self, target, left, right, up, down):
        if self.fuel > TIME_STEP and self.age >= self.delay:
            self.fuel -= TIME_STEP
            if self.fuel < 0:
                self.fuel = 0
            self.aim(target)
            self.x_thrust = self.i * self.thrust
            self.y_thrust = self.j * self.thrust
        else:
            self.x_thrust = 0
            self.y_thrust = 0

    def draw(self):
        if sqrt(self.x_thrust ** 2 + self.y_thrust ** 2) > 0:
            rotated_image = self.image.copy()
        else:
            rotated_image = MISSILE_IMAGE_NO_THRUST.copy()
        angle = 180/3.14159*atan2(self.j, self.i) - 90
        rotated_image = pygame.transform.rotate(rotated_image, angle)
        game().blit(rotated_image, (self.x_pos - self.height / 2, SCREEN_HEIGHT - (self.y_pos + self.height / 2)))

    def destroy(self):
        CANNON_HIT_SOUND.play()
        game().blit(MISSILE_EXPLOSION_IMAGE, (self.x_pos - self.height / 2, SCREEN_HEIGHT -
                                              (self.y_pos + self.height / 2)))
        pygame.display.update()


class PowerUp(Movable):
    def __init__(self, image, x_offset, y_offset, x_vel, y_vel, mass, max_vel, max_acc, charge, fuel):
        super().__init__(image, x_offset, y_offset, x_vel, y_vel, mass, max_vel, max_acc, charge, fuel)
        self.check_hits = True


class Health(PowerUp):
    def __init__(self):
        image = HEALTH_IMAGE
        self.set_size(image)
        x_offset, y_offset = self.set_spawn()
        x_vel = 0
        y_vel = 0
        mass = HEALTH_MASS
        max_vel = PLAYER_VEL
        max_acc = PLAYER_ACC
        charge = 0
        fuel = 0
        super().__init__(image, x_offset, y_offset, x_vel, y_vel, mass, max_vel, max_acc, charge, fuel)

    def destroy(self):
        HEALTH_PICKUP_SOUND.play()


class Shields(PowerUp):
    def __init__(self):
        image = SHIELDS_IMAGE
        self.set_size(image)
        x_offset, y_offset = self.set_spawn()
        x_vel = 0
        y_vel = 0
        mass = SHIELDS_MASS
        max_vel = PLAYER_VEL
        max_acc = PLAYER_ACC
        charge = 25
        fuel = 0
        super().__init__(image, x_offset, y_offset, x_vel, y_vel, mass, max_vel, max_acc, charge, fuel)

    def destroy(self):
        SHIELDS_PICKUP_SOUND.play()


class Dampers(PowerUp):
    def __init__(self):
        image = DAMPERS_IMAGE
        self.set_size(image)
        x_offset, y_offset = self.set_spawn()
        x_vel = 0
        y_vel = 0
        mass = DAMPERS_MASS
        max_vel = PLAYER_VEL
        max_acc = PLAYER_ACC
        charge = 100
        fuel = 0
        super().__init__(image, x_offset, y_offset, x_vel, y_vel, mass, max_vel, max_acc, charge, fuel)

    def destroy(self):
        SHIELDS_PICKUP_SOUND.play()
