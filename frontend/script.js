
    const BASE_URL = "http://127.0.0.1:7860";

    let totalReward = 0;
    let isDone = false;

    function updateStatus(text) {
      document.getElementById("statusBadge").innerText = text;
    }

    function updateTicket(ticket) {
      document.getElementById("ticketBox").innerText = ticket;
    }

    function updateStep(step) {
      document.getElementById("stepValue").innerText = step;
    }

    function updateRemaining(remaining) {
      document.getElementById("remainingValue").innerText = remaining;
    }

    function updateReward(value) {
      document.getElementById("rewardValue").innerText = value;
    }

   function updateResponse(data) {
  const box = document.getElementById("responseBox");

  if (data.ticket !== undefined && data.step !== undefined && data.remaining_steps !== undefined) {
    box.innerText =
`Status: ${data.done ? "Completed" : "Running"}
Step: ${data.step}
Remaining Steps: ${data.remaining_steps}
Total Reward: ${data.total_reward ?? totalReward}
Current Ticket: ${data.ticket}`;
    return;
  }

  if (data.next_state) {
    box.innerText =
`Result: ${data.info?.result ?? "N/A"}
Your Action: ${data.info?.your_action ?? "N/A"}
Correct Label: ${data.info?.correct_label ?? "N/A"}
Reward: ${data.reward}
Done: ${data.done ? "Yes" : "No"}

Next Ticket: ${data.next_state.ticket}
Next Step: ${data.next_state.step}
Remaining Steps: ${data.next_state.remaining_steps}`;
    return;
  }

  if (data.error) {
    box.innerText = `Error: ${data.error}`;
    return;
  }

  box.innerText = JSON.stringify(data, null, 2);
}

    async function startSession() {
      try {
        const res = await fetch(`${BASE_URL}/reset`);
        const data = await res.json();

        totalReward = 0;
        isDone = false;

        updateTicket(data.ticket);
        updateStep(data.step);
        updateRemaining(data.remaining_steps);
        updateReward(totalReward);
        updateStatus("Running");
        updateResponse(data);
      } catch (error) {
        updateResponse({ error: error.message });
        updateStatus("Server Error");
      }
    }

    async function getCurrentState() {
      try {
        const res = await fetch(`${BASE_URL}/state`);
        const data = await res.json();

        updateTicket(data.ticket);
        updateStep(data.step);
        updateRemaining(data.remaining_steps);
        updateReward(data.total_reward ?? totalReward);
        updateStatus(data.done ? "Completed" : "Running");
        updateResponse(data);
      } catch (error) {
        updateResponse({ error: error.message });
        updateStatus("Server Error");
      }
    }

    async function sendAction(action) {
      if (isDone) {
        updateResponse({ message: "Tickets   already finished. Click Start / Reset." });
        return;
      }

      try {
        const res = await fetch(`${BASE_URL}/step`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ action })
        });

        const data = await res.json();

        totalReward += data.reward;
        isDone = data.done;

        updateTicket(data.next_state.ticket);
        updateStep(data.next_state.step);
        updateRemaining(data.next_state.remaining_steps);
        updateReward(totalReward);
        updateStatus(data.done ? "Completed" : "Running");
        updateResponse(data);
      } catch (error) {
        updateResponse({ error: error.message });
        updateStatus("Server Error");
      }
    }
  