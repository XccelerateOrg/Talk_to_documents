from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

model_path = "TheBloke/Trion-M-7B-GPTQ"

model = AutoModelForCausalLM.from_pretrained(model_path,
                                             device_map="auto",
                                             trust_remote_code=False,
                                             # disable_exllama=True,
                                             revision="main",
                                             cache_dir="./models/")
tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=True, cache_dir="./models/")

llm_pipeline = pipeline("text-generation", model=model,
                        tokenizer=tokenizer,
                        max_new_tokens=128,
                        do_sample=True,
                        temperature=0.7,
                        top_p=0.85,
                        top_k=50,
                        repetition_penalty=1.1)


def get_answer(questions: str, context: str):
    prompt_template = f"""Below is a content and a question. Answer the question in the context of the content.
### Content:
{context}

### Question:
{questions}

### Response:
"""
    gen_text = llm_pipeline(prompt_template)[0]['generated_text']

    gen_text = gen_text.split('Response:')[-1]

    return gen_text
