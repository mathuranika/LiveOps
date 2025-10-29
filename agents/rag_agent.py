# agents/rag_agent.py
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import google.generativeai as genai

class RAGAgent:
    def __init__(self, master_df):
        self.df = master_df.copy().fillna('')
        # Combine relevant fields for retrieval
        text_cols = [c for c in ['order_id','customer_id','customer_name','issue_category',
                                 'feedback_text','status','route','promised_time',
                                 'actual_time','delay_minutes','delivery_cost']
                     if c in self.df.columns]
        if not text_cols:
            text_cols = self.df.columns.tolist()
        self.df['doc'] = self.df[text_cols].astype(str).agg(' | '.join, axis=1)

        # TF-IDF retriever
        self.vectorizer = TfidfVectorizer(max_features=2000, stop_words='english')
        self.tfidf = self.vectorizer.fit_transform(self.df['doc'].values)

        # Configure Gemini
        self.gemini_key = os.environ.get("GEMINI_API_KEY")
        if self.gemini_key:
            genai.configure(api_key=self.gemini_key)
            self.model = genai.GenerativeModel("gemini-2.5-flash")
        else:
            self.model = None

    def retrieve(self, query, top_k=3):
        qv = self.vectorizer.transform([query])
        cos_sim = linear_kernel(qv, self.tfidf).flatten()
        idx = cos_sim.argsort()[::-1][:top_k]
        results = []
        for i in idx:
            score = float(cos_sim[i])
            row = self.df.iloc[i].to_dict()
            results.append({"score": score, "row": row})
        return results

    def generate_answer(self, query, retrieved, use_llm=True):
        snippets = "\n\n".join([
            f"Score: {r['score']:.3f} | Order {r['row'].get('order_id','N/A')} -> {r['row'].get('doc','')[:500]}"
            for r in retrieved
        ])

        if self.model and use_llm:
            prompt = f"""
You are NexGen's AI logistics assistant.
User query: {query}

Context (from database):
{snippets}

Provide a concise and factual explanation.
Include order IDs and summarise causes of delays or complaints clearly.
"""
            try:
                response = self.model.generate_content(prompt)
                return {
                    "answer": response.text.strip(),
                    "used_llm": True
                }
            except Exception as e:
                return {
                    "answer": f"(Gemini API failed: {e})\nFallback:\n{self.simple_synthesis(query, retrieved)}",
                    "used_llm": False
                }
        else:
            return {"answer": self.simple_synthesis(query, retrieved), "used_llm": False}

    def simple_synthesis(self, query, retrieved):
        lines = []
        for r in retrieved:
            row = r['row']
            order_id = row.get('order_id','N/A')
            reason = row.get('issue_category') or row.get('feedback_text') or row.get('status') or row.get('doc','')[:150]
            lines.append(f"- Order {order_id}: likely cause → {reason} (score {r['score']:.2f})")
        return "Based on the data, possible causes:\n" + "\n".join(lines)
