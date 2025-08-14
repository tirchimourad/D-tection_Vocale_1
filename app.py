import streamlit as st
import speech_recognition as sr
from datetime import datetime

# Fonction de transcription améliorée
def transcribe_speech(api_choice, language):
   r = sr.Recognizer()
   with sr.Microphone() as source:
        st.info("Parlez maintenant...")
        try:
            audio_text = r.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            return "Aucune parole détectée (timeout)."
        
        st.info("Transcription en cours...")
        try:
            if api_choice == "Google":
                return r.recognize_google(audio_text, language=language)
            elif api_choice == "Sphinx":
                return r.recognize_sphinx(audio_text, language=language)
            elif api_choice == "Google Cloud":
                return r.recognize_google_cloud(audio_text, language=language)
            elif api_choice == "Azure":
                return r.recognize_azure(audio_text, language=language)
            elif api_choice == "IBM":
                return r.recognize_ibm(audio_text, language=language)
            else:
                return "API non supportée."
        except sr.UnknownValueError:
            return "Impossible de comprendre l'audio."
        except sr.RequestError as e:
            return f"Erreur lors de la requête à l'API: {e}"

# Interface Streamlit
def main():
    st.title("Application de Reconnaissance Vocale")
    st.write("Cliquez sur le microphone pour commencer à parler et transcrire votre voix.")
    
    # Choix de l'API
    api_choice = st.selectbox(
        "Choisissez l'API de reconnaissance vocale",
        ["Google", "Sphinx", "Google Cloud", "Azure", "IBM"]
    )
    
    # Choix de la langue
    language = st.selectbox("Choisissez la langue", ["fr-FR", "en-US", "es-ES", "de-DE"])
    
    # Pause / reprise
    pause_recognition = st.checkbox("Mettre en pause la reconnaissance")
    
    # Bouton de transcription
    if st.button("Commencer la transcription"):
        if pause_recognition:
            st.warning("La reconnaissance vocale est en pause.")
        else:
            transcription = transcribe_speech(api_choice, language)
            st.write("Transcription :", transcription)
            
            # Option de sauvegarde
            save_text = st.checkbox("Sauvegarder le texte transcrit")
            if save_text and transcription.strip():
                filename = f"transcription_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(transcription)
                st.success(f"Texte sauvegardé sous {filename}")
                st.download_button(
                    label="Télécharger la transcription",
                    data=transcription,
                    file_name=filename,
                    mime="text/plain"
                )

if __name__ == "__main__":
    main()


