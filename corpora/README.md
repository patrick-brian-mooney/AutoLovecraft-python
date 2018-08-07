# About These Texts


<a class="h-card u-url p-name" rel="me" href="http://patrickbrianmooney.nfshost.com/~patrick/">Patrick Mooney</a><br />
<span class="vevent"><span class="summary description">Last update to <a class="url location" href="#">this document</a></span>: <abbr class="dtstart" title="2017-05-19">19 May 2017</abbr></span>


This folder (`corpora`) contains texts intended to be used to produce "stories" in my automated-text blog <a rel="me muse" href="http://autolovecraft.tumblr.com/">The Worst of Bad Lovecraft</a>. I believe that all texts in this folder are in the public domain, but if I am incorrect in this assumption, please let me know and the problem will be corrected swiftly. The document you are reading *right now* is the "master README file" for this collection of texts, and will occasionally be referred to as such in these documents.

The top level of this collection, which you are currently browsing, contains several things:

1. The master corpus, downloaded <a rel="muse" href="http://gutenberg.net.au/ebooks06/0600031h.html">from Project Gutenberg</a> (`original corpus (from Project Gutenberg).html`) , and its current-state edited, massaged version (`master corpus (edited and massaged).odt`), stored as a versioned LibreOffice document;
2. The text currently being used as the basis of Lovecraft-trained blog posts, which is called `[something].txt` (at the time of this writing, `The Unnamable.txt`), plus the compiled chains generated from that story, saved as `[story title].[chain length].pkl`, which (at the time of this writing) is `TheUnnamable.3.pkl`.
3. A folder, `previous`, containing edited stories that have previously been used as the basis for training the Markov chain-based generator.
4. A folder, `not yet used`, containing both stories that have been edited but not used as the basis for blog posts, and empty files titled in such a way to remind me which Lovecraft stories from the Project Gutenberg collection have not yet been edited.
5. A folder, `not in PG corpus`, containing Lovecraft stories from sources other than Project Gutenberg.

There are certainly errors in many, if not all, of the texts in these folders. They are always a gradually improving work in progress. However, if you yourself catch errors, you are most welcome to submit corrections.

## Goals for these texts

The texts in this folder and its subfolders are edited (gradually; intermittently; sporadically) with a rather unusual editorial goal in mind: the point is not to create a *scholarly* text (with its various apparatuses for the study of the material, historical, and practical variants), nor to produce a *comparative* or *critical* text (though this project may wind up performing an unusual approximation of this over the long term), nor to produce (in the normal sense) a *reading* text.

Instead, these texts are intended gradually to come to approximate a *very specific type of "reading" text*, one that is produced for a very specific *nonhuman reader*. That reader is, of course, my own <a rel="me" href="https://github.com/patrick-brian-mooney/markov-sentence-generator">Markov chain-based text generator</a> (forked from <a rel="muse" href="https://github.com/patrick-brian-mooney/markov-sentence-generator">Harry R. Schwartz's text generator</a>).

You're a Lovecraft reader, so you already realize that humanity is not the only possible medium in which sentience can arise, and should be comfortable with the idea that some texts are not really meant for human eyes, even if they appear at first to be human-parseable. If you're looking for human-oriented Lovecraft reading texts, you should head on over to <a rel="muse" href="http://hplovecraft.com/">The H.P. Lovecraft Archive</a> to find what you're looking for.

## Editorial decisions and rationale

Merely a brief sketch of how some decisions have been made.

* The **overriding goal** is to produce a series of input texts that will result in "pleasing" (more detail about this later) output text when they are fed as input text to the sentence generator. 
* The overriding goal **is not** to "be faithful to Lovecraft's original texts." (These texts are, to at least some degree, adaptations, not archival or scholarly editions.)
* The overriding goal **is not** to produce human-friendly copies of Lovecraft's stories. (These texts are edited for machine consumption.)
* An *important goal* is that these texts "play well" with other texts, i.e. are easily (productively) remixable with other things that I send into my Markov sentence generator.


Some results of these principles:

* Lovecraft's idiosyncratic and Anglophile spellings are moved toward *contemporary American usage* in the majority of cases, in order to satisfies the "plays well with others" requirement.
* *Instances of dialect* are *converted to standard diction* (because the text generator does not understand the contexts in which these dialects should and should not appear).
* Punctuation is *standardized*. This most notably implies regularization of ellipses, dashes, and hyphens, though other changes are sometimes made, too. (In many cases, "standardized" also implies "moved towards contemporary American usage.")
* There is an increased *tendency toward hyphenation*, and *away from simple agglomeration*, for compound nouns.
