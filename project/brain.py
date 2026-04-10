# brain.py
import numpy as np
import pickle
import os
<<<<<<< HEAD
import re
import pandas as pd
=======
>>>>>>> parent of 1ae06cc (update the search logic and add the basic knowkedge answer)
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class MaintenanceBrain:
    def __init__(self, vector_path='expert_vectors.npy', answer_path='expert_answers.pkl'):
        """
        Initializes the AI Logic: Loads NLP model and expert data.
        """
        # Load the sentence transformer model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
<<<<<<< HEAD
        self.df_answers = pd.read_pickle(answer_path)

        # Define cluster map:
        self.topic_map = {
        0: "System Permissions",
        1: "Network Configuration",
        2: "Package Installation",
        3: "User Account Management",
        4: "Hardware Drivers",
        5: "Display & Desktop",
        6: "Security & Firewall",
        7: "Disk & Storage",
        8: "Boot & Kernel",
        9: "General Support"
    }



        # Load data assets
=======
        
        # Security check for data files
>>>>>>> parent of 1ae06cc (update the search logic and add the basic knowkedge answer)
        if not os.path.exists(vector_path) or not os.path.exists(answer_path):
            raise FileNotFoundError("System assets (.npy or .pkl) are missing!")
            
        self.expert_vectors = np.load(vector_path)
        with open(answer_path, 'rb') as f:
            self.expert_answers = pickle.load(f)

        # --- REFINEMENT LOGIC ---
        # Map fragmented expert notes to professional sentences
        self.refinement_map = {
            "chown the files": "Update the file ownership using the 'chown' command to ensure proper permissions in the new directory.",
            "tail -f": "Monitor the log files in real-time by executing the 'tail -f' command.",
            "sudo service gdm stop": "Properly terminate the display manager using 'sudo service gdm stop' before making changes."
        }

    def _post_process(self, raw_text):
        """
        Internal method to polish the raw database text.
        """
        # 1. Check for predefined professional phrases
        for key, refined in self.refinement_map.items():
            if key.lower() in raw_text.lower():
                return refined
        
        # 2. General formatting (Capitalize and add period)
        processed = raw_text.strip().capitalize()
        if not processed.endswith(('.', '!', '?')):
            processed += '.'
        return processed

    def search(self, user_query, threshold=0.75):
        """
        Core search function: Math stays here, UI stays away.
        """
        query_vec = self.model.encode([user_query])
        similarities = cosine_similarity(query_vec, self.expert_vectors)[0]
        
        best_idx = np.argmax(similarities)
        best_score = similarities[best_idx]
        
        if best_score >= threshold:
            raw_answer = self.expert_answers[best_idx]
            return {
                "found": True, 
                "confidence": best_score, 
                "answer": self._post_process(raw_answer) # Output is now polished
            }
        return {"found": False, "confidence": best_score, "answer": None}