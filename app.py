import streamlit as st
from io import BytesIO
from gtts import gTTS
import base64

st.set_page_config(page_title="Apprentissage audio anglais", layout="centered")
st.title("Coach Audio – Anglais")
st.markdown("Entraîne-toi avec des phrases utiles en français et anglais.\nAjoute les tiennes ou utilise celles du programme.")

# --- Choix de mode ---
mode = st.radio("Choisis le mode :", ["Programme prêt", "Mes phrases personnalisées"])

# --- Phrases du programme (exemple de session 1) ---
phrases_preset = [
    ("Je suis prêt.", "I'm ready."),
    ("Elle est fatiguée.", "She's tired."),
    ("Il ne vient pas.", "He's not coming."),
    ("Je m'en fiche.", "I don't care."),
    ("Il est toujours occupé.", "He's always busy."),
]

# --- Collecte des phrases ---
phrases = []
if mode == "Programme prêt":
    st.subheader("Session 1 – Phrases pré-définies")
    for fr, en in phrases_preset:
        st.markdown(f"**FR** : {fr}<br>**EN** : {en}", unsafe_allow_html=True)
    phrases = phrases_preset

elif mode == "Mes phrases personnalisées":
    st.subheader("Ajoute tes propres phrases :")
    with st.form("custom_form"):
        french = st.text_area("Phrase en français")
        english = st.text_area("Traduction en anglais")
        submitted = st.form_submit_button("Ajouter la phrase")

        if submitted and french and english:
            phrases.append((french, english))

    if phrases:
        st.success("Phrase ajoutée. Tu peux générer ton audio maintenant.")

# --- Génération Audio ---
if st.button("🎧 Générer l'audio") and phrases:
    st.info("Génération en cours...")

    for fr, en in phrases:
        st.markdown(f"### Phrase :")
        st.markdown(f"**FR** : {fr}")
        st.markdown(f"**EN** : {en}")

        # Générer les deux audios
        fr_tts = gTTS(fr, lang="fr")
        en_tts = gTTS(en, lang="en")

        fr_audio = BytesIO()
        en_audio = BytesIO()

        fr_tts.write_to_fp(fr_audio)
        en_tts.write_to_fp(en_audio)

        fr_audio.seek(0)
        en_audio.seek(0)

        st.audio(fr_audio, format="audio/mp3", start_time=0)
        st.audio(en_audio, format="audio/mp3", start_time=0)

        # Option de téléchargement individuel
        st.download_button(
            label="⬇️ Télécharger audio FR",
            data=fr_audio,
            file_name="phrase_fr.mp3",
            mime="audio/mp3"
        )
        st.download_button(
            label="⬇️ Télécharger audio EN",
            data=en_audio,
            file_name="phrase_en.mp3",
            mime="audio/mp3"
        )
