import os
import streamlit as st
from scraper import WebPage
from utils import make_zip



st.set_page_config(layout='centered')



col1, col2, col3 = st.columns([3, 2, 1])

with col1:
    url = st.text_input('enter url')

with col2:
    directory = st.text_input('enter directory')

with col3:
    st.markdown("<div style='height:1.7em'></div>", unsafe_allow_html=True)
    go = st.button('go', use_container_width=True)


if go:
    if not url:
        st.warning('Please enter a valid URL.')

    page = WebPage(url)
    pdf_links = page.get_pdf_urls()
    with st.spinner(f'Fetching {url} ...'):
        if not pdf_links:
            st.warning('no pdfs found.')

        else:
            st.success(f'found {len(pdf_links)} pdfs.')
            progress_bar = st.progress(0)
            status = st.empty()

            total = len(pdf_links)

            for i, ref in enumerate(pdf_links, start=1):
                page.download_pdf(ref, directory)
                progress_bar.progress(i / total)


            zip_buffer = make_zip(directory)
            st.download_button(
                label='download .zip',
                data=zip_buffer,
                file_name='pdfs.zip',
                mime='application/zip'
            )
