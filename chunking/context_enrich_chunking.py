import json
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatDatabricks
from langchain_core.documents import Document
import numpy as np

def perform_context_enriched_chunking(document, chunk_size=500, chunk_overlap=50, 
                                     window_size=1, summarize=True):
    """
    Performs context-enriched chunking by attaching summaries from neighboring chunks.
    
    Args:
        document (str): The text document to process
        chunk_size (int): Base size for each chunk
        chunk_overlap (int): Overlap between chunks
        window_size (int): Number of chunks to include on each side for context
        summarize (bool): Whether to summarize context (True) or use raw text (False)
        
    Returns:
        list: The enriched document chunks with metadata
    """
    # Initialize the Databricks model
    chat_model = ChatDatabricks(
        endpoint="databricks-meta-llama-3-3-70b-instruct",
        temperature=0.1,
        max_tokens=250,
    )

    # Create text splitter with optimal parameters
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ".", " ", ""],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    # Split the document into base chunks
    base_chunks = splitter.split_text(document)
    print(f"Document split into {len(base_chunks)} base chunks")

    # Create a summarization chain
    summary_prompt = PromptTemplate.from_template(
        "Provide a brief summary of the following text:\n\n{text}\n\nSummary:"
    )
    print(summary_prompt)
    # Modern LCEL pattern replacing LLMChain and StuffDocumentsChain
    summary_chain = summary_prompt | chat_model | StrOutputParser()

    # Process chunks with contextual windows
    enriched_documents = []
    for i, chunk in enumerate(base_chunks):
        print(f"Processing chunk {i+1}/{len(base_chunks)}")
        
        # Define window around current chunk
        window_start = max(0, i - window_size)
        window_end = min(len(base_chunks), i + window_size + 1)
        window = base_chunks[window_start:window_end]
        
        # Extract context (excluding the current chunk)
        context_chunks = [c for j, c in enumerate(window) if j != i - window_start]
        context_text = " ".join(context_chunks)
        
        # Prepare metadata
        metadata = {
            "chunk_id": i,
            "total_chunks": len(base_chunks),
            "chunk_size": len(chunk),
            "window_start_idx": window_start,
            "window_end_idx": window_end - 1,
            "has_context": len(context_chunks) > 0
        }
        
        # Handle context based on whether summarization is enabled
        if context_chunks and summarize:
            try:
                # Invoke the LCEL chain directly with the context string
                context_summary = summary_chain.invoke({"text": context_text})
                
                metadata["context"] = context_summary
                metadata["context_type"] = "summary"
                
                # Create enriched text
                enriched_text = f"Context: {context_summary}\n\nContent: {chunk}"
                
            except Exception as e:
                print(f"Summarization error for chunk {i}: {e}")
                # Fallback to raw context
                metadata["context"] = context_text
                metadata["context_type"] = "raw_text"
                metadata["summary_error"] = str(e)
                enriched_text = f"Context: {context_text}\n\nContent: {chunk}"
        
        elif context_chunks:
            # Use raw context without summarization
            metadata["context"] = context_text
            metadata["context_type"] = "raw_text"
            enriched_text = f"Context: {context_text}\n\nContent: {chunk}"
        
        else:
            # No context available
            metadata["context"] = ""
            metadata["context_type"] = "none"
            enriched_text = chunk
        
        # Create Document object
        doc = Document(
            page_content=enriched_text,
            metadata=metadata
        )
        
        enriched_documents.append(doc)
    
    return enriched_documents

# Mock implementation for testing without Databricks
class MockChatModel:
    """Mock LLM for testing without Databricks."""
    def __init__(self, **kwargs):
        self.kwargs = kwargs
    
    def invoke(self, input_text):
        """Generate a simple summary based on the first few words."""
        if isinstance(input_text, list) and hasattr(input_text[0], 'page_content'):
            text = input_text[0].page_content
        else:
            text = str(input_text)
        
        # Extract first sentence or first 50 characters for mock summary
        first_sentence = text.split('.')[0]
        return f"Summary: {first_sentence[:100]}..."

def perform_context_enriched_chunking_mock(document, chunk_size=500, chunk_overlap=50, 
                                          window_size=1):
    """
    Mock implementation of context-enriched chunking for testing without Databricks.
    """
    # Create text splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    # Split the document into base chunks
    base_chunks = splitter.split_text(document)
    print(f"Document split into {len(base_chunks)} base chunks")
    
    # Create a mock summarization function
    def mock_summarize(text):
        first_sentence = text.split('.')[0]
        return f"Summary: {first_sentence[:100]}..."
    
    # Process chunks with contextual windows
    enriched_documents = []
    for i, chunk in enumerate(base_chunks):
        # Define window around current chunk
        window_start = max(0, i - window_size)
        window_end = min(len(base_chunks), i + window_size + 1)
        window = base_chunks[window_start:window_end]
        
        # Extract context (excluding the current chunk)
        context_chunks = [c for j, c in enumerate(window) if j != i - window_start]
        context_text = " ".join(context_chunks)
        
        # Generate mock summary for context
        if context_chunks:
            context_summary = mock_summarize(context_text)
            metadata = {
                "chunk_id": i,
                "total_chunks": len(base_chunks),
                "context": context_summary,
                "context_type": "summary"
            }
            enriched_text = f"Context: {context_summary}\n\nContent: {chunk}"
        else:
            metadata = {
                "chunk_id": i,
                "total_chunks": len(base_chunks),
                "context": "",
                "context_type": "none"
            }
            enriched_text = chunk
        
        # Create Document object
        doc = Document(
            page_content=enriched_text,
            metadata=metadata
        )
        
        enriched_documents.append(doc)
    
    return enriched_documents

# Example usage
if __name__ == "__main__":

    with open("docs/chunking/fixedSizeChunk/rag_chunking_test_doc.md", "r", encoding="utf-8") as file:
        document = file.read()
    
    # Use mock version for testing without Databricks
    print("Using mock implementation for testing...")
    enriched_docs = perform_context_enriched_chunking_mock(
        document,
        chunk_size=500,
        chunk_overlap=50,
        window_size=1
    )
    
    # # Display results
    # print("\n----- CHUNKING RESULTS -----")
    # print(f"Total enriched chunks: {len(enriched_docs)}")
    
    # # Print an example chunk with its context
    # print("\n----- EXAMPLE ENRICHED CHUNK -----")
    # middle_chunk_idx = len(enriched_docs) // 2
    # example_chunk = enriched_docs[middle_chunk_idx]
    # print(f"Chunk {middle_chunk_idx} with context:")
    # print("-" * 40)
    # print(example_chunk.page_content)
    # print("-" * 40)
    # print(f"Metadata: {example_chunk.metadata}")
    
    # print("\nTo use with Databricks:")
    # print("1. Replace 'perform_context_enriched_chunking_mock' with 'perform_context_enriched_chunking'")
    # print("2. Ensure your Databricks endpoint is correctly configured")
    # print("3. Store documents with context in Delta table")
    # print("4. Create embeddings that include the context information")
    output_path = "docs/chunking/context_enrich_chunking/chunk_output.txt"
    try:
        with open(output_path, "w", encoding="utf-8") as output_file:
            for i, doc in enumerate(enriched_docs):
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