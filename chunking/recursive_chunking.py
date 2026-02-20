from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from langchain_core.documents import Document
import json
import re

def perform_code_chunking(code_document, language="python", chunk_size=100, chunk_overlap=15):
    """
    Performs recursive chunking on code documents using language-aware splitting.
    
    Args:
        code_document (str): The code document to process
        language (str): Programming language of the code
        chunk_size (int): The target size of each chunk in characters
        chunk_overlap (int): The number of characters of overlap between chunks
        
    Returns:
        list: The chunked code as Document objects with metadata
    """
    # Create language-specific splitter using the updated API
    if language.lower() == "python":
        code_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.PYTHON,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    elif language.lower() == "javascript":
        code_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.JS,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    elif language.lower() == "java":
        code_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.JAVA,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    elif language.lower() == "go":
        code_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.GO,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    elif language.lower() == "rust":
        code_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.RUST,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    else:
        # Fallback to generic code splitting
        code_splitter = RecursiveCharacterTextSplitter(
            separators=["\nclass ", "\ndef ", "\n\n", "\n", " ", ""],
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )
        
    # Split the code into chunks
    code_chunks = code_splitter.split_text(code_document)
    print(f"Code document split into {len(code_chunks)} chunks")
    
    # Extract functions and classes for better metadata
    documents = []
    for i, chunk in enumerate(code_chunks):
        # Try to identify code structure
        function_match = re.search(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', chunk)
        class_match = re.search(r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)', chunk)
        import_match = re.search(r'import\s+([a-zA-Z_][a-zA-Z0-9_\.]*)', chunk)
        
        # Determine chunk type
        chunk_type = "code_segment"
        if function_match:
            chunk_type = "function"
            structure_name = function_match.group(1)
        elif class_match:
            chunk_type = "class"
            structure_name = class_match.group(1)
        elif import_match:
            chunk_type = "import"
            structure_name = import_match.group(1)
        else:
            structure_name = f"segment_{i}"
        
        # Create document with enhanced metadata
        doc = Document(
            page_content=chunk,
            metadata={
                "chunk_id": i,
                "total_chunks": len(code_chunks),
                "language": language,
                "chunk_type": chunk_type,
                "structure_name": structure_name,
                "lines": chunk.count('\n') + 1
            }
        )
        documents.append(doc)
    
    return documents

# Example usage with Databricks integration
if __name__ == "__main__":
    # Create Python code document
    with open("docs/chunking/recursive_chunking/python_code.md", "r", encoding="utf-8") as file:
        python_document = file.read()

    # Process with code chunking
    chunked_docs = perform_code_chunking(
        python_document,
        language="python",
        chunk_size=100,
        chunk_overlap=15
    )
    
    # Display results
    print("\n----- CHUNKING RESULTS -----")
    print(f"Total code chunks: {len(chunked_docs)}")
    
    # Print chunk types distribution
    chunk_types = {}
    for doc in chunked_docs:
        chunk_type = doc.metadata["chunk_type"]
        chunk_types[chunk_type] = chunk_types.get(chunk_type, 0) + 1
    
    print("\n----- CODE STRUCTURE BREAKDOWN -----")
    for chunk_type, count in chunk_types.items():
        print(f"{chunk_type}: {count} chunks")
    
    # Print an example function chunk
    print("\n----- EXAMPLE FUNCTION CHUNK -----")
    function_chunks = [doc for doc in chunked_docs if doc.metadata["chunk_type"] == "function"]
    if function_chunks:
        example_chunk = function_chunks[0]
        print(f"Function: {example_chunk.metadata['structure_name']}")
        print("-" * 40)
        print(example_chunk.page_content)
        print("-" * 40)
    
    # For integration with Databricks
    print("\nTo use with Databricks:")
    print("1. Store code chunks in Delta table with metadata")
    print("2. Create embeddings using:")
    print("   from langchain_community.embeddings import DatabricksEmbeddings")
    print("   embeddings = DatabricksEmbeddings(endpoint='databricks-bge-large-en')")
    print("3. Create Vector Search index for code retrieval")
    print("4. Use function/class metadata for filtering during retrieval")

    # Open file in write mode
    with open("docs/chunking/recursive_chunking/chunk_output.txt", "w", encoding="utf-8") as output_file:
        
        for i, doc in enumerate(chunked_docs):
            # Write the chunk header
            output_file.write(f"--- Chunk {i} ---\n\n")
            
            # Write the chunk content
            output_file.write(doc.page_content + "\n\n")
            
            # Write the metadata as JSON for readability
            output_file.write("Metadata:\n")
            output_file.write(json.dumps(doc.metadata, indent=4))
            
            # Add separation between chunks
            output_file.write("\n\n")

    print("All chunks have been successfully saved to 'docs/chunking/recursiveChunking/chunk_output.txt'")