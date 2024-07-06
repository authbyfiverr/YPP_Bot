import agentWindow
import swordfight
import agentVision
import time

if __name__ == '__main__':
    # agentWindow.create_window(update_interval=1)
    time.sleep(2)
    targets_sf = agentVision.load_target_images_from_folder('targets_sf')
    screenshot = agentVision.crop_screenshot_to_ypp(agentVision.take_screenshot())
    found_targets = agentVision.find_all_targets_on_screenshot(targets_sf['green.png'], screenshot, threshold=0.75, center=True)
    swordfight.add_dots_and_save_2(screenshot, found_targets)
    #gameboard = swordfight.sample_pixels_around_centers(screenshot, swordfight.sf_tile_x_coords, swordfight.sf_tile_y_coords)

    #swordfight.print_sampled_values_grid(gameboard, swordfight.sf_tile_x_coords, swordfight.sf_tile_y_coords)
    #swordfight.add_dots_and_save(screenshot, swordfight.sf_tile_x_coords, swordfight.sf_tile_y_coords)