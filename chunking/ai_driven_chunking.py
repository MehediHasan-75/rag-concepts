from langchain_community.chat_models import ChatDatabricks
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import json
import re

def perform_ai_driven_chunking(document, max_chunks=20, fallback_chunk_size=1000):
    """
    Uses an LLM to intelligently chunk content based on semantic boundaries.
    
    Args:
        document (str): The text document to process
        max_chunks (int): Maximum number of chunks to create
        fallback_chunk_size (int): Chunk size to use if LLM chunking fails
        
    Returns:
        list: The semantically chunked documents with metadata
    """
    # Initialize the Databricks LLM
    llm = ChatDatabricks(
        endpoint="databricks-meta-llama-3-3-70b-instruct",
        temperature=0.1,
        max_tokens=4000  # Increased to handle longer outputs
    )
    
    # Create a chat prompt template for the chunking task
    chunking_prompt = ChatPromptTemplate.from_template("""
    You are a document processing expert. Your task is to break down the following document into 
    at most {max_chunks} meaningful chunks. Follow these guidelines:
    
    1. Each chunk should contain complete ideas or concepts
    2. More complex sections should be in smaller chunks
    3. Preserve headers with their associated content
    4. Keep related information together
    5. Maintain the original order of the document
    
    DOCUMENT:
    {document}
    
    Return ONLY a valid JSON array of strings, where each string is a chunk.
    Format your response as:
    ```json
    [
      "chunk1 text",
      "chunk2 text",
      ...
    ]
    ```
    
    Do not include any explanations or additional text outside the JSON array.
    """)
    
    # Create the chain
    chunking_chain = chunking_prompt | llm
    
    try:
        # Invoke the LLM to get chunking suggestions
        response = chunking_chain.invoke({"document": document, "max_chunks": max_chunks})
        
        # Extract JSON from the response
        content = response.content
        
        # Find JSON array in the response (looking for text between [ and ])
        json_match = re.search(r'\[\s*".*"\s*\]', content, re.DOTALL)
        if json_match:
            content = json_match.group(0)
        
        # Try to parse the JSON response
        chunks = json.loads(content)
        print(f"Successfully chunked document into {len(chunks)} AI-driven chunks")
        
        # Create Document objects with metadata
        documents = []
        for i, chunk in enumerate(chunks):
            # Calculate relative position for tracking
            position = i / len(chunks)
            
            # Analyze chunk complexity based on length and unique word density
            words = re.findall(r'\b\w+\b', chunk.lower())
            unique_words = set(words)
            word_density = len(unique_words) / max(1, len(words))
            
            doc = Document(
                page_content=chunk,
                metadata={
                    "chunk_id": i,
                    "total_chunks": len(chunks),
                    "chunk_size": len(chunk),
                    "chunk_type": "ai_driven",
                    "document_position": round(position, 2),
                    "word_count": len(words),
                    "unique_words": len(unique_words),
                    "word_density": round(word_density, 2)
                }
            )
            documents.append(doc)
        
        return documents
            
    except Exception as e:
        print(f"LLM chunking failed: {e}")
        print("Falling back to basic chunking")
        return fallback_chunking(document, chunk_size=fallback_chunk_size)

def fallback_chunking(document, chunk_size=1000, chunk_overlap=100):
    """
    Fallback method if LLM chunking fails.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    chunks = splitter.split_text(document)
    print(f"Fallback chunking created {len(chunks)} chunks")
    
    # Convert to Document objects
    documents = []
    for i, chunk in enumerate(chunks):
        doc = Document(
            page_content=chunk,
            metadata={
                "chunk_id": i,
                "total_chunks": len(chunks),
                "chunk_size": len(chunk),
                "chunk_type": "fallback",
                "document_position": round(i / len(chunks), 2)
            }
        )
        documents.append(doc)
    
    return documents

# Mock implementation for testing without Databricks
def perform_ai_driven_chunking_mock(document, max_chunks=20):
    """
    Mock version of AI-driven chunking for testing without Databricks.
    Uses paragraph-based chunking as a simple approximation of LLM chunking.
    """
    # Simple chunking by paragraphs for the mock
    paragraphs = document.split("\n\n")
    
    # Combine very short paragraphs
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        if not para.strip():
            continue
            
        if len(current_chunk) + len(para) < 500:
            current_chunk += para + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = para + "\n\n"
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    # Ensure we don't exceed max_chunks
    if len(chunks) > max_chunks:
        # Combine chunks to reduce count
        new_chunks = []
        chunks_per_group = len(chunks) // max_chunks + 1
        
        for i in range(0, len(chunks), chunks_per_group):
            group = chunks[i:i + chunks_per_group]
            new_chunks.append("\n\n".join(group))
        
        chunks = new_chunks
    
    print(f"Mock AI chunking created {len(chunks)} chunks")
    
    # Create Document objects
    documents = []
    for i, chunk in enumerate(chunks):
        # Calculate relative position
        position = i / len(chunks)
        
        # Basic text analytics
        words = re.findall(r'\b\w+\b', chunk.lower())
        unique_words = set(words)
        word_density = len(unique_words) / max(1, len(words))
        
        doc = Document(
            page_content=chunk,
            metadata={
                "chunk_id": i,
                "total_chunks": len(chunks),
                "chunk_size": len(chunk),
                "chunk_type": "mock_ai_driven",
                "document_position": round(position, 2),
                "word_count": len(words),
                "unique_words": len(unique_words),
                "word_density": round(word_density, 2)
            }
        )
        documents.append(doc)
    
    return documents

# Example usage
if __name__ == "__main__":
    # Import the dummy document creation function
    
    with open("docs/chunking/fixedSizeChunk/rag_chunking_test_doc.md", "r", encoding="utf-8") as file:
        document = file.read()
    
    # Use mock version for testing without Databricks
    print("Using mock implementation for testing...")
    chunked_docs = perform_ai_driven_chunking_mock(document, max_chunks=10)
    
    # Display results
    print("\n----- CHUNKING RESULTS -----")
    print(f"Total chunks: {len(chunked_docs)}")
    
    # Print an example chunk
    print("\n----- EXAMPLE CHUNK -----")
    middle_chunk_idx = len(chunked_docs) // 2
    example_chunk = chunked_docs[middle_chunk_idx]
    print(f"Chunk {middle_chunk_idx}:")
    print("-" * 40)
    print(example_chunk.page_content[:200] + "..." if len(example_chunk.page_content) > 200 
          else example_chunk.page_content)
    print("-" * 40)
    print(f"Metadata: {example_chunk.metadata}")
    
    print("\nTo use with Databricks:")
    print("1. Replace 'perform_ai_driven_chunking_mock' with 'perform_ai_driven_chunking'")
    print("2. Ensure your Databricks endpoint is correctly configured")
    print("3. Consider adjusting max_chunks based on your document size")

    output_path = "docs/chunking/ai_driven_chunking/chunk_output.txt"
    try:
        with open(output_path, "w", encoding="utf-8") as output_file:
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
        print(f"\nAll chunks have been successfully saved to '{output_path}'")
    except FileNotFoundError:
        print(f"\nCould not save to '{output_path}'. Please ensure the directory exists.")