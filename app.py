import os
import gradio as gr
from tokenizers import Tokenizer
from huggingface_hub import hf_hub_download

# Explicitly set cache directories using a path inside the app folder
cache_dir = "/app/cache"

# Ensure the cache directory exists
os.makedirs(cache_dir, exist_ok=True)

# Download the tokenizer from Hugging Face Hub and specify cache directory
tokenizer_path = hf_hub_download(
    repo_id="antonyrajesh/Tamil-BPE-Tokenizer", 
    filename="tokenizer.json", 
    cache_dir=cache_dir
)

# Load the tokenizer
tokenizer = Tokenizer.from_file(tokenizer_path)

# Encoding function
def encode_text(text):
    encoded = tokenizer.encode(text)
    return {
        "Tokens": encoded.tokens, 
        "Token IDs": encoded.ids
    }

# Decoding function (converts input string to list of integers)
def decode_text(token_ids_str):
    try:
        # Convert the comma-separated string into a list of integers
        token_ids = list(map(int, token_ids_str.split(',')))
        decoded_text = tokenizer.decode(token_ids)
        return {
            "Decoded Text": decoded_text
        }
    except Exception as e:
        return {"Error": f"Invalid input. Please provide a comma-separated list of token IDs. Error: {str(e)}"}

# Create Gradio interface for encoding
encode_interface = gr.Interface(
    fn=encode_text, 
    inputs="text", 
    outputs="json",
    title="Tamil BPE Tokenizer - Encode",
    description="Tokenize Tamil text using your custom BPE tokenizer."
)

# Create Gradio interface for decoding (input as comma-separated token IDs)
decode_interface = gr.Interface(
    fn=decode_text, 
    inputs="text",  # Input will be a comma-separated list of token IDs
    outputs="json",
    title="Tamil BPE Tokenizer - Decode",
    description="Decode token IDs (comma-separated) back into Tamil text. E.g., '1001,2002,3003'"
)

# Combine the encode and decode interfaces into a tabbed interface
demo = gr.TabbedInterface([encode_interface, decode_interface], 
                          tab_names=["Encode", "Decode"])

# Launch the app on a single port
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)