from transformers import pipeline

# Force PyTorch instead of TensorFlow
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2", framework="pt")

def ask_question(context, question):
    result = qa_pipeline(question=question, context=context)
    return result["answer"]
