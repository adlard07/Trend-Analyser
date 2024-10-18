import kagglehub

# Download latest version
path = kagglehub.dataset_download("mafzal19/electric-vehicle-sales-by-state-in-india")

print("Path to dataset files:", path)