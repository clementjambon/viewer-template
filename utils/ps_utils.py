import numpy as np
import polyscope as ps

# -----------------------------
# LISTS
# -----------------------------

CUBE_VERTICES_LIST = [
    [0.0, 0.0, 1.0],
    [1.0, 0.0, 1.0],
    [1.0, 1.0, 1.0],
    [0.0, 1.0, 1.0],
    [0.0, 0.0, 0.0],
    [1.0, 0.0, 0.0],
    [1.0, 1.0, 0.0],
    [0.0, 1.0, 0.0],
]

CUBE_EDGES_LIST = [
    [0, 1],  # 0
    [1, 2],  # 1
    [2, 3],  # 2
    [3, 0],  # 3
    [4, 5],  # 4
    [5, 6],  # 5
    [6, 7],  # 6
    [7, 4],  # 7
    [0, 4],  # 8
    [1, 5],  # 9
    [2, 6],  # 10
    [3, 7],  # 11
]

CUBE_TRIANGLES_LIST = [
    [0, 1, 2],
    [2, 3, 0],
    [6, 5, 4],
    [4, 7, 6],
    [5, 2, 1],
    [2, 5, 6],
    [0, 3, 4],
    [4, 3, 7],
    [2, 6, 3],
    [3, 6, 7],
    [0, 4, 1],
    [1, 4, 5],
]


# -----------------------------
# NUMPY
# -----------------------------

CUBE_VERTICES_NP = np.array(CUBE_VERTICES_LIST)
CUBE_EDGES_NP = np.array(CUBE_EDGES_LIST)


def create_bbox(
    bbox_min=np.array([-1.0, -1.0, -1.0]),
    bbox_max=np.array([1.0, 1.0, 1.0]),
    edge_radius: float = 0.005,
    suffix: str = "",
    enabled: bool = True,
):
    cube_vertices = (bbox_max - bbox_min) * CUBE_VERTICES_NP + bbox_min

    bbox = ps.register_curve_network(
        f"bbox{suffix}",
        cube_vertices,
        CUBE_EDGES_NP,
        enabled=enabled,
        radius=edge_radius,
    )
