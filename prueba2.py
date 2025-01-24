from unstructured.partition.pdf import partition_pdf
output_path ='./content'
file_path = './trabajo.pdf'

# Reference: https://docs.unstructured.io/open-source/core-functionality/chunking

def pipeline(file_path):
    chunks = process_pdf(file_path)
    table, texts, images = divide_chunks(chunks)
    print(table)
    print(texts)
    print(images)



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


def divide_chunks(chunks):
    tables = []
    texts = []
    images = []

    for chunk in chunks:
        if "Table" in str(type(chunk)):
            tables.append(chunk)
        if "CompositeElement" in str(type(chunk)):
            texts.append(chunk)
            chunk_elements = chunk.metadata.orig_elements
            for element in chunk_elements:
                if "Image" in str(type(element)):
                    images.append(element)

    return tables, texts, images

pipeline(file_path)from unstructured.partition.pdf import partition_pdf
output_path ='./content'
file_path = './trabajo.pdf'

# Reference: https://docs.unstructured.io/open-source/core-functionality/chunking

def pipeline(file_path):
    chunks = process_pdf(file_path)
    table, texts, images = divide_chunks(chunks)
    print(table)
    print(texts)
    print(images)



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


def divide_chunks(chunks):
    tables = []
    texts = []
    images = []

    for chunk in chunks:
        if "Table" in str(type(chunk)):
            tables.append(chunk)
        if "CompositeElement" in str(type(chunk)):
            texts.append(chunk)
            chunk_elements = chunk.metadata.orig_elements
            for element in chunk_elements:
                if "Image" in str(type(element)):
                    images.append(element)

    return tables, texts, images

pipeline(file_path)
