import torch
import torch.nn as nn
import torch.nn.functional as F
from neuralop.models import FNO3d

class GINO_Simulator(nn.Module):
    def __init__(self, in_channels=3, out_channels=4, latent_dim=64, grid_size=64):
        super().__init__()
        
        # 1. GNN ENCODER (The "Geometry Handler")
        # Takes (x,y,z) + boundary_flags -> Latent Embedding
        # We use a Graph Neural Operator (GNO) layer here for resolution independence
        self.gnn_encoder = GNO_Layer(in_channels=in_channels, out_channels=latent_dim, radius=0.05)
        
        # 2. FNO PROCESSOR (The "Physics Engine")
        # Operates on the Latent Grid (e.g., 64x64x64 voxel latent space)
        self.fno_processor = FNO3d(
            n_modes_height=16, n_modes_width=16, n_modes_depth=16,
            hidden_channels=latent_dim, 
            in_channels=latent_dim, 
            out_channels=latent_dim
        )
        
        # 3. GNN DECODER (The "Detail Refiner")
        # Projects latent physics back to the original mesh topology
        self.gnn_decoder = GNO_Layer(in_channels=latent_dim, out_channels=out_channels, radius=0.05)

    def forward(self, input_graph, latent_grid_coords):
        """
        input_graph: The irregular mesh from your Silver Layer (HDF5)
        latent_grid_coords: A fixed uniform grid to project onto
        """
        
        # Step A: Encode Irregular Mesh -> Latent Features
        x = self.gnn_encoder(input_graph.x, input_graph.edge_index)
        
        # Step B: Interpolate to Uniform Grid (The "Bridge")
        # We map the graph nodes to the nearest latent grid points
        x_grid = map_to_grid(x, input_graph.pos, latent_grid_coords)
        
        # Step C: Solve Physics in Frequency Domain
        x_grid = self.fno_processor(x_grid)
        
        # Step D: Interpolate back to Mesh
        x_physics = map_from_grid(x_grid, latent_grid_coords, input_graph.pos)
        
        # Step E: Final Refinement
        output_fields = self.gnn_decoder(x_physics, input_graph.edge_index)
        
        return output_fields # (Pressure, Velocity X, Y, Z)
