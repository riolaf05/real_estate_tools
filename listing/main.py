from tools.google_places_api import search_places, get_latitude_longitude, get_near_places
from dotenv import load_dotenv
load_dotenv(override=True)

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.tools import BaseTool, StructuredTool, tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os
import streamlit as st

# Tool setup
toolkit = [
    search_places,
    get_latitude_longitude,
    get_near_places
]

# secrets
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
os.environ["GPLACES_API_KEY"] = st.secrets["GPLACES_API_KEY"]

llm = ChatOpenAI(model="gpt-4o", temperature=0.0, max_tokens=1000)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", """
Sei un assistente che scrive annunci immobiliari efficaci e accattivanti per affitti a Milano.
Ricevi un indirizzo e, usando esclusivamente i tool search_places, get_latitude_longitude e get_near_places, individua i luoghi di interesse nelle vicinanze (università, ospedali, metro, supermercati, aree verdi, ecc).
Scrivi un annuncio immobiliare in stile simile al seguente esempio, mettendo in risalto la posizione e i servizi vicini trovati.

Questo è solo un annuncio di esempio, non copiarlo parola per parola. Usa i luoghi trovati per personalizzare l'annuncio, su qualsiasi indirizzo o città fornita:

Esempio:
Vivi Milano al centro di tutto – Stanza in trilocale moderno e luminoso a due passi da Bocconi, IULM e Ospedale San Paolo!
📍 Via San Vigilio 33 – Cantalupa/San Paolo – Milano
💶 € 700/mese
📐 100 m² · Trilocale

Se cerchi una casa spaziosa, moderna e perfettamente collegata, questa è la tua occasione!
A pochi minuti dalla MM2 Famagosta, in una zona tranquilla ma dinamica, proponiamo in affitto un trilocale di 100 m² ideale per giovani professionisti, studenti universitari che vogliono vivere Milano con comodità e stile.

🟢 Posizione imbattibile:
A soli 5 minuti dalla fermata M2 Famagosta
A brevissima distanza da Università Bocconi, IULM e a pochi passi dall’Ospedale San Paolo.
Servita da supermercati, negozi e aree verdi.

🏡 Caratteristiche dell’appartamento:
Ampio soggiorno luminoso  
Cucina separata e funzionale
3 camere da letto spaziose
Bagno con doccia e vasca
Balconi e affacci tranquilli
Possibilità di usufruire di un posto auto e box condominiale per depositare bici.
📦 Arredato e pronto da abitare!

Non perdere questa opportunità: comfort, spazio e una posizione strategica per vivere Milano al meglio!
📞 Contattaci ora per una visita!

Usa i luoghi trovati per personalizzare l'annuncio. Se non puoi trovare luoghi vicini, dillo chiaramente.
Restituisci solo l'annuncio, senza spiegazioni aggiuntive.
        """),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

agent = create_openai_tools_agent(llm, toolkit, prompt)
agent_executor = AgentExecutor(agent=agent, tools=toolkit, verbose=False)

# Streamlit UI
st.set_page_config(page_title="Generatore Annuncio Immobiliare", page_icon="🏠")
st.title("Generatore Annuncio Immobiliare")

st.markdown(
    """
    <div style="background-color: #fff3cd; padding: 10px; border-radius: 5px; border: 1px solid #ffeeba;">
        <strong>Nota:</strong> Inserisci un indirizzo a Milano: l'app genererà un annuncio immobiliare personalizzato, mettendo in risalto i luoghi di interesse nelle vicinanze (università, metro, ospedali, supermercati, ecc).
    </div>
    """,
    unsafe_allow_html=True
)

address = st.text_input("Inserisci l'indirizzo dell'immobile:")

if st.button("Genera annuncio") and address:
    with st.spinner("Sto generando l'annuncio..."):
        try:
            result = agent_executor.invoke({"input": address})
            if isinstance(result, dict) and "output" in result:
                output = result["output"]
            else:
                output = result
            st.subheader("Annuncio generato:")
            st.write(output)
        except Exception as e:
            st.error(f"Errore durante la generazione dell'annuncio: {e}")
