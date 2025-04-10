import streamlit as st
from template import answer_prompt
from pymilvus import MilvusClient
from embedding import api_encode as encode
import llm
import time

client = MilvusClient('./local.db')
collection_name = 'scmp'
st.set_page_config(
    page_title="SCMP CHATBOX",
    page_icon=":robot:",
    layout="wide"
)

# st.title('SCMP CHATBOX')
st.image('title.png')

if "history" not in st.session_state:
    st.session_state.history = []
if "references" not in st.session_state:
    st.session_state.references = []

with st.sidebar:
    st.header("🔥Hot questions")
    st.markdown("""- Please introduce me about human robot
- What happened about Panama ports?
    """)

    buttonClean = st.button("clear history", key="clean")
    if buttonClean:
        st.session_state.history = []
        st.session_state.references = []
        st.rerun()
    if st.session_state.references:
        st.header("📚 reference")
        for i, ref in enumerate(st.session_state.references[-1], 1):
            st.markdown(f"{i}. {ref}")


for i, message in enumerate(st.session_state.history):
    if message["role"] == "user":
        with st.chat_message(name="user", avatar="user.png"):
            st.markdown(message["content"])
    else:
        with st.chat_message(name="assistant", avatar="scmp.png"):
            st.markdown(message["content"])

with st.chat_message(name="user", avatar="user.png"):
    input_placeholder = st.empty()
with st.chat_message(name="assistant", avatar="scmp.png"):
    message_placeholder = st.empty()

query = st.chat_input("Input your question here")
if query:
    input_placeholder.markdown(query)
    history = st.session_state.history

    results = client.search(
        collection_name=collection_name, 
        data=[encode([query])[0]],
        anns_field='dense',
        output_fields=['content', 'metadata'],
        limit=10,
    )[0]


    reference_template = """[{no}] **Title: {header}**
    > {content}
    """
    reference = ""
    reference_list = []
    for i, ref in enumerate(results):
        entity = ref['entity']
        cur = reference_template.format(
            no=i+1,
            header=entity['metadata']['header'],
            content=entity['content'],
        )
        reference += cur + '\n'
        reference_list.append(cur)

    response = llm.query_stream(answer_prompt.format(question=query, reference=reference))
    answer = ''
    for chunk in response:
        delta = chunk.choices[0].delta.content
        answer += delta
        message_placeholder.markdown(answer, unsafe_allow_html=True)
        time.sleep(0.01)


    history.extend([
        {'role': 'user', 'content': query},
        {'role': 'assistant', 'content': answer},
    ])

    st.session_state.history = history
    st.session_state.references.append(reference_list)
    st.rerun()