from argparse import ArgumentParser, Namespace
import time

import numpy as np

import polyscope as ps
import polyscope.imgui as psim

from utils.gui_utils import state_button
from utils.ps_utils import create_bbox


class Viewer:

    def __init__(
        self,
        args: Namespace,
    ) -> None:

        self.n_points = args.n_points
        self.n_steps = args.n_steps

        self.training = False

        # -----------------------
        # Init polyscope
        # -----------------------

        ps.init()
        self.ps_init()

        # -----------------------
        # Init components
        # -----------------------

        self.create_point_cloud_sequence()

        # -----------------------
        # Start polyscope
        # -----------------------

        ps.set_user_callback(self.ps_callback)
        ps.show()

    def ps_init(self) -> None:
        """
        Initialize Polyscope
        """
        ps.set_ground_plane_mode("none")
        ps.set_max_fps(120)
        ps.set_window_size(1080, 1080)
        # Anti-aliasing
        ps.set_SSAA_factor(4)
        # Uncomment to prevent polyscope from changing scales (including Gizmo!)
        # ps.set_automatically_compute_scene_extents(False)

        # Just a toy bounding
        create_bbox()

        self.window_size = ps.get_window_size()

        self.last_time = time.time()

    # `ps_callback` is called every frame by polyscope
    def ps_callback(self) -> None:

        # Update fps count
        new_time = time.time()
        self.fps = 1.0 / (new_time - self.last_time)
        self.last_time = new_time

        # I usually put all my guy stuff in another function
        self.gui()

        # I usually draw things in a draw function (e.g., rendering buffer)
        self.draw()

    def gui(self) -> None:
        psim.Text(f"fps: {self.fps:.4f};")

        # Just an example of a button with a different displayed state depending on the value
        clicked, self.training = state_button(
            self.training, "Stop##viewer", "Train##viewer"
        )
        if clicked:
            # Do something
            pass

        # Click to re-create the point cloud sequence
        if psim.Button("New Sequence"):
            self.create_point_cloud_sequence()

        # A slider to change the current point cloud
        clicked, self.current_pc = psim.SliderInt(
            "Point cloud", self.current_pc, v_min=0, v_max=len(self.pc_sequence) - 1
        )
        if clicked:
            self.update_point_cloud()

    def draw(self) -> None:
        # TODO: give an example with render buffers
        pass

    def create_point_cloud_sequence(self) -> None:
        point_cloud = np.random.normal(size=(self.n_points, 3))
        self.pc_sequence = [
            point_cloud * (1 - scale) for scale in np.linspace(0, 1, self.n_steps)
        ]
        self.current_pc: int = 0
        self.update_point_cloud()

    def update_point_cloud(self) -> None:
        assert self.current_pc < len(self.pc_sequence)
        polyscope_pc = ps.register_point_cloud(
            "point cloud", self.pc_sequence[self.current_pc]
        )
        # You can also set colors on the points, etc.
        # polyscope_pc.add_color_quantity(...)


def main(args):

    Viewer(args)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--n_points", type=int, default=1000)
    parser.add_argument("--n_steps", type=int, default=100)
    args = parser.parse_args()

    main(args)
