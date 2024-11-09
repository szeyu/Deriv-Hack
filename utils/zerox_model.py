from pyzerox import zerox
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables from .env file
load_dotenv()

###################### Example for OpenAI ######################
model = "gpt-4o"  # openai model
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")  # Load API key from .env file

###################### Example for Gemini ######################
# model = "gemini/gpt-4o-mini" ## "gemini/<gemini_model>" -> format <provider>/<model>
# os.environ['GEMINI_API_KEY'] = "" # your-gemini-api-key

async def zerox_model(input_doc_path, custom_system_prompt=None, kwargs={}):
    # process only some pages or all
    select_pages = None  # None for all, but could be int or list(int) page numbers (1 indexed)

    output_dir = "./output_test"  # directory to save the consolidated markdown file
    result = await zerox(file_path=input_doc_path, model=model, output_dir=output_dir,
                        custom_system_prompt=custom_system_prompt, select_pages=select_pages, **kwargs)
    st.write(result)
    st.markdown(result)