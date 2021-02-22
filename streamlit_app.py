import streamlit as st
import pickle
import pandas as pd
import plotly.express as px

@st.cache
def load_data():

    df1 = pickle.load( open("topic_party.pck", "rb"))
    df2 = pickle.load( open("topic_plot_data.pck", "rb"))
    return df1, df2

st.image("kamer.png")

st.markdown("""
## Stem helper 

### Gebasseerd op topics mbv top2vec op kamerdebatten

In drie makkelijke stappen je stem uitbrengen.

***

""")

# load data #################################################################################################
topic_partijen, plotdata = load_data()


# umap cluster plot #########################################################################################

st.markdown("""
### 1. Waar is over gedebateerd in de tweede kamer

Krijg eerst een idee van de topics waarover gedebateerd is in de tweede kamer (in 2019)""")

fig0 = px.scatter(
    plotdata,
    x = "x",
    y = "y",
    color = "cluster_label_str",
    hover_name = "hover_text",
    size = "terms",
    width = 900, height = 600,
    size_max = 6,
    title = "2D Kamer speeches. Gekleurd per topic. Hover over voor sleutelwoorden per topic."
)
st.plotly_chart(fig0)


# partijverdeling ###########################################################################################
st.markdown("""
### 2. Kijk naar de partijverdeling van een topic

Wat spreekt je aan? Zoek naar een topic en zie welke partijen hier actief in hebben gedebateerd
""")

search_term = st.text_input("vul een zoekterm in", "landbouw")
search_term = search_term.lower()
tmp = (
    topic_partijen
    .query('party != "no_party"' )
)

tmp = tmp[ tmp['topic_words'].str.contains(search_term)]
tmp = tmp.sort_values(["party_count"])

if tmp.shape[0] > 0 :
    n = len(tmp.topic_words.value_counts())
    st.write(f"Er zijn {n} topics gevonden met gegeven zoekterm:  **{search_term}**. Zie de sleutelwoorden van deze topics ")

    st.table(tmp.topic_words.value_counts().index)

    st.markdown("### De partij verdeling van bovenstaande topics zie je hieronder")

    fig = px.bar(
        tmp, 
        x = "party", 
        y = "party_count", 
        height = 800, 
        width=800, 
        facet_col = "topic_words", facet_col_wrap=1,
        hover_name= "topic_words")

    st.plotly_chart(fig)
else:
    st.write("zoekterm niet in topics sleutelwoorden")


st.markdown("### 3. Vergeet niet te stemmen op 17 maart")


st.markdown("""

***

***

### Korte uitleg
Alle Tweede Kamer parlementaire debatten van januari-1995 t/m juni-2019 zijn in een data set verzameld. Dat is het werk van:

**Rauh, Christian; Schwalbach**, Jan, 2020, Zie [hier voor de paper](https://doi.org/10.7910/DVN/L4OAKN/C2TWCZ) en [hier voor de data](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/L4OAKN).

Van kamerdebatten in 2019 heb ik een [top2vec](https://github.com/ddangelov/Top2Vec) aanpak gedaan waarbij elke speech van een kamerlid geclustered wordt in topics. 
Deze topics kenmerken zich door een aantal sleutelworden. Dit streamlit dashboard geeft in de bovenstaande scatterplot een 2-dimensionale 
weergave de gevonden topics. Hover over de scatterplot om de sleutelwoorden voor een topic te zien. 

Geef een zoekterm op, waar je interesse ligt, bijvoorbeeld **landbouw**. Het dashboard zoekt in de sleutelwoorden van de topics.
Zodat je een idee kan krijgen welke partij veel of weinig deelnemen in bepaalde topics / debatten. 

Zie mijn [Github repo](https://github.com/longhowlam/kamer_debatten) voor wat meer details, groeten en succes met stemmen Longhow.

""")
