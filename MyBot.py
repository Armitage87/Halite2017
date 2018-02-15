import hlt
import logging
from collections import OrderedDict


game = hlt.Game("T-Clap Aggressive")
logging.info("Starting T-Clap Aggressive")

while True:
    game_map = game.update_map()
    command_queue = []
    planets = game_map.all_planets()
    my_ships = game_map.get_me().all_ships()
    all_players = game_map.all_players()
    turns = 0
    for ship in my_ships:
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            continue

        entities_by_distance = game_map.nearby_entities_by_distance(ship)
        largest_planet = max(planet.radius for planet in game_map.all_planets())
        entities_by_distance = OrderedDict(sorted(entities_by_distance.items(), key=lambda t: t[0]))

        closest_empty_planets = [entities_by_distance[distance][0] for distance in entities_by_distance if
                                 isinstance(entities_by_distance[distance][0], hlt.entity.Planet) and not
                                 entities_by_distance[distance][0].is_owned()]

        closest_enemy_ships = [entities_by_distance[distance][0] for distance in entities_by_distance if
                               isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and
                               entities_by_distance[distance][0] not in my_ships]
        closest_my_ships = [entities_by_distance[distance][0] for distance in entities_by_distance if
                               isinstance(entities_by_distance[distance][0], hlt.entity.Ship) and
                               entities_by_distance[distance][0] in my_ships]
        logging.info(turns)
        if len(all_players) <= 2:
            if ship.id % 3 == 0 and len(closest_empty_planets) > 0:
                target_planet = closest_empty_planets[0]
                if ship.can_dock(target_planet):
                    command_queue.append(ship.dock(target_planet))
                else:
                    navigate_command = ship.navigate(
                        ship.closest_point_to(target_planet),
                        game_map,
                        speed=int(hlt.constants.MAX_SPEED),
                        ignore_ships=False, avoid_obstacles=True, max_corrections=18, angular_step=10)

                    if navigate_command:
                        command_queue.append(navigate_command)
            elif len(closest_enemy_ships) > 0:
                target_ship = closest_enemy_ships[0]
                navigate_command = ship.navigate(
                                ship.closest_point_to(target_ship),
                                game_map,
                                speed=int(hlt.constants.MAX_SPEED),
                                ignore_ships=False, avoid_obstacles=True, max_corrections=18, angular_step=10)

                if navigate_command:
                    command_queue.append(navigate_command)

        elif len(all_players) > 2 and len(closest_empty_planets) >= 1:
            target_planet = closest_empty_planets[0]
            if ship.can_dock(target_planet):
                command_queue.append(ship.dock(target_planet))
            else:
                navigate_command = ship.navigate(
                    ship.closest_point_to(target_planet),
                    game_map,
                    speed=int(hlt.constants.MAX_SPEED),
                    ignore_ships=False, avoid_obstacles=True, max_corrections=18, angular_step=10)

                if navigate_command:
                    command_queue.append(navigate_command)

        elif len(all_players) > 2 and len(closest_enemy_ships) > 0:
            target_ship = closest_enemy_ships[0]
            navigate_command = ship.navigate(
                ship.closest_point_to(target_ship),
                game_map,
                speed=int(hlt.constants.MAX_SPEED),
                ignore_ships=False, avoid_obstacles=True, max_corrections=18, angular_step=10)

            if navigate_command:
                command_queue.append(navigate_command)

    game.send_command_queue(command_queue)
    turns += 1






