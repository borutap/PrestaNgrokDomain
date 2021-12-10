# PrestaNgrokDomain

Update your PrestaShop domain URL according to running ngrok tunnel.

## Installation

PrestaNgrokDomain requires [Chromedriver](https://chromedriver.storage.googleapis.com/index.html?path=96.0.4664.45/) to run. It should be placed in this project's directory.
To run the script, firstly install the required Python dependencies.
```sh
pip install -r requirements.txt
```
Now rename `.env.dist` file to `.env` and set the variables according to your configuration.
Then start ngrok and your PrestaShop Apache and MySQL server. It is assumed the shop's domain is rooted at `/` and MySQL port is `3306`. The program might be more flexible in the future!
When the servers are up run the script.
```sh
python main.py
```
## License

MIT
