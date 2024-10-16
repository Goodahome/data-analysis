import streamlit
import streamlit.web.cli
from streamlit import bootstrap

if __name__ == '__main__':
    streamlit._is_running_with_streamlit = True
    bootstrap.run('web.py', 'streamlit run', [], {})