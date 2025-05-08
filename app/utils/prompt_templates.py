def get_conversation_prompt(scenario, history, message, lang):
    return f"""
You are practicing {lang} conversation. The scenario is: {scenario}
Conversation so far:
{history}

User: {message}
Bot:
"""

def get_hint_conversation_prompt(scenario, history, lang):
    return f"""
You are practicing {lang} conversation. The scenario is: {scenario}
Conversation so far:
{history}
User:

Can you generate example of dialogue for user what to speak next? Words should be less than 15 words.
"""

def get_context_prompt(scenario, role, place, lang):
    return f"""
You are roleplaying as a {role} in a {place} to help a user practice {lang}. The conversation simulates a realistic and friendly interaction.
Rules: 
1. The dialogue must be no more than 7 turns total (each turn = 1 user + 1 assistant message).
2. Your sentences must be no longer than 30 words.
3. Begin with a short greeting.
4. End with a polite goodbye if it’s the 7th turn, even if the user hasn’t said goodbye.
5. Be friendly and natural, but stay on topic.
Scenario context: "I am at a {place} talking with you as a {role}"
Scenario: "{scenario}"
"""

def get_keywords_prompt(scenario, role, place, lang, response):
    return f"""
I would like you to generate me an image based on your last response on our role-play scenario conversation.
For a context, The scenario is {scenario}. You are playing as a {role} in a {place}. The language used in this role-play is {lang} 
I need your help to extract the relevant keywords and nouns out of this response: 
{response}

Please generate keywords result only. Do not put any additional sentences or symbols.
"""

def get_image_prompt(scenario, role, place, lang, response, keywords):
    return f"""
I would like you to create a photograph based on your last response.
As for context, we are currently doing a role-based scenario. The scenario is {scenario}.
You are playing as a {role} in a {place}.The language used in this role-play is {lang}.
Your last dialogue response was {response}. 
These are the keywords to generate the image: {keywords}.
"""