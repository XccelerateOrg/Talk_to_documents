# This repository showcases how to use a local LLM to talk to your documents

* This model requires a GPU to run, since it is a quantized model.

The entry point of the code is from `main.py`.
This file sets up the frontend using streamlit. There's a side panel to upload your documents (only accepts text files).
And then you can ask the assistant any question in the context of the uploaded file.

Next take a look at the config file, where we setup the paths for the different artifacts that are generated when 
running the program.

The `doc_processor.py` file is responsible for converting documents to vectors, and to fetch them
when conversing with the assistant. There are two functions within this file:
- process_file: this function breaks down the file into vectors and stores them into the vectorDB
- process_query: this function matches the given query with the nearness factor of the documents and returns the most
matching document for context.

Finally, the `AI_model.py` file contains the LLM logic. We use a quantized model with very decent performance. The 
function __get_answer()__ which generates an answer given context and a question. 
