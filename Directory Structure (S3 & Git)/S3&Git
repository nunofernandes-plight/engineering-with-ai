# This structure separates code (Git) from heavy data (DVC/S3).

my-platform-repo/
├── .dvc/                  <-- DVC Configuration (points to S3 bucket)
├── dvc.yaml               <-- Defines the Pipeline (Ray -> Bronze -> Silver)
├── dvc.lock               <-- Exact hashes of the current data version
├── scripts/               <-- Your Python solvers and wrappers
│
└── data/                  <-- The "Virtual" Workspace (Managed by DVC)
    ├── bronze/            <-- Git-ignored (sim-outputs/)
    │   └── run_001.zip    <-- Raw OpenFOAM case
    │
    ├── silver/            <-- Git-ignored
    │   ├── run_001.h5     <-- Clean HDF5 (Nodes/Edges)
    │   └── registry.parquet <-- THE KEY: Metadata Index
    │
    └── gold/              <-- Git-ignored
        ├── train_set_v1/  <-- Normalized tensors
        └── manifest.json  <-- Stores the Mean/StdDev for un-normalizing later
