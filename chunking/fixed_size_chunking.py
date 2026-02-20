from langchain_text_splitters import CharacterTextSplitter
from langchain_core.documents import Document

def perform_fixed_size_chunking(document, chunk_size=1000, chunk_overlap=200):
    """
        Splits a text document into fixed-size chunks with specified character overlap.
        
        This function uses LangChain's CharacterTextSplitter, which splits based on 
        a defined separator (defaulting to double newlines). 
        
        Note on Overlap Behavior: 
        LangChain only overlaps whole "pieces" of text (defined by the separator). 
        If a single indivisible piece of text is larger than the allowed `chunk_overlap`, 
        the splitter will skip the overlap entirely for that boundary.

        Args:
            document (str): The raw text document to be processed.
            chunk_size (int, optional): The maximum length of each chunk in characters. 
                Defaults to 1000.
            chunk_overlap (int, optional): The target number of overlapping characters 
                between consecutive chunks to preserve context. Defaults to 200.

        Returns:
            list[Document]: A list of LangChain Document objects, each containing the 
                chunked text (`page_content`) and associated metadata.
    """
    # Create the text splitter with optimal parameters
    text_splitter = CharacterTextSplitter(
        separator="\n\n", #only one separator allowed
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    
    # Split the text into chunks
    chunks = text_splitter.split_text(document)
    print(f"Document split into {len(chunks)} chunks")
    
    documents = []
    for i, chunk in enumerate(chunks):
        # --------------------------------------------------------------------
        # WHY WE USE THE DOCUMENT WRAPPER HERE:
        # 1. Context Retention: If we only embedded raw strings, the AI wouldn't 
        #    know where the text came from.
        # 2. Metadata Filtering: Wrapping it allows us to attach metadata. Later, 
        #    we can tell the vector database: "Search for 'passwords', BUT ONLY 
        #    in chunks where chunk_type is 'fixed-size'."
        # 3. Ecosystem Compatibility: Almost all LangChain tools (embedding models, 
        #    vector stores, LLM chains) strictly require a list of Document objects.
        # --------------------------------------------------------------------
        doc = Document(
            page_content=chunk, # The actual chunk of text
            metadata={          # The context data attached to this specific text
                "chunk_id": i,
                "total_chunks": len(chunks),
                "chunk_size": len(chunk),
                "chunk_type": "fixed-size"
            }
        )
        documents.append(doc)
    
    return documents

# Example usage
if __name__ == "__main__":
    

    with open("docs/chunking/fixed_size_chunk/rag_chunking_test_doc.md", "r", encoding="utf-8") as file:
        document = file.read()
    
    # Process with fixed-size chunking
    chunked_docs = perform_fixed_size_chunking(
        document,
        chunk_size=1000,
        chunk_overlap=200
    )
    # LangChain only overlaps whole "pieces" of text. If a single piece of text is larger than your allowed overlap, it skips the overlap entirely.
    
    # For integration with Databricks Vector Search
    print("\nThese documents are ready for embedding and storage in Databricks Vector Search")
    print("Example next steps:")
    print("1. Create embeddings using the Databricks embedding endpoint")
    print("2. Store documents and embeddings in Delta table")
    print("3. Create Vector Search index for retrieval")


# Open a new file in write mode ("w")
with open("docs/chunking/fixed_size_chunk/chunk_output.txt", "w", encoding="utf-8") as output_file:
    
    for i, doc in enumerate(chunked_docs):
        # Write the chunk header
        output_file.write(f"--- Chunk {i} ---\n\n")
        
        # Write the actual chunk text
        output_file.write(doc.page_content)
        
        # Add some blank lines between chunks for readability
        output_file.write("\n\n")

print("All chunks have been successfully saved to 'chunk_output.txt'")