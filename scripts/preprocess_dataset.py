import pandas as pd

# Load raw dataset
df = pd.read_csv("Dataset/symptoms_df.csv")

# Normalize: lowercase, replace spaces with underscores, strip
def normalize(symptom):
    if pd.isna(symptom):
        return None
    return str(symptom).strip().lower().replace(" ", "_")

for col in df.columns:
    if col.lower().startswith("symptom"):
        df[col] = df[col].apply(normalize)

# Drop empty symptoms
df = df.dropna(how="all", subset=[c for c in df.columns if "symptom" in c.lower()])

# Save cleaned dataset
df.to_csv("Dataset/symptoms_df_clean.csv", index=False)
print("✅ Preprocessed dataset saved to Dataset/symptoms_df_clean.csv")
