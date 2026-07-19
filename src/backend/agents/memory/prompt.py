from langchain_core.prompts import ChatPromptTemplate

summarize_prompt = ChatPromptTemplate.from_messages([
  ('system', '''Summarize the given text in two versions:

User summary – keep the request unchanged if it is ≤50 tokens; otherwise shorten it while preserving meaning.

AI summary – strictly ≤200 tokens, concise, essential, no filler
Return messages only on English language
'''), 
  ('human', 'User_message: {user_message}\n Ai_message: {message_to_user}')
])
