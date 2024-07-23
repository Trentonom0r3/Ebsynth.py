import os
import sys

# import numpy as np
# import tqdm

import gc
import torch


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ezsynth.aux_run import run_scratch
from ezsynth.utils.flow_utils.OpticalFlow import RAFT_flow

from ezsynth.aux_computations import precompute_edge_guides
from ezsynth.aux_utils import (
    extract_indices,
    read_frames_from_paths,
    save_seq,
    setup_src_from_folder,
    validate_file_or_folder_to_lst,
)
from ezsynth.aux_classes import RunConfig
from ezsynth.utils.sequences import SequenceManager
from ezsynth.utils._ebsynth import ebsynth

style_paths = [
    # "J:/AI/Ezsynth/examples/styles/style000.png",
    "J:/AI/Ezsynth/examples/styles/style002.png",
    # "J:/AI/Ezsynth/examples/styles/style003.png",
    # "J:/AI/Ezsynth/examples/styles/style006.png",
    # "J:/AI/Ezsynth/examples/styles/style014.png",
    # "J:/AI/Ezsynth/examples/styles/style019.png",
    # "J:/AI/Ezsynth/examples/styles/style099.jpg",
]

image_folder = "J:/AI/Ezsynth/examples/input"
output_folder = "J:/AI/Ezsynth/output"

# edge_method="Classic",
edge_method = "PAGE"
# edge_method="PST",
flow_method = "RAFT"
model = "sintel"

img_file_paths, img_idxes, img_frs_seq = setup_src_from_folder(image_folder)
style_paths = validate_file_or_folder_to_lst(style_paths, "style")

style_idxes = extract_indices(style_paths)
num_style_frs = len(style_paths)
style_frs = read_frames_from_paths(style_paths)

manager = SequenceManager(
    img_idxes[0],
    img_idxes[-1],
    style_paths,
    style_idxes,
    img_idxes,
)

sequences = manager.create_sequences()

edge_guides = precompute_edge_guides(
    img_frs_seq, edge_method
)

stylized_frames = []

rafter = RAFT_flow(model_name="sintel")

cfg = RunConfig()

eb = ebsynth(**cfg.get_ebsynth_cfg())
eb.runner.initialize_libebsynth()

tmp_stylized_frames, err_list, flows, poses = run_scratch(
    sequences[0], img_frs_seq, style_frs, edge_guides, RunConfig(), rafter, eb
)

save_seq(tmp_stylized_frames, "J:/AI/Ezsynth/output_0")

# stylized_frames.extend(tmp_stylized_frames)

tmp_stylized_frames, err_list, flows, poses = run_scratch(
    sequences[1], img_frs_seq, style_frs, edge_guides, RunConfig(), rafter, eb
)

save_seq(tmp_stylized_frames, "J:/AI/Ezsynth/output_1")

# tmp_stylized_frames, err_list, flows, poses = run_scratch(
#     sequences[1], img_frs_seq, style_frs, edge_guides, RunConfig()
# )

# save_seq(tmp_stylized_frames, "J:/AI/Ezsynth/output_2")

gc.collect()
torch.cuda.empty_cache()

# tmp_stylized_frames, err_list, flows, poses = run_scratch(
#     sequences[1], img_frs_seq, style_frs, edge_guides, RunConfig()
# )

# save_seq(tmp_stylized_frames, "J:/AI/Ezsynth/output_1")

# stylized_frames.extend(tmp_stylized_frames)

# print(len(stylized_frames))

# save_seq(stylized_frames, output_folder)