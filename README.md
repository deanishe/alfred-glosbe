# Alfred Glosbe #

Translate text using the [glosbe.com](http://glosbe.com/) [API](http://glosbe.com/a-api).

![](https://github.com/deanishe/alfred-glosbe/raw/master/screenshot2.png "")

Download [here](https://github.com/deanishe/alfred-glosbe/raw/master/Glosbe%20Translation.alfredworkflow).

## TL;DR ##

- `.ende query` Search for German translations of the English word `query`
	- `ENTER` Copy selected translation to clipboard
- `.deen query` Search for English translations of the German word `query`
	- `ENTER` Copy selected translation to clipboard
- `glosbelang [query]` Show/search list of supported languages (not all pairs are supported).
	- `ENTER` Copy ISO-639-3 code of selected language to clipboard
- `glosbehelp` Open included help file in your browser

Other translation pairs must be configured (see **Usage** section below).

## Usage ##

**Note:** Search is (unfortunately) case-sensitive, so if you search for the German word "lager", you won't get any results. You must enter "Lager". Similarly, searching for the English word "Lager" will also return no results: it must be "lager".

Only English &gt; German and German &gt; English are pre-configured (using the keywords `.ende` and `.deen` respectively).

To translate English &gt; German, use `.ende query`. Actioning a result (selecting it and hitting `ENTER`) will copy the translation to the clipboard.

### Setting up other searches ###

To set up additional languages, you'll have to add your own Script Filter to the Workflow using the existing ones as a template (or just change the existing ones).

The Script should look like this (using French &gt; English as an example):

```bash
python fra eng "{query}"
```

The languages codes (`fra`, `eng`) are ISO-639-3 codes. These are all 3 letters long, but many common 2-letter codes (e.g. `en`, `de`, `fr`) are also supported. To see a full list of supported languages, run `python translate.py -t -l` from Terminal in the Workflow directory, or use `glosbelang [query]` in Alfred to search the list.

## About Glosbe.com ##

Glosbe.com supports hundreds of languages (though not all translation pairs are supported).

- [List of all available languages](http://glosbe.com/all-languages)
- [English &gt; other dictionaries](http://glosbe.com/en/all-dictionaries)
- [German &gt; other dictionaries](http://glosbe.com/de/all-dictionaries)
- [French &gt; other dictionaries](http://glosbe.com/fr/all-dictionaries)
- And many, many more. Use the language selector on the site to view the languages you're interested in.

## Screenshots ##

![English &gt; German search](https://github.com/deanishe/alfred-glosbe/raw/master/screenshot1.png "English &gt; German search")

![German &gt; English search](https://github.com/deanishe/alfred-glosbe/raw/master/screenshot2.png "German &gt; English search")

![No results](https://github.com/deanishe/alfred-glosbe/raw/master/screenshot3.png "No results")

![Searching languages](https://github.com/deanishe/alfred-glosbe/raw/master/screenshot4.png "Searching languages")

![Searching language codes](https://github.com/deanishe/alfred-glosbe/raw/master/screenshot5.png "Searching language codes")
