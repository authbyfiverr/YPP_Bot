import agentVision

target_images = agentVision.target_images

class State:
    def __init__(self, state_name, target_image_list, substates=None):
        self.state_name = state_name
        self.target_image_list = target_image_list
        self.substates = substates if substates else []

    def state_target_match(self, screenshot):
        for target_image_path in self.target_image_list:
            if agentVision.find_target_on_screenshot(target_images[target_image_path], screenshot):
                return self.state_name
        return False

    def add_substate(self, substate):
        self.substates.append(substate)

class StateMachine:
    def __init__(self, root_state):
        self.root_state = root_state

    def determine_state(self, screenshot):
        state_hierarchy = []
        current_state = self.root_state
        while current_state:
            state_hierarchy.append(current_state.state_name)
            next_state = None
            for substate in current_state.substates:
                if substate.state_target_match(screenshot):
                    next_state = substate
                    break
            if not next_state:
                break
            current_state = next_state
        return state_hierarchy

ypp_sun_menu_at_sea = [
    #State('Vessel Tab', ['sunset_menu_vessel_tab_selected.png'], None),
]

ypp_sun_menu_on_land = [
    #State('Island Tab', ['sunset_menu_island_tab_selected.png'], None),
    #State('Shoppe Tab', ['sunset_menu_shoppe_tab_selected.png'], None),
    #State('House Tab', ['sunset_menu_house_tab_selected.png'], None),
]


ypp_rigging_performace = [
    State('Booched', ['rigging_bootched_performance_in_puzzle_icon.png'], None),
]

ypp_puzzling_states = [
    State('Rigging', ['rigging.png'], ypp_rigging_performace),
    State('Sword Fight', ['swordfight.png'], None),
    #State('Rumble', ['rumble.png'], None),
    State('Bilging', ['bilging.png'], None),
    State('Carp', ['carp.png'], None),
    State('Patching', ['patching.png'], None),
    State('Sailing', ['sailing.png'], None),
    #State('Gunning', ['gunning.png'], None),
    #State('Foraging', ['foraging.png'], None),
    State('Treasure Haul', ['treasure_haul.png'], None),
    #State('Duty Navigation', ['dutynav.png'], None)
]

ypp_notice_board_states = [
    State('News', ['notice_board_pirate_news.png'], None),
    State('Voyages', ['notice_board_voyages.png'], None),
    State('Missions', ['notice_board_missions.png'], None),
    State('Events', ['notice_board_events.png'], None),
    State('Shoppe Jobs', ['notice_board_featured_jobs.png'], None),
    State('Blockades', ['notice_board_blockades.png'], None)
]

ypp_in_game_states = [
    State('Notice Board', ['notice_board_title_text.png'], ypp_notice_board_states),
    State('In Battle', ['sea_battle_tile_1.png', 'sea_battle_tile_2.png'], ypp_puzzling_states + ypp_sun_menu_at_sea),

]

ypp_player_location_states = [
    State('At Sea', ['ship_at_sea_icon_under_map.png', 'island_icon_under_map.png'], ypp_in_game_states + ypp_puzzling_states + ypp_sun_menu_at_sea),
    State('On Land', ['island_ahoy_tab_selected.png', 'ypp_sundial_island.png'], ypp_in_game_states),
]

ypp_initial_states = [
    State('In-Game', ['puzzle_pirates_logo_in_game.png'], ypp_player_location_states),
    State('Login', ['login_logon_button.png'], None),
    State('Pirate Select', ['pirate_select_pick_yer_pirate_text.png'], None),
    State('Client Update', ['update_puzzle_for_treasure_text.png'], None)
]

ypp_state = State('', [], ypp_initial_states)


ypp_alerts = [
    State('Jobbing Invite', ['jobbing_invite.png'], None)
]

ypp_alerts_init_state = State('', [], ypp_alerts)

