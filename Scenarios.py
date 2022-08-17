from Objects import *


def one_vs_one():
    # Game Parameters
    cannon_phase = 1
    rocket_phase = 2
    missile_phase = 3
    health_phase = 2
    shield_phase = 3
    dampers_phase = 3
    cannon_chance = 20
    rocket_chance = 30
    missile_chance = 35
    health_chance = 40
    shields_chance = 45
    dampers_chance = 100
    max_cannons = 16
    max_rockets = 8
    max_missiles = 4
    max_healths = 1
    max_shields = 1
    max_dampers = 1

    # Initialize Objects
    items = []

    # Add One Player and One Enemy
    items.append(Player())
    player = items[0]

    drag_const = 0
    phase = 2
    t = 0
    loop = True
    while loop:
        t += TIME_STEP
        loop = get_quit_event()
        left, right, down, up, space, shields, dampers, esc, pause = keystrokes()
        if esc:
            return loop
        elif pause:
            pause_game()

        # Get Indexes of Items
        player_indexes = []
        enemy_indexes = []
        cannon_indexes = []
        rocket_indexes = []
        missile_indexes = []
        health_indexes = []
        shield_indexes = []
        dampers_indexes = []
        for k, item in enumerate(items):
            if isinstance(item, Player):
                player_indexes.append(k)
            elif isinstance(item, Enemy):
                enemy_indexes.append(k)
            elif isinstance(item, Cannon):
                cannon_indexes.append(k)
            elif isinstance(item, Rocket):
                rocket_indexes.append(k)
            elif isinstance(item, Missile):
                missile_indexes.append(k)
            elif isinstance(item, Health):
                health_indexes.append(k)
            elif isinstance(item, Shields):
                shield_indexes.append(k)
            elif isinstance(item, Dampers):
                dampers_indexes.append(k)

        # Check Win/Loss Condition
        if len(player_indexes) == 0:
            return end_game(1)
        elif len(enemy_indexes) == 0:
            if phase < 3 and t > 3:
                phase += 1
                if phase == 1:
                    items.append(Enemy(mass=5))
                elif phase == 2:
                    items.append(Enemy(mass=10))
                elif phase == 3:
                    items.append(Enemy(mass=20))
            elif phase == 3:
                return end_game(0)

        # Abilities
        for item in items:
            ability_output = item.do_ability(items, space)
            if not(ability_output is None):
                drag_const = ability_output

        # Player Thrust
        for item in items:
            item.get_thrust(player, left, right, up, down)

        # Physics
        for item in items:
            item.do_physics(drag_const)
            item.move()

        # Check Hits
        del_indexes = []
        for item in items:
            items, del_indexes = item.get_hits(items, del_indexes)

        # Spawn New Objects
        players = [items[k] for k in player_indexes]
        enemies = [items[k] for k in enemy_indexes]
        for enemy in enemies:
            rnd = random(0, 100*FPS)
            if rnd <= FPS:
                rnd = random(0, dampers_chance)
                if rnd < cannon_chance and phase >= cannon_phase and max_cannons > len(cannon_indexes):
                    items.append(Cannon(player, enemy))
                elif rnd < rocket_chance and phase >= rocket_phase and max_rockets > len(rocket_indexes):
                    items.append(Rocket(player, enemy))
                elif rnd < missile_chance and phase >= missile_phase and max_missiles > len(missile_indexes):
                    items.append(Missile(player, enemy))
                elif rnd < health_chance and phase >= health_phase and max_healths > len(health_indexes):
                    items.append(Health())
                elif rnd < shields_chance and phase >= shield_phase and max_shields > len(shield_indexes):
                    items.append(Shields())
                elif rnd < dampers_chance and phase >= dampers_phase and max_dampers > len(dampers_indexes):
                    items.append(Dampers())

        # Cycle Abilities
        if shields:
            items[player_indexes[0]].ability = 1
        if dampers:
            items[player_indexes[0]].ability = 0

        # Update Screen
        reset_screen()
        if len(enemies) == 0:
            enemy = Enemy()
            enemy.mass = 0
        else:
            enemy = enemies[0]
        display_stats(players[0], enemy)
        for item in reversed(items):
            item.draw()
        limit_fps()
        pygame.display.update()

        # Clean Up Casualties
        del_indexes.sort()
        del_indexes.reverse()
        if len(del_indexes) >= 1:
            for del_index in del_indexes:
                del items[del_index]


def test():
    loop = True
    while loop:
        loop = get_quit_event()
        reset_screen()
        limit_fps()
        pygame.display.update()
