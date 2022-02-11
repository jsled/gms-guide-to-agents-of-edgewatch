
generate: guide.html
	. v/bin/activate; python3 cite.py < guide.html > index.html

publish: index.html
	scp -r index.html guide.{css,js} lib jsled@asynchronous.org:asynchronous.org/gms-guide-to-agents-of-edgewatch
