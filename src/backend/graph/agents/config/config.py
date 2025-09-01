from dotenv import load_dotenv
import os 

load_dotenv()

qdrant_url = os.getenv('QDRANT_URL')
base_url = 'https://openrouter.ai/api/v1'
zep_api = os.getenv('ZEP_API')

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ['HUGGINGFACEHUB_API_TOKEN'] = os.getenv('HUGGINGFACEHUB_API_TOKEN')
os.environ['QDRANT_API_KEY'] = os.getenv('QDRANT_API_KEY')