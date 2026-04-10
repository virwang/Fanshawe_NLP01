# brain.py
import numpy as np
import pickle
import os
import re
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class MaintenanceBrain:
    def __init__(self, vector_path='expert_vectors.npy', answer_path='expert_answers.pkl'):
        # Load the NLP model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Load the DataFrame containing expert answers and their cluster IDs
        if not os.path.exists(answer_path):
            raise FileNotFoundError(f"File {answer_path} not found")
        self.df_answers = pd.read_pickle(answer_path)

        # Load the expert vectors from the .npy file
        if not os.path.exists(vector_path):
            raise FileNotFoundError(f"File {vector_path} not found")
        self.expert_vectors = np.load(vector_path)
        
        # Define cluster map:
        self.topic_map = {
        0: "CLI & Remote Admin",
            1: "Hardware & Media Drivers",
            2: "Package & Software Operations",
            3: "Disk & Boot Management",
            4: "Desktop & System Tweaks"
            }
            
            
        with open(answer_path, 'rb') as f:
            self.expert_answers = pickle.load(f)

        # INTERNAL KNOWLEDGE BASE (The "basic_kb")
        # Handles fundamental commands that might be missing from the expert logs.
        self.basic_kb = {
            "list user": "To see all users: `cat /etc/passwd`. For logged-in users: `who` or `w`.",
            "show user": "To see all users: `cat /etc/passwd`. For logged-in users: `who` or `w`.",
            "check user": "To see all users: `cat /etc/passwd`. For logged-in users: `who` or `w`.",
            "permission": "Use `chmod` to change permissions (e.g., `chmod 755 filename`).",
            "disk space": "Use `df -h` to check free space or `lsblk` for partitions.",
            "reboot": "Run `sudo reboot` or `sudo shutdown -r now` to restart.",
            "install": "Run `sudo apt update && sudo apt install [package_name]`."
        }

    def _extract_actionable_steps(self, text):
        """
        Extracts terminal commands from expert logs. 
        Fixed to avoid UnboundLocalError.
        """
        # Pattern to find technical commands
        cmd_pattern = r'(sudo|apt|chmod|chown|systemctl|cat /etc/|ls -|grep|tail -f|/var/log)'
        lines = re.split(r'[\n;]', text)
        
        # Filter lines that contain commands
        actions = [line.strip() for line in lines if re.search(cmd_pattern, line)]
        
        if actions:
            # Define 'step' ONLY if we found an action
            step = actions[0]
            step = re.sub(r'^(try|maybe|just|you can)\s+', '', step, flags=re.IGNORECASE)
            
            # UI Polish: If the command is basically the whole text, don't repeat it
            if len(step) >= len(text) * 0.8:
                return f"**Actionable Step:** `{step}`"
            
            return f"**Actionable Step:** `{step}`\n\n**Expert Context:** {text}"
        
        # Fallback: If no command is found, just return the text normally
        return text.capitalize()


    # def _extract_actionable_steps(self, text):
    #     """
    #     Extracts terminal commands from expert logs to provide a direct answer.
    #     """
    #     # Matches common Linux commands or file paths
    #     cmd_pattern = r'(sudo|apt|chmod|chown|systemctl|cat /etc/|ls -|grep|df -h)'
    #     lines = re.split(r'[\n;]', text)
        
    #     # Priority: find lines containing actual commands
    #     actions = [line.strip() for line in lines if re.search(cmd_pattern, line)]
        
    #     if actions:
    #         step = actions[0]
    #         if len(step) >= len(text) * 0.8:
    #             return f"**Actionable Step:** `{step}`"
        
    #     # If the original text is long, show the context for reference
    #     return f"**Actionable Step:** `{step}`\n\n**Expert Context:** {text}"
        
    #     return text

    def search(self, user_query, threshold=0.60):
        """
        Hybrid search: Checks basic_kb first, then the vector database.
        """
        query_lower = user_query.lower()

        # 1. KEYWORD INTERCEPTION (Quick fix for basic questions)
        for key, value in self.basic_kb.items():
            if key in query_lower:
                return {
                    "found": True,
                    "confidence": 1.0, 
                    "answer": value,
                    "topic": "General Support"
                }

        # 2. SEMANTIC SEARCH (For complex expert logs)
        query_vec = self.model.encode([user_query])
        sims = cosine_similarity(query_vec, self.expert_vectors)[0]
        
        best_idx = np.argmax(sims)
        best_score = similarities = sims[best_idx]
        
        if best_score >= threshold:
            matched_row = self.df_answers.iloc[best_idx]
            cluster_id = matched_row['cluster_id']
            raw_answer = matched_row['answer']

            return {
                "found": True, 
                "confidence": float(best_score), 
                "answer": self._extract_actionable_steps(raw_answer),
                "topic": self.topic_map.get(cluster_id, "Specialist Insight") # Get topic name from cluster ID, default to "Specialist Insight"
            }
        
        return {
            "found": False, 
            "confidence": best_score, 
            "answer": "No confident match found. Try using keywords like 'sudo' or 'permissions'.",
            "topic": "Unclassified"

        }