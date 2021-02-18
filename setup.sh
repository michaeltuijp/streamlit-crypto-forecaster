mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
git clone https://github.com/ourownstory/neural_prophet.git\n\
cd neural_prophet\n\
pip install .\n\
\n\
" > ~/.streamlit/config.toml
