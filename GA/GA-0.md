10. http://0.0.0.0:8000/api
Run 
uv run server.py

11. uv run server-11.py

18. https://knapsack-robust-skinning.ngrok-free.dev
Run
OLLAMA_HOST=0.0.0.0:11434 OLLAMA_ORIGINS=* ollama serve
ngrok http 11434 --traffic-policy-file /tmp/policy.yml

7. Crawl
tmp=$(mktemp -d) && wget --recursive --level=inf --no-parent --accept html,htm -P "$tmp" https://sanand0.github.io/tdsdata/crawl_html/ && (cd "$tmp"/sanand0.github.io/tdsdata/crawl_html/ && find . -type f | sed 's#^\./##' | awk 'BEGIN{m=0;n=0} {f=tolower($0); split(f,a,"/"); b=a[length(a)]; if (b ~ /^[a-s]/ && b ~ /\.html$/) m++; else n++} END{print "matching:", m; print "non-matching:", n}') && rm -rf "$tmp"

5. uvicorn server-5:app --host 0.0.0.0 --port 8000 --reload
ngrok http 8000