import pandas as pd
import json

# -------------------------
# Load jailbreak prompts
# -------------------------
jailbreak = pd.read_csv("datasets/jailbreak_prompts_2023_05_07.csv")

jailbreak = jailbreak[["prompt"]]
jailbreak["label"] = 1


# -------------------------
# Load regular prompts
# -------------------------
regular = pd.read_csv("datasets/regular_prompts_2023_05_07.csv")

regular = regular[["prompt"]]
regular["label"] = 0


# -------------------------
# Load synthetic dataset
# -------------------------
synthetic = pd.read_csv("datasets/synthetic_dataset.csv")

synthetic = synthetic[["prompt","jailbreak"]]
synthetic.rename(columns={"jailbreak":"label"},inplace=True)


# -------------------------
# Load JSONL dataset
# -------------------------
prompts = []
labels = []

with open("datasets/Prompt_INJECTION_And_Benign_DATASET.jsonl","r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)

        prompts.append(data["prompt"])

        if data["label"] == "malicious":
            labels.append(1)
        else:
            labels.append(0)

json_df = pd.DataFrame({
    "prompt":prompts,
    "label":labels
})


# -------------------------
# Merge all datasets
# -------------------------
final_dataset = pd.concat([
    jailbreak,
    regular,
    synthetic,
    json_df
])


# -------------------------
# Save final dataset
# -------------------------
final_dataset.to_csv("datasets/final_dataset.csv",index=False)

print("Dataset successfully prepared!")
print("Total samples:",len(final_dataset))
