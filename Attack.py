
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np

from supremacy import helpers

# This is your team name
CREATOR = "FarmerAI"


# def tank_ai(tank, info, game_map):
#     """
#     Function to control tanks.
#     """
#     if not tank.stopped:
#         if tank.stuck:
#             tank.set_heading(np.random.random() * 360.0)
#         elif "target" in info:
#             tank.goto(*info["target"])


# def ship_ai(ship, info, game_map):
#     """
#     Function to control ships.
#     """
#     if not ship.stopped:
#         if ship.stuck:
#             if ship.get_distance(ship.owner.x, ship.owner.y) > 20:
#                 ship.convert_to_base()
#             else:
#                 ship.set_heading(np.random.random() * 360.0)


# def jet_ai(jet, info, game_map):
#     """
#     Function to control jets.
#     """
#     if "target" in info:
#         jet.goto(*info["target"])


class PlayerAi:
    """
    This is the AI bot that will be instantiated for the competition.
    """

    def __init__(self):
        self.team = CREATOR  # Mandatory attribute
        self.build_queue = helpers.BuildQueue(
            ["mine", "tank", "ship", "jet"], cycle=True
        )
        self.ntanks = {}
        self.nships = {}

    def run(self, t: float, dt: float, info: dict, game_map: np.ndarray):
        """
        This is the main function that will be called by the game engine.
        """
        
        # Get information about my team
        myinfo = info[self.team]

        # Iterate through all my bases and process build queue
        for base in myinfo["bases"]:
            # Calling the build_queue will return the object that was built by the base.
            # It will return None if the base did not have enough resources to build.
            # obj = self.build_queue(base)
            # print(base.cost("mine"))

            # Bookkeeping
            uid = base.uid
            if uid not in self.ntanks:
                self.ntanks[uid] = 0
                self.nships[uid] = 0

            # Build things
            if base.mines < 2:
                if base.crystal > base.cost("mine"):
                    base.build_mine()
            # If we have enough mines, pick something at random
            else:
                if self.nships[uid] < 3:
                    if base.crystal > base.cost("ship"):
                        ship = base.build_ship(heading=360 * np.random.random())
                        self.nships[uid] += 1
                elif self.ntanks[uid] < 5:
                    if base.crystal > base.cost("tank"):
                        tank = base.build_tank(heading=360 * np.random.random())
                        self.ntanks[uid] += 1
                elif base.crystal > base.cost("jet"):
                    jet = base.build_jet(heading=360 * np.random.random())

        # Let ship build bases only if no other base is close by
        # Iterate through all my ships
        if "ships" in myinfo:
            for ship in myinfo["ships"]:
                if not ship.stopped:
                    # If the ship position is the same as the previous position,
                    # convert the ship to a base if it is far from the owning base,
                    # set a random heading otherwise
                    if ship.stuck:
                        base_nearby=False
                        for base in myinfo["bases"]:
                            if ship.get_distance(base.x, base.y) <= 40:
                                base_nearby=True

                        if not base_nearby:
                            #print("Convert Ship")
                            ship.convert_to_base()
                        else:
                            #print("else")
                            ship.set_heading(np.random.random() * 360.0)


        # Try to find an enemy target
        target = None
        # If there are multiple teams in the info, find the first team that is not mine
        if len(info) > 1:
            for name in info:
                if name != self.team:
                    # Target only bases
                    if "base" in info[name]:
                        t = info[name]["base"][0]
                        # dist = np.zeros((len("jets")))
                        # for i,jet in enumerate("jets"):
                        #     dist[i] = jet.get_distance(base[])

                        # Simply target the first jet
                        target = [t.x, t.y]
            


        # Iterate through all my tanks
        if "tanks" in myinfo:
            for tank in myinfo["tanks"]:
                if not tank.stopped:
                    # If the tank position is the same as the previous position,
                    # set a random heading
                    if tank.stuck:
                        tank.set_heading(np.random.random() * 360.0)
                    # Else, if there is a target, go to the target
                    elif tank.get_distance(tank.owner.x, tank.owner.y) >= 5:
                        tank.stop()

        # # Iterate through all my jets
        # if "jets" in myinfo:
        #     for jet in myinfo["jets"]:
        #         # Jets simply go to the target if there is one, they never get stuck
        #         if target is not None:
        #             jet.goto(*target)

        # Iterate through all my jets
        if "jets" in myinfo:
            for jet in myinfo["jets"]:
               localtarget = None
               if len(info) > 1:
                for name in info:
                    if name != self.team:
                        # Target bases in certain distance
                        if "bases" in info[name]:
                            t = info[name]["bases"][0]
                            for base in info[name]["bases"]:
                                if jet.get_distance(t.x,t.y) > jet.get_distance(base.x,base.y):
                                    t = base
                                localtarget = [t.x,t.y]
                                if localtarget is not None:
                                    jet.goto(*localtarget)

        
        # Control all my vehicles
        # helpers.control_vehicles(
        #     info=myinfo, game_map=game_map, tank=tank_ai, ship=ship_ai, jet=jet_ai
        # )

