import streamlit as st
from io import BytesIO
from gtts import gTTS
from pydub import AudioSegment

st.set_page_config(page_title="Apprentissage audio anglais", layout="centered")
st.title("Coach Audio – Anglais")
st.markdown("Entraîne-toi avec des phrases utiles en français et anglais.\nAjoute les tiennes ou utilise celles du programme.")

# Choix de mode
mode = st.radio("Choisis le mode :", ["Programme prêt", "Mes phrases personnalisées"])

# Phrases du programme (exemple)
phrases_preset = [
    ("Je suis prêt.", "I'm ready."),
    ("Elle est fatiguée.", "She's tired."),
    ("Il ne vient pas.", "He's not coming."),
    ("Je m'en fiche.", "I don't care."),
    ("Il est toujours occupé.", "He's always busy."),
]

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
        repeat = st.slider("Combien de fois répéter la phrase en anglais ?", 1, 3, 2)
        submitted = st.form_submit_button("Ajouter la phrase")

        if submitted and french and english:
            phrases.append((french, english, repeat))

    if phrases:
        st.success("Phrase ajoutée. Tu peux générer ton audio maintenant.")

if st.button("🎧 Générer l'audio") and phrases:
    st.info("Génération en cours...")
    audio = AudioSegment.silent(duration=1000)

    for item in phrases:
        if len(item) == 2:
            fr, en = item
            repeat = 2
        else:
            fr, en, repeat = item

        tts_fr = gTTS(fr, lang="fr")
        tts_en = gTTS(en, lang="en")

        fr_mp3 = BytesIO()
        en_mp3 = BytesIO()
        tts_fr.write_to_fp(fr_mp3)
        tts_en.write_to_fp(en_mp3)
        fr_mp3.seek(0)
        en_mp3.seek(0)

        fr_audio = AudioSegment.from_mp3(fr_mp3)
        en_audio = AudioSegment.from_mp3(en_mp3)


        audio += fr_audio + AudioSegment.silent(duration=2000)
        for _ in range(repeat):
            audio += en_audio + AudioSegment.silent(duration=1500)

    final_mp3 = BytesIO()
    audio.export(final_mp3, format="mp3")
    final_mp3.seek(0)

    st.audio(final_mp3, format="audio/mp3")
    st.download_button("⬇️ Télécharger l'audio MP3", data=final_mp3, file_name="session_audio.mp3", mime="audio/mp3")
