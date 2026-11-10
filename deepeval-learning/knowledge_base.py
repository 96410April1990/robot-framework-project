POLICIES = [
    "Employees receive 20 annual leave days.",
    "Employees receive 10 sick leave days.",
    "Employees can work remotely 2 days per week.",
    "The company provides health insurance."
]

def retrieve_documents(question):
    question = question.lower()

    if "leave" in question:
        return POLICIES[:2]

    if "remote" in question:
        return [POLICIES[2]]

    if "insurance" in question:
        return [POLICIES[3]]

    return []

#This is a rule based retriever, not semantic vector search. 
