import re
import nltk
from nltk.tokenize import sent_tokenize
from langchain_core.documents import Document
from langchain_text_splitters import TextSplitter
import json

# You might need to download NLTK resources in Databricks
# This can be run once at the start of your notebook
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class AdaptiveTextSplitter(TextSplitter):
    """
    Custom text splitter that adapts chunk sizes based on text complexity.
    """
    
    def __init__(
        self,
        min_chunk_size: int = 300,
        max_chunk_size: int = 1000,
        min_chunk_overlap: int = 30,
        max_chunk_overlap: int = 150,
        complexity_measure: str = "lexical_density",
        length_function=len,
        **kwargs
    ):
        """Initialize with parameters for adaptive chunking.
        
        Args:
            min_chunk_size: Minimum size for chunks with highest complexity
            max_chunk_size: Maximum size for chunks with lowest complexity
            min_chunk_overlap: Minimum overlap between chunks
            max_chunk_overlap: Maximum overlap for complex chunks
            complexity_measure: Method to measure text complexity 
                                (options: "lexical_density", "sentence_length", "combined")
            length_function: Function to measure text length
        """
        super().__init__(**kwargs)
        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size
        self.min_chunk_overlap = min_chunk_overlap
        self.max_chunk_overlap = max_chunk_overlap
        self.complexity_measure = complexity_measure
        self.length_function = length_function
    
    def analyze_complexity(self, text: str) -> float:
        """
        Analyze the complexity of text and return a score between 0 and 1.
        Higher score means more complex text.
        """
        if not text.strip():
            return 0.0
        
        # Lexical density: ratio of unique words to total words
        if self.complexity_measure == "lexical_density" or self.complexity_measure == "combined":
            words = re.findall(r'\b\w+\b', text.lower())
            if not words:
                lex_density = 0
            else:
                unique_words = set(words)
                lex_density = len(unique_words) / len(words)
            
            # Normalize between 0 and 1, assuming max lex_density of 0.8
            lex_density = min(1.0, lex_density / 0.8)
        else:
            lex_density = 0
        
        # Average sentence length as a complexity factor
        if self.complexity_measure == "sentence_length" or self.complexity_measure == "combined":
            # Tokenize into sentences. This safely handles both single sentences 
            # (from split_text) and multi-sentence chunks (from create_documents).
            sentences = sent_tokenize(text)

            if not sentences:
                sent_complexity = 0
            else:
                avg_length = sum(len(s) for s in sentences) / len(sentences)
                # Normalize with assumption that 200 char is complex
                sent_complexity = min(1.0, avg_length / 200)
        else:
            sent_complexity = 0
        
        # Combined measure
        if self.complexity_measure == "combined":
            return (lex_density + sent_complexity) / 2
        elif self.complexity_measure == "lexical_density":
            return lex_density
        else:  # sentence_length
            return sent_complexity
    
    def split_text(self, text: str) -> list[str]:
        """Split text into chunks based on adaptive sizing."""
        if not text:
            return []
            
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = []
        current_size = 0
        current_complexity = 0.5  # Start with medium complexity
        
        for sentence in sentences:
            sentence_len = self.length_function(sentence)
            
            # Skip empty sentences
            if sentence_len == 0:
                continue
                
            # Analyze sentence complexity
            sentence_complexity = self.analyze_complexity(sentence)
            
            # Update running complexity average
            if current_chunk:
                current_complexity = (current_complexity + sentence_complexity) / 2
            else:
                current_complexity = sentence_complexity
                
            # Calculate target size based on complexity
            # More complex text gets smaller chunks
            target_size = self.max_chunk_size - (current_complexity * (self.max_chunk_size - self.min_chunk_size))
            
            # Calculate adaptive overlap
            target_overlap = self.min_chunk_overlap + (current_complexity * (self.max_chunk_overlap - self.min_chunk_overlap))
            
            # Check if adding this sentence would exceed the target size
            if current_size + sentence_len > target_size and current_chunk:
                # Join current chunk and add to results
                chunks.append(" ".join(current_chunk))
                
                # Start new chunk with overlap
                overlap_size = 0
                overlap_chunk = []
                
                # Add sentences from the end of the previous chunk for overlap
                for prev_sentence in reversed(current_chunk):
                    if overlap_size + self.length_function(prev_sentence) <= target_overlap:
                        overlap_chunk.insert(0, prev_sentence)
                        overlap_size += self.length_function(prev_sentence)
                    else:
                        break
                
                # Start new chunk with the overlap plus the current sentence
                current_chunk = overlap_chunk + [sentence]
                current_size = sum(self.length_function(s) for s in current_chunk)
            else:
                # Add sentence to current chunk
                current_chunk.append(sentence)
                current_size += sentence_len
        
        # Add the last chunk if it exists
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks
    
    def create_documents(self, texts: list[str], metadatas: list[dict] = None) -> list[Document]:
        """Create Document objects with complexity metadata."""
        documents = []
        
        for i, text in enumerate(texts):
            # Calculate text complexity for metadata
            complexity = self.analyze_complexity(text)
            
            # Create base metadata
            metadata = {
                "chunk_id": i,
                "total_chunks": len(texts),
                "chunk_size": self.length_function(text),
                "chunk_type": "adaptive",
                "text_complexity": round(complexity, 3),
            }
            
            # Add any additional metadata
            if metadatas and i < len(metadatas):
                metadata.update(metadatas[i])
            
            doc = Document(page_content=text, metadata=metadata)
            documents.append(doc)
        
        return documents

