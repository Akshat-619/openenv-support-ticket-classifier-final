import os
import requests

BASE_URL = os.getenv("ENV_BASE_URL", "http://127.0.0.1:7860")


def run_episode():
    print("START")

    reset_res = requests.get(f"{BASE_URL}/reset")
    state = reset_res.json()

    done = False
    step_count = 0

    while not done:
        step_res = requests.post(f"{BASE_URL}/auto_step")
        result = step_res.json()

        print(f"STEP {step_count}: {result}")

        done = result["done"]
        step_count += 1

    print("END")


if __name__ == "__main__":
    run_episode()