import os
import requests

BASE_URL = os.getenv("ENV_BASE_URL", "https://akshat619-support-ticket-env.hf.space")


def run_episode():
    print("START")

    reset_res = requests.post(f"{BASE_URL}/reset")
    reset_res.raise_for_status()

    done = False
    step_count = 0
    total_reward = 0

    while not done:
        step_res = requests.post(f"{BASE_URL}/auto_step")
        step_res.raise_for_status()
        result = step_res.json()

        print(f"STEP {step_count}: {result}")

        total_reward += result["reward"]
        done = result["done"]
        step_count += 1

    score = max(0.0, min(1.0, (total_reward + 5) / 10))

    print("END")
    print({"score": round(score, 2)})


if __name__ == "__main__":
    run_episode()