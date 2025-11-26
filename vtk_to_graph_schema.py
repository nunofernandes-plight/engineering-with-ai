import numpy as np
import h5py
import pyvista as pv
from scipy.spatial import cKDTree

def convert_vtk_to_graph_schema(vtk_file_path, globals_dict, output_h5_path):
    # 1. Load Data using PyVista (Universal VTK reader)
    mesh = pv.read(vtk_file_path)
    
    # 2. Extract Nodes (The Point Cloud)
    # Shape: (Num_Nodes, 3)
    pos = mesh.points.astype(np.float32)
    
    # 3. Extract Fields (The Targets)
    # Shape: (Num_Nodes, 1)
    pressure = mesh.point_data['p'].astype(np.float32)
    # Shape: (Num_Nodes, 3)
    velocity = mesh.point_data['U'].astype(np.float32)
    
    # 4. Extract Connectivity (The Edges)
    # VTK stores cells, we need to convert to an edge list for GNNs.
    # We extract the 'cells' array and convert to 'edge_index' format (Source -> Target)
    # (Simplified extraction logic here for brevity)
    edges = extract_edges_from_vtk_cells(mesh) 
    
    # 5. Write to HDF5 (The AI-Ready Format)
    with h5py.File(output_h5_path, 'w') as f:
        # Globals
        f.create_dataset('global_context', data=list(globals_dict.values()))
        
        # Geometry
        geo_grp = f.create_group('geometry')
        geo_grp.create_dataset('coords', data=pos, compression="gzip")
        geo_grp.create_dataset('connectivity', data=edges, compression="gzip")
        
        # Fields
        fields_grp = f.create_group('fields')
        fields_grp.create_dataset('pressure', data=pressure, compression="gzip")
        fields_grp.create_dataset('velocity', data=velocity, compression="gzip")
        
    print(f"Successfully created Graph Schema: {output_h5_path}")
