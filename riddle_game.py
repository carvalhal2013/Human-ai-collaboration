"""Riddle guessing game: the player picks a category, the LLM picks a secret topic
in it and gives one riddle at a time. The player has 3 attempts to guess it."""

from openai import OpenAI

client = OpenAI()  # reads OPENAI_API_KEY from the environment
MAX_ATTEMPTS = 3


def call_gpt(prompt, temperature=0.7):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )
    return response.choices[0].message.content.strip()


# 1. The player chooses the category; the LLM picks a secret topic in it.
category = input("Choose a category (e.g. animals, food, sports): ")
topic = call_gpt(
    f"Pick one common, concrete thing from the category '{category}'. "
    f"Reply with only the name, one or two words, no punctuation.",
    temperature=1.0,
)

riddles = []
for attempt in range(1, MAX_ATTEMPTS + 1):
    # 2. One new riddle per attempt, each easier than the last.
    riddle = call_gpt(
        f"Write one short riddle whose answer is '{topic}'. "
        f"Never mention the word '{topic}'. Give no answer. "
        f"It must use a different clue from these earlier riddles and be easier "
        f"than them: {riddles if riddles else 'none yet'}"
    )
    riddles.append(riddle)
    print(f"\nRiddle {attempt} of {MAX_ATTEMPTS}:\n{riddle}\n")

    guess = input("Your guess: ")

    # 3. Strict YES/NO verdict, checked in Python, so the game logic
    #    doesn't depend on parsing free-form text.
    verdict = call_gpt(
        f"The secret answer is '{topic}'. The player guessed '{guess}'. "
        f"Is the guess the same thing (exact match, synonym or spelling variant)? "
        f"A related but different thing is NOT correct. Reply only YES or NO.",
        temperature=0,
    )

    if verdict.upper().startswith("YES"):
        print("\n" + call_gpt(
            f"The player correctly guessed '{topic}' after {attempt} riddle(s): {riddles}. "
            f"Congratulate them in one sentence, then briefly explain how each riddle points to '{topic}'."
        ))
        break

    if attempt < MAX_ATTEMPTS:
        print("\n" + call_gpt(
            f"The secret answer is '{topic}' (do NOT reveal it). The riddle was: {riddle}. "
            f"The player guessed '{guess}', which is wrong. In one or two sentences, "
            f"explain which clue in the riddle doesn't fit their guess, without giving the answer away."
        ))
        print(f"Attempts left: {MAX_ATTEMPTS - attempt}")
else:
    # 4. Out of attempts: reveal and explain.
    print("\n" + call_gpt(
        f"The player failed to guess '{topic}' in {MAX_ATTEMPTS} attempts. Their last guess was '{guess}'. "
        f"The riddles were: {riddles}. Tell them the answer was '{topic}', "
        f"say briefly why their last guess was wrong, and explain how each riddle points to '{topic}'."
    ))
