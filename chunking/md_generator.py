import random
import string

# Configuration
OUTPUT_FILENAME = "docs/chunking/fixedSizeChunk/rag_chunking_test_doc.md"
NUM_SECTIONS = 5
MAX_PARAGRAPHS_PER_SECTION = 4
MAX_SENTENCES_PER_PARAGRAPH = 8

# Vocabulary for generating synthetic text
WORDS = ["data", "system", "model", "network", "cloud", "user", "process", "server", "application", "database", 
         "api", "infrastructure", "security", "latency", "throughput", "algorithm", "deployment", "container"]
VERBS = ["manages", "optimizes", "processes", "transmits", "stores", "authenticates", "computes", "analyzes"]
ADJECTIVES = ["distributed", "scalable", "secure", "efficient", "redundant", "automated", "virtualized", "hybrid"]

# Target facts to inject for retrieval testing ("Needles")
TARGET_FACTS = [
    "The primary database password is 'Tr0ub4dour&3'.",
    "Project Alpha is scheduled to launch on October 12th, 2026.",
    "The emergency shutoff code for the main reactor is 881-ZULU.",
    "CEO Jane Doe announced a 15% increase in Q3 revenue.",
    "The legacy mainframe uses COBOL and is hosted in the basement server room."
]

def generate_sentence():
    """Generates a random technical-sounding sentence."""
    length = random.randint(5, 12)
    sentence = [random.choice(WORDS) if i % 2 == 0 else random.choice(ADJECTIVES) for i in range(length)]
    sentence.insert(1, random.choice(VERBS))
    return " ".join(sentence).capitalize() + ". "

def generate_paragraph():
    """Generates a paragraph of random sentences."""
    num_sentences = random.randint(3, MAX_SENTENCES_PER_PARAGRAPH)
    return "".join(generate_sentence() for _ in range(num_sentences))

def generate_list(is_numbered=False):
    """Generates a markdown list."""
    num_items = random.randint(3, 6)
    list_text = ""
    for i in range(1, num_items + 1):
        prefix = f"{i}. " if is_numbered else "* "
        list_text += f"{prefix}{generate_sentence().strip()}\n"
    return list_text + "\n"

def main():
    with open(OUTPUT_FILENAME, "w", encoding="utf-8") as f:
        f.write("# RAG Chunking Test Document\n\n")
        f.write("This document contains synthetic data and specific target facts to test retrieval and chunking strategies.\n\n")
        
        fact_index = 0
        
        for section in range(1, NUM_SECTIONS + 1):
            # Generate H2 Header
            f.write(f"## Section {section}: {random.choice(ADJECTIVES).capitalize()} {random.choice(WORDS).capitalize()}\n\n")
            
            num_paragraphs = random.randint(2, MAX_PARAGRAPHS_PER_SECTION)
            
            for p in range(num_paragraphs):
                # Inject a target fact randomly into some paragraphs
                if fact_index < len(TARGET_FACTS) and random.random() > 0.6:
                    paragraph_text = generate_paragraph()
                    # Insert the fact in the middle of the paragraph
                    insert_point = len(paragraph_text) // 2
                    f.write(f"{paragraph_text[:insert_point]} [TARGET FACT: {TARGET_FACTS[fact_index]}] {paragraph_text[insert_point:]}\n\n")
                    fact_index += 1
                else:
                    f.write(f"{generate_paragraph()}\n\n")
            
            # Add a list to test how the chunker handles list elements
            if random.random() > 0.5:
                f.write(f"### Key Components of Section {section}\n\n")
                f.write(generate_list(is_numbered=random.choice([True, False])))
                
            f.write("---\n\n") # Markdown separator
            
    print(f"✅ Generated '{OUTPUT_FILENAME}' successfully.")
    print(f"Injected {min(fact_index, len(TARGET_FACTS))} target facts for retrieval testing.")

if __name__ == "__main__":
    main()