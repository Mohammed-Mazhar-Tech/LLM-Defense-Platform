import re
import pickle
import json


# -----------------------------
# 1. RULE BASED FIREWALL
# -----------------------------
class RuleBasedFirewall:

    def __init__(self):

        self.patterns = [
            r"ignore\s+previous",
            r"ignore\s+all\s+instructions",
            r"bypass\s+.*rules",
            r"bypass\s+.*rule",
            r"bypass\s+.*restriction",
            r"act\s+(as|like)\s+.*ai",
            r"pretend\s+you\s+are",
            r"roleplay",
            r"reveal\s+.*prompt",
            r"override\s+.*rule",
            r"disable\s+.*safety",
            r"jailbreak",
        ]
    def validate(self, prompt):
        text = prompt.lower()

        danger_words = [
            "bypass",
            "override",
            "ignore",
            "act",
            "pretend",
            "jailbreak",
            "disable"
        ]

    # Check simple danger words
        for word in danger_words:
            if word in text:
                return False, "Blocked by firewall (suspicious instruction)"

    # Check regex attack patterns
        for pattern in self.patterns:
            if re.search(pattern, text):
                return False, "Blocked by firewall (prompt injection detected)"

        return True, "Passed firewall"


# -----------------------------
# 2. ML CLASSIFIER
# -----------------------------
class MLClassifier:

    def __init__(self):

        import pickle

        with open("models/classifier.pkl", "rb") as f:
            self.vectorizer, self.model = pickle.load(f)

    def classify(self, prompt):

    # Convert prompt to vector
        vec = self.vectorizer.transform([prompt])

    # Get probability scores
        probs = self.model.predict_proba(vec)[0]

        safe_prob = probs[0]
        malicious_prob = probs[1]

        risk_score = (malicious_prob - safe_prob + 1) / 2 * 100

        if malicious_prob > 0.90:
            return False, risk_score, "Malicious prompt detected"

        return True, risk_score, "Prompt safe"
    
# -----------------------------
# 3. IRS (PROMPT CLEANING)
# -----------------------------
class IRS:

    def refine(self, prompt):

        prompt = re.sub(r'[!]{3,}', '!', prompt)
        prompt = re.sub(r'\s+', ' ', prompt)

        return prompt.strip()


# -----------------------------
# 4. RAG SYSTEM
# -----------------------------
class RAG:

    def __init__(self):

        with open("rag/knowledge.json") as f:
            self.kb = json.load(f)

    def retrieve(self, prompt):

        p = prompt.lower()

        for key, value in self.kb.items():
            if key in p:
                return value

        return "General knowledge context."


# -----------------------------
# 5. LLM
# -----------------------------
import ollama

def generate_llm_response(prompt):

    response = ollama.chat(
        model="llama3:8b-instruct-q4_0",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


# -----------------------------
# 6. RESPONSE SHIELD
# -----------------------------
class ResponseShield:

    patterns = [
        r"how\s+to\s+hack",
        r"how\s+to\s+exploit",
        r"steal\s+password",
        r"root\s+access\s+command",
        r"sudo\s+rm\s+-rf"
    ]

    def verify(self, response):

        r = response.lower()

        for p in self.patterns:
            if p in r:
                return False, "Unsafe response blocked"

        return True, "Response safe"


# -----------------------------
# 7. MAIN DEFENSE PLATFORM
# -----------------------------
class DefensePlatform:

    def __init__(self):

        self.firewall = RuleBasedFirewall()
        self.classifier = MLClassifier()
        self.irs = IRS()
        self.rag = RAG()
        self.shield = ResponseShield()

    def process(self, prompt):

    # 1️⃣ Firewall
        safe, msg = self.firewall.validate(prompt)

        if not safe:
            return {
                "status": "BLOCKED",
                "risk_score": "100 %",
                "reason": msg
            }

    # 2️⃣ ML Classifier
        safe, risk_score, msg = self.classifier.classify(prompt)

        if not safe:
            return {
                "status": "BLOCKED",
                "risk_score": f"{risk_score:.2f} %",
                "reason": msg
            }

    # 3️⃣ IRS (clean prompt)
        prompt = self.irs.refine(prompt)

    # 4️⃣ RAG
        context = self.rag.retrieve(prompt)

        final_prompt = f"Context: {context}\nQuestion: {prompt}"

    # 5️⃣ LLM
        response = generate_llm_response(final_prompt)

    # 6️⃣ Response Shield
        safe, msg = self.shield.verify(response)

        if not safe:
            return {
                "status": "BLOCKED",
                "risk_score": f"{risk_score:.2f} %",
                "reason": msg
            }

        return {
            "status": "SAFE",
            "risk_score": f"{risk_score:.2f} %",
            "response": response
        }
