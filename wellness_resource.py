from flask import Blueprint, render_template, request
import random

# Blueprint registered under prefix "/wellness"
wellness_bp = Blueprint("wellness", __name__, template_folder="Templates")

# ------------------ Data ------------------
categories = {
    "Mind": ["Practice meditation for 5 minutes daily", "Try journaling your thoughts", "Use apps like Headspace or Calm"],
    "Body": ["Do at least 20 minutes of exercise", "Simple stretches help reduce stiffness", "Stay hydrated while being active"],
    "Nutrition": ["Eat balanced meals with protein, carbs, and veggies", "Drink at least 7–8 glasses of water daily", "Avoid too much junk food"],
    "Sleep": ["Aim for 7–8 hours of sleep daily", "Avoid screen time 30 mins before bed", "Keep a consistent sleep schedule"],
    "Stress Relief": ["Try deep breathing (inhale 4s, hold 4s, exhale 4s)", "Listen to calming music", "Take short breaks while working"]
}

affirmations = [
    "✨ You are stronger than you think.",
    "🌞 Small steps every day lead to big changes.",
    "🌸 Prioritize your well-being — you deserve it.",
    "💡 Every day is a new beginning — take a deep breath and start fresh."
]

tasks = []
moods = []

# ------------------ Routes ------------------
@wellness_bp.route("/")
def home():
    return render_template("Wellness_resource_index.html",
                           categories=categories,
                           affirmation=random.choice(affirmations))

@wellness_bp.route("/affirmation")
def affirmation():
    return render_template("affirmation.html", affirmation=random.choice(affirmations))

@wellness_bp.route("/self-check", methods=["GET", "POST"])
def self_check():
    tip = None
    if request.method == "POST":
        stress = int(request.form.get("stress"))
        sleep = int(request.form.get("sleep"))
        mood = int(request.form.get("mood"))

        if stress > 7:
            tip = "😟 You seem stressed. Try deep breathing or take a short walk."
        elif sleep < 6:
            tip = "😴 You need more rest. Try to get at least 7–8 hours of sleep."
        elif mood < 5:
            tip = "💙 It’s okay to have tough days. Try journaling or talking to a friend."
        else:
            tip = "🌟 You're doing well! Keep maintaining your healthy habits."
    return render_template("self_check.html", tip=tip)

@wellness_bp.route("/planner", methods=["GET", "POST"])
def planner():
    global tasks
    if request.method == "POST":
        task = request.form.get("task")
        if task:
            tasks.append(task)
    return render_template("planner.html", tasks=tasks)

@wellness_bp.route("/mood", methods=["GET", "POST"])
def mood():
    global moods
    if request.method == "POST":
        mood_value = request.form.get("mood")
        if mood_value:
            moods.append(mood_value)
    return render_template("mood.html", moods=moods)

@wellness_bp.route("/resources")
def resources():
    return render_template("resource.html")


