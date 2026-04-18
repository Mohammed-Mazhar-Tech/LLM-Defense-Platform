from defense_pipeline import DefensePlatform

platform = DefensePlatform()

print("\nLLM Defense Platform Started\n")

while True:

    prompt = input("\nEnter Prompt: ")

    if prompt.lower() == "exit":
        print("Exiting system...")
        break

    result = platform.process(prompt)

    print("\n----------- RESULT -----------")

    print("Status:", result["status"])

    if "risk_score" in result:
        print("Risk Score:", result["risk_score"])

    if result["status"] == "SAFE":
        print("Response:", result["response"])
    else:
        print("Reason:", result["reason"])

    print("------------------------------")
