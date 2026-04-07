import random
from llm_client import classify_ticket_with_llm


class SupportTicketEnv:
    def __init__(self):
        self.tickets = [
            {"ticket": "I was charged twice for one order", "label": "billing"},
            {"ticket": "My package has not arrived yet", "label": "shipping"},
            {"ticket": "The app crashes when I open settings", "label": "technical"},
            {"ticket": "I want to change my delivery address", "label": "shipping"},
            {"ticket": "I need a refund for my last purchase", "label": "billing"},
            {"ticket": "Login button is not working", "label": "technical"},
        ]
        self.max_steps = 5
        self.reset()

    def reset(self):
        self.step_count = 0
        self.remaining_steps = self.max_steps
        self.done = False
        self.total_reward = 0
        self.current_ticket = random.choice(self.tickets)

        return {
            "ticket": self.current_ticket["ticket"],
            "step": self.step_count,
            "remaining_steps": self.remaining_steps,
        }

    def state(self):
        return {
            "ticket": self.current_ticket["ticket"],
            "step": self.step_count,
            "remaining_steps": self.remaining_steps,
            "done": self.done,
            "total_reward": self.total_reward,
        }

    def auto_action(self):
        return classify_ticket_with_llm(self.current_ticket["ticket"])

    def step(self, action: str):
        if self.done:
            return {
                "done": True,
                "reward": 0,
                "info": {
                    "result": "episode_finished",
                    "correct_label": self.current_ticket["label"],
                    "your_action": action,
                },
                "next_state": self.state(),
            }

        correct_label = self.current_ticket["label"]
        chosen = action.strip().lower()
        is_correct = chosen == correct_label.lower()

        reward = 1 if is_correct else -1
        self.total_reward += reward
        self.step_count += 1
        self.remaining_steps -= 1

        info = {
            "correct_label": correct_label,
            "result": "correct" if is_correct else "wrong",
            "your_action": chosen,
        }

        if self.remaining_steps <= 0:
            self.done = True
        else:
            self.current_ticket = random.choice(self.tickets)

        return {
            "done": self.done,
            "reward": reward,
            "info": info,
            "next_state": {
                "ticket": self.current_ticket["ticket"],
                "step": self.step_count,
                "remaining_steps": self.remaining_steps,
            },
        }