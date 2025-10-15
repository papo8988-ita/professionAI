
    import gradio as gr
    
    from transformers import pipeline
    
    pipe = pipeline("text-classification", model="papo8988-ita/MLOps-project-repo")
    
    def predict_sentiment(text):
    result = pipe(text)[0]
    return f"Predizione: {result['label']} (score: {result['score']:.2f})"
    
    demo = gr.Interface(
        fn=predict_sentiment,
        inputs=gr.Textbox(lines=3, label="Testo da analizzare"),
        outputs=gr.Textbox(label="Risultato"),
        title="Twitter Sentiment Analysis",
        description="Modello basato su papo8988-ita/MLOps-project-repo per classificare sentiment positivo, neutro o negativo."
    )
    
    if name == "main":
    demo.launch()
    