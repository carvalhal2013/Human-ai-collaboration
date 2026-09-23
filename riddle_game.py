"""Riddle guessing game: the LLM picks a secret topic, writes 3 riddles about it,
and the player guesses the topic. The LLM then judges and explains the answer."""

import random
from openai import OpenAI

client = OpenAI()  # reads OPENAI_API_KEY from the environment


def call_gpt(prompt, temperature=0.7):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )
    return response.choices[0].message.content.strip()


# 1. Auto-generate a secret topic. A random category keeps the LLM from
#    picking the same topic every run.
category = random.choice(["animals", "food", "household objects", "nature", "jobs", "sports", "musical instruments"])
topic = call_gpt(
    f"Pick one common, concrete thing from the category '{category}'. "
    f"Reply with only the name, one or two words, no punctuation.",
    temperature=1.0,
)

# 2. Ask for 3 different riddles about that topic, without revealing it.
riddles = call_gpt(
    f"Write 3 different short riddles whose answer is '{topic}'. "
    f"Each riddle must use a different clue (e.g. appearance, use, sound). "
    f"Never mention the word '{topic}'. Number them 1-3 and give no answers."
)
print(f"\nHere are 3 riddles, all about the same thing:\n\n{riddles}\n")

# 3. Get the player's guess.
guess = input("What is the topic? ")

# 4. Let the LLM judge the guess and explain.
feedback = call_gpt(
    f"The secret topic was '{topic}'. The riddles were:\n{riddles}\n\n"
    f"The player guessed '{guess}'. "
    f"Start with 'Correct!' or 'Not quite.' (accept synonyms and close variants). "
    f"If wrong, explain briefly why the guess doesn't fit the clues. "
    f"Then reveal the correct answer and explain how each riddle points to it."
)
print(f"\n{feedback}")
