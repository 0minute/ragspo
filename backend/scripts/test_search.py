"""Script to test document search functionality.

This script provides a simple CLI interface to test the RAG search functionality.
"""

import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.rag.search import build_answer_with_sources


def main() -> None:
    """Run interactive search test.
    
    This function allows testing the search functionality from the command line.
    """
    print("=" * 60)
    print("RAG-SPO Document Search Test")
    print("=" * 60)
    print("\nType your query (or 'quit' to exit)")
    print("-" * 60)
    
    while True:
        try:
            # Get query from user
            query = input("\nQuery: ").strip()
            
            if not query:
                continue
            
            if query.lower() in ["quit", "exit", "q"]:
                print("Exiting...")
                break
            
            # Perform search
            print("\nSearching...")
            response = build_answer_with_sources(query, top_k=5)
            
            # Display results
            print("\n" + "=" * 60)
            print("ANSWER:")
            print("-" * 60)
            print(response.answer)
            
            if response.sources:
                print("\n" + "=" * 60)
                print("SOURCES:")
                print("-" * 60)
                for idx, source in enumerate(response.sources, 1):
                    print(f"\n{idx}. {source.file_title} (chunk {source.chunk_index})")
                    print(f"   Score: {source.score:.4f}")
                    print(f"   URL: {source.download_url}")
            else:
                print("\nNo sources found.")
            
            print("\n" + "=" * 60)
            
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"\n✗ Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    # Check if query was provided as command line argument
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(f"Query: {query}\n")
        
        # try:
        response = build_answer_with_sources(query, top_k=5)
        
        print("ANSWER:")
        print("-" * 60)
        print(response.answer)
        
        if response.sources:
            print("\nSOURCES:")
            print("-" * 60)
            for idx, source in enumerate(response.sources, 1):
                print(f"{idx}. {source.file_title} (chunk {source.chunk_index}, score: {source.score:.4f})")
        # except Exception as e:
        #     print(f"Error: {e}")
        #     sys.exit(1)
    else:
        # Run interactive mode
        main()

