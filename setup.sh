git clone https://github.com/ourownstory/neural_prophet.git
cd neural_prophet
pip install .

mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml
