from PythonClientAPI.game.PointUtils import *
from PythonClientAPI.game.Entities import FriendlyUnit, EnemyUnit, Tile
from PythonClientAPI.game.Enums import Team
from PythonClientAPI.game.World import World
from PythonClientAPI.game.TileUtils import TileUtils


class PlayerAI:

    def __init__(self):
        ''' Initialize! '''
        self.turn_count = 0  # game turn count
        self.target = None  # target to send unit to!
        self.outbound = True  # is the unit leaving, or returning?
        self.prev_pos = (0, 0)

    def do_move(self, world, friendly_unit, enemy_units):
        '''
        This method is called every turn by the game engine.
        Make sure you call friendly_unit.move(target) somewhere here!

        Below, you'll find a very rudimentary strategy to get you started.
        Feel free to use, or delete any part of the provided code - Good luck!

        :param world: world object (more information on the documentation)
            - world: contains information about the game map.
            - world.path: contains various pathfinding helper methods.
            - world.util: contains various tile-finding helper methods.
            - world.fill: contains various flood-filling helper methods.

        :param friendly_unit: FriendlyUnit object
        :param enemy_units: list of EnemyUnit objects
        '''

        # Initialize Parameters

        snek = friendly_unit.snake
        snek_head = friendly_unit.position

        enemy_snek_heads = []
        for unit in enemy_units:
            enemy_snek_heads.append(unit.position)

        # increment turn count
        self.turn_count += 1

        # DO NOT EDIT
        # if unit is dead, stop making moves.
        if friendly_unit.status == 'DISABLED':
            print("Turn {0}: Disabled - skipping move.".format(str(self.turn_count)))
            self.target = None
            self.outbound = True
            return

        # if unit reaches the target point, reverse outbound boolean and set target back to None
        if self.target is not None and friendly_unit.position == self.target.position:
            #  self.outbound = not self.outbound (we still want it to be outbound)
            self.target = None

        '''#if outbound and no target set, set target as the closest capturable tile at least 2 tile away from your territory's edge.
        if (world.position_to_tile_map[snek_head]).is_friendly:  # only happens if we are in friendly territory
            if self.outbound and self.target is None:
                edges = [tile for tile in world.util.get_friendly_territory_edges()]
                avoid = []
                first = []
                for edge in edges:
                    avoid += [pos for pos in world.get_neighbours(edge.position).values]
                    first = avoid
                    for poss in first:
                        avoid += [poss for poss in world.get_neighbours(poss).values]
                self.target = world.util.get_closest_capturable_territory_from(friendly_unit.position, avoid)'''

        if (world.position_to_tile_map[snek_head]).is_friendly:
            if self.outbound and self.target is None:
                edges = [tile for tile in world.util.get_friendly_territory_edges()]
                avoid = []
                for edge in edges:
                    avoid += [pos for pos in world.get_neighbours(edge.position).values()]
                self.target = world.util.get_closest_capturable_territory_from(friendly_unit.position, avoid)


        # Choose the direction upon reaching target based on previous movement and position on map
        if self.target is None:
            change = sub_points(snek_head, self.prev_pos)

            # east west
            if (change[0]==0):
                if snek_head[0] <= 14:
                    self.target = world.position_to_tile_map[(snek_head[0] + 6, snek_head[1])]  # PLACEHOLDER VALUE (6)
                else:
                    self.target = world.position_to_tile_map[(snek_head[0] - 6, snek_head[1])]

                # north south
            if change[1]==0 :
                if snek_head[1] <= 14:
                    self.target = world.position_to_tile_map[(snek_head[0], snek_head[1] + 6)]
                else:
                    self.target = world.position_to_tile_map[(snek_head[0], snek_head[1] - 6)]

                # if the steps required to return to the nearest friendly territory is only 2 steps more than the steps required for an enemy to reach our body,
        # return to then nearest friendly edge

        closest_friendly_tile = world.util.get_closest_friendly_territory_from(snek_head,snek)

        # number of steps to reach friendly edge
        r = world.path.get_shortest_path_distance(snek_head, closest_friendly_tile.position)

        # number of steps to reach body; start with artribrarily large number that will be replaced
        c = 1000000

        # find shortest distance between enemy head and body points
        for point in snek:
            for head in enemy_snek_heads:
                distance = world.path.get_shortest_path_distance(point, head)
                if distance < c:
                    c = distance

        if r >= c - 3:
            self.outbound = False  # enemy sneks are too close so we dipping back home
            self.target = None

            # else if inbound and no target set, set target as the closest friendly tile
        if not self.outbound and self.target is None:
            self.target = world.util.get_closest_friendly_territory_from(friendly_unit.position, snek)

        # set next move as the next point in the path to target
        next_move = world.path.get_shortest_path(friendly_unit.position, self.target.position, friendly_unit.snake)[0]

        # update previous position
        self.prev_pos = snek_head
        # move!
        friendly_unit.move(next_move)
        print("Turn {0}: currently at {1}, making {2} move to {3}.".format(
            str(self.turn_count),
            str(friendly_unit.position),
            'outbound' if self.outbound else 'inbound',
            str(self.target.position)
        ))







