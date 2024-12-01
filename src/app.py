import streamlit as st
from services.blob_service import upload_blob
from services.credit_card_service import get_credit_card_info

def config_interface():
    st.title("Upload de arquivos DIO - Azure - Fake Docs")
    uploaded_file = st.file_uploader("Escolha um arquivo", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        filename = uploaded_file.name
        # Enviar para o blob storage
        blob_url = upload_blob(uploaded_file, filename)
        if blob_url is None:
            st.write("Erro ao enviar arquivo")
        else:
            st.write("Arquivo enviado com sucesso!")
            credit_card_info = get_credit_card_info(blob_url)
            print(credit_card_info)
            show_image_and_validation(blob_url, credit_card_info)

def show_image_and_validation(image_url, credit_card_info):
    st.image(image_url, caption="Imagem enviada", use_column_width=True)
    st.write("Resultado da validação:")

    if credit_card_info and 'card_name' in credit_card_info:
        st.markdown('<h1 style="color: green;">Cartão de crédito válido</h1>', unsafe_allow_html=True)
        st.write("Nome do cartão:", credit_card_info['card_name'])
        st.write("Banco emissor:", credit_card_info['bank_name'])
        st.write("Data de validade:", credit_card_info['expiration_date'])
    else:
        st.markdown('<h1 style="color: red;">Cartão de crédito inválido</h1>', unsafe_allow_html=True)
        st.write("Este não é um cartão de crédito válido")

    st.write("Informações do cartão de crédito:")
    st.write(credit_card_info)

if __name__ == "__main__":
    config_interface()