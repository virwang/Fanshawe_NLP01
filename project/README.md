# Project: Ops Knowledge Base AI (FalconOps)

This folder contains project materials for the Fanshawe NLP01 course (Winter 2026).

## Overview

**FalconOps** is an advanced IT support tool designed to transform raw, unstructured expert communication logs into a searchable knowledge base. By leveraging **Natural Language Processing (NLP)**, the system assists system administrators in retrieving technical solutions from over 8,000 historical expert records. Unlike traditional keyword-based searches, FalconOps understands the context and intent behind user queries, providing a more reliable and efficient troubleshooting experience.

## Key Features

- **Intent Recognition:** Understands technical synonyms (e.g., "modify permissions" vs. "chown")
- **Semantic Matching:** Uses cosine similarity to identify the closest expert response to a user's query
- **Fail-Safe Mechanism:** Automatically triggers an escalation protocol if no high-confidence solution is found
- **Confidence Thresholding:** Blocks responses with confidence scores below 0.75, preventing irrelevant advice
- **Optimized Performance:** Uses pre-calculated vector caches to ensure sub-second response times

## Technical Architecture

The system is built upon a **Decoupled Architecture**, separating data processing from the user interface to ensure modularity and scalability:

### Data Processing Pipeline
- **Sentence Embeddings:** Utilizes the `all-MiniLM-L6-v2` Transformer model to convert text instructions into high-dimensional vectors
- **Vector Storage:** Efficient storage of 8,000+ embeddings using `.npy` format for rapid mathematical comparison

### Logic & Reasoning Engine (brain.py)
- **Semantic Matching:** Uses **Cosine Similarity** for intelligent query matching
- **Confidence Thresholding:** Critical safety feature that prevents low-confidence responses
- **Post-Processing:** Filters informal language and formats output into professional advisory tone

### Interface Layer (app.py)
- Streamlined dashboard built with **Streamlit**
- Real-time feedback and clear escalation path to human experts (Fanshawe Tech Support)

## Contents

- Jupyter notebooks for course assignments and experiments
- Supporting data and notes related to the projects
- Data processing pipelines for NLP model training and evaluation
- Integration with pre-trained transformer models

## How to Run

1. **Install Python** (recommend 3.8+) and pip

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install required packages** (if requirements.txt exists)
   ```bash
   pip install -r requirements.txt
   ```

4. **Open the notebooks with JupyterLab or Jupyter Notebook**
   ```bash
   jupyter lab
   ```

## Dependencies

Key libraries used in this project:
- `sentence-transformers` - For sentence embeddings
- `faiss` - For efficient vector similarity search
- `scikit-learn` - For clustering and similarity metrics
- `pandas` & `numpy` - For data manipulation
- `streamlit` - For the web interface
- `matplotlib` & `seaborn` - For visualization

## Future Work

While the current version focuses on semantic retrieval, future iterations will explore:
- Enhanced multi-turn conversation support
- Integration with live ticketing systems
- Advanced clustering for solution categorization
- Real-time model updates based on new expert interactions

---

For more detailed instructions or additional information, please refer to the individual notebook documentation.
