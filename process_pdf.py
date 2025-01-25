from unstructured.partition.pdf import partition_pdf
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
from langchain.chains import SimpleSequentialChain
from langchain_ollama import ChatOllama
import ollama



def processing_pipeline(file_path):
    chunks = process_pdf(file_path)
    texts, images = divide_chunks(chunks)

    text_summaries, images_summaries = summarize(texts,images)


    return texts, images, text_summaries, images_summaries
   
    print("Chunks stored correctly")




def process_pdf(file_path):
    chunks = partition_pdf(
        filename=file_path,
        infer_table_structure=True,            # extract tables
        strategy="hi_res",                     # mandatory to infer tables

        extract_image_block_types=["Image"],   # Add 'Table' to list to extract image of tables
        # image_output_dir_path=output_path,   # if None, images and tables will saved in base64

        extract_image_block_to_payload=True,   # if true, will extract base64 for API usage

        chunking_strategy="by_title",          # or 'basic'
        max_characters=10000,                  # defaults to 500
        combine_text_under_n_chars=2000,       # defaults to 0
        new_after_n_chars=6000,

        extract_images_in_pdf=True,         
    )
    return chunks


def divide_chunks(chunks):
    texts = []
    images = []
    for chunk in chunks:
        if "CompositeElement" in str(type(chunk)):
            texts.append(chunk)
            
            chunk_elements = chunk.metadata.orig_elements
            for element in chunk_elements:
                if "Image" in str(type(element)):
                    images.append(element)
                    
                    
              

    return   texts, images


def summarize(texts, images):
    text_summaries = [summarize_text(text) for text in texts]

    #comprehensive_summary = create_comprehensive_summary(text_summaries)
    comprehensive_summary = 'sd'
    images_summaries = [summarize_images(image,comprehensive_summary) for image in images]

    return text_summaries, images_summaries
   
   

def summarize_images(element,context):
    prompt_template = f"""Describe what is shown in the image with great detail.
                 
"""
    model = ChatOllama(
        model='llava:latest',
        base_url='http://ollama:11434',
        temperature=0.5
    )
    messages = [
    (
        "user",
        [
            {"type": "text", "text": prompt_template},
            {
                "type": "image_url",
                "image_url": {"url": "data:image/jpeg;base64,{element}"},
            },
        ],
    )
]
    prompt = ChatPromptTemplate.from_messages(messages)
    
    input_prompt = prompt.format(element=element)
    response = model.invoke([{"role": "user", "content": input_prompt}])
    print(response.content)
    
    
    return response.content


def summarize_text(element):
    prompt_text = """
You are an assistant tasked with summarizing tables and text.
Give a concise summary of the table or text.

Respond only with the summary, no additional comment.
Do not start your message by saying "Here is a summary" or anything like that.
Just give the summary as it is.

Table or text chunk: {element}
"""
    prompt = ChatPromptTemplate.from_template(prompt_text)
    model = ChatOllama(
        model='llama3.1:latest',
        base_url='http://ollama:11434',  # Ensure this matches the running Ollama server
        temperature=0.5
)
    input_prompt = prompt.format(element=element)
    response = model.invoke([{"role": "user", "content": input_prompt}])
    
    return response.content


def create_comprehensive_summary(text_summaries):
    prompt_template = """
    You are tasked with creating a comprehensive summary of a document based on individual section summaries.
    Please synthesize the following summaries into a coherent, well-structured overview of the entire document:

    {summaries}

    Provide a concise yet informative summary that captures the main ideas and key points from all sections.
    Organize the information logically and highlight any important themes or conclusions.
    """

    prompt = ChatPromptTemplate.from_template(prompt_template)
    
    model = ChatOllama(
        model='llama3.1:latest',
        base_url='http://ollama:11434',
        temperature=0.5
    )

    all_summaries = "\n\n".join(text_summaries)

    formatted_prompt = prompt.format_messages(summaries=all_summaries)

    response = model.invoke(formatted_prompt)

    return response.content