def perform_adaptive_chunking(document, min_size=300, max_size=1000, 
                              min_overlap=30, max_overlap=150,
                              complexity_measure="combined"):
    """
    Performs adaptive chunking on a document, with chunk size varying by text complexity.
    """
    # Create the adaptive text splitter
    splitter = AdaptiveTextSplitter(
        min_chunk_size=min_size,
        max_chunk_size=max_size,
        min_chunk_overlap=min_overlap,
        max_chunk_overlap=max_overlap,
        complexity_measure=complexity_measure
    )
    
    # Split the document into chunks
    chunks = splitter.split_text(document)
    print(f"Document split into {len(chunks)} adaptive chunks")
    
    # Create Document objects with complexity metadata
    documents = splitter.create_documents(chunks)
    
    # Add additional metrics
    chunk_sizes = [doc.metadata["chunk_size"] for doc in documents]
    if chunk_sizes:
        avg_size = sum(chunk_sizes) / len(chunk_sizes)
        for doc in documents:
            doc.metadata["avg_chunk_size"] = round(avg_size, 1)
            doc.metadata["size_vs_avg"] = round(doc.metadata["chunk_size"] / avg_size, 2)
    
    return documents


# Example usage with Databricks integration
if __name__ == "__main__":
    
    with open("docs/chunking/fixedSizeChunk/rag_chunking_test_doc.md", "r", encoding="utf-8") as file:
        document = file.read()

    # Process with adaptive chunking
    chunked_docs = perform_adaptive_chunking(
        document,
        min_size=300,
        max_size=1000,
        complexity_measure="combined"
    )
    
    # Display results
    print("\n----- CHUNKING RESULTS -----")
    print(f"Total adaptive chunks: {len(chunked_docs)}")
    
    # Calculate complexity stats
    complexities = [doc.metadata["text_complexity"] for doc in chunked_docs]
    sizes = [doc.metadata["chunk_size"] for doc in chunked_docs]
    
    print("\n----- COMPLEXITY ANALYSIS -----")
    print(f"Average complexity: {sum(complexities)/len(complexities):.3f}")
    print(f"Min complexity: {min(complexities):.3f}")
    print(f"Max complexity: {max(complexities):.3f}")
    
    print("\n----- SIZE ANALYSIS -----")
    print(f"Average chunk size: {sum(sizes)/len(sizes):.1f} characters")
    print(f"Min chunk size: {min(sizes)} characters")
    print(f"Max chunk size: {max(sizes)} characters")
    
    # Print examples of high and low complexity chunks
    high_complex_idx = complexities.index(max(complexities))
    low_complex_idx = complexities.index(min(complexities))
    
    print("\n----- HIGHEST COMPLEXITY CHUNK -----")
    print(f"Complexity: {chunked_docs[high_complex_idx].metadata['text_complexity']}")
    print(f"Size: {chunked_docs[high_complex_idx].metadata['chunk_size']} characters")
    print("-" * 40)
    print(chunked_docs[high_complex_idx].page_content[:200] + "...")
    
    print("\n----- LOWEST COMPLEXITY CHUNK -----")
    print(f"Complexity: {chunked_docs[low_complex_idx].metadata['text_complexity']}")
    print(f"Size: {chunked_docs[low_complex_idx].metadata['chunk_size']} characters")
    print("-" * 40)
    print(chunked_docs[low_complex_idx].page_content[:200] + "...")
    
    # For integration with Databricks Vector Search
    print("\nTo integrate with Databricks:")
    print("1. Create embeddings using DatabricksEmbeddings")
    print("2. Store documents and embeddings in a Delta table")
    print("3. Create a Vector Search index with complexity filtering capability")
    print("4. During retrieval, consider filtering by complexity for specific use cases")
    
    # Clean output written to file once at the end
    output_path = "docs/chunking/adaptiveChunking/chunk_output.txt"
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