# Memorize App

This is an app designed to help with memorization through mnemonics. The app is not finished right now but the core functionality still works. The idea is to find words that sound like a word that you are trying to memorize. For example, instead of memorizing that `huevos <means> eggs` you would memorize it using a mnemoic `huevos <soundslike> oasis <image> eggs` with "eggs in an oasis" being the imagery. This techinque isn't for everyone but it helps me personally so I think at least some others would enjoy using the app.

## How to Run

The code base comes with a management script that lets you run everything with one command: `python3 manage.py dev up`. This requires click and docker-compose to be installed. Right now only the API works which is separate from the frontend and backend. To use the api you can run a curl command to interact with it. There is currently only one endpoint:

```
alon@alon-XPS:~/memorize$ curl -d '{"lang" : "es", "word":"huevos"}' -H "Content-Type: application/json" -X POST http://localhost/api/mnemonic/
[
  [
    "oasis", 
    1.591621994972229
  ], 
  [
    "waves", 
    1.600000023841858
  ], 
  [
    "whatever", 
    1.600000023841858
  ], 
  [
    "paso", 
    1.632455587387085
  ], 
  [
    "waste", 
    1.6485282182693481
  ], 
  [
    "weights", 
    1.6485282182693481
  ], 
  [
    "sofa", 
    1.7638263702392578
  ], 
  [
    "survey", 
    1.8142136335372925
  ], 
  [
    "slowly", 
    1.880983829498291
  ], 
  [
    "solely", 
    1.880983829498291
  ]
]

```

The endpoint prints a list of similar sounding words. It should work with any language in [http://espeak.sourceforge.net/languages.html](this) list by modify the lang parameter in the API call. Some fun words to try in spanish:
* Barato
* Camiseta
* Jugar 

## How it Works

Glad you asked! The app generates a phonetic representation of the given word using the IPA (International Phonetic Alphabet). Each phoneme in the IPA gets converted to a vector of 22 features (there are about 100 different phonemes). Then we look for words that have a similar array of vectors. This is done using Earth Mover's Distance - a way of finding similar arrays given a large list. We find similar words from a list of the top 10,000 most common english words.

The best way to see more about how the code works is to check out the `mnemonic/generate.py` file. This is what generates the feature arrarys from the list of 10,000 english words in the repo.
