from dotenv import load_dotenv

import os 

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

base_url = 'https://openrouter.ai/api/v1'