> [**a-wystlan**](https://bosworthtoller.com/2792)
> *verb*
> to hiss, lisp.

### What is Wystlan?

Wystlan is a toy project playing with the idea of a [DSL](https://en.wikipedia.org/wiki/Domain-specific_language) for non-technical [OSINT](https://en.wikipedia.org/wiki/Open-source_intelligence)ers. It runs using a [Python](https://en.wikipedia.org/wiki/Python_(programming_language))-based [LISP](https://en.wikipedia.org/wiki/Lisp_(programming_language)) [interpreter](https://en.wikipedia.org/wiki/Interpreter_(computing)). 

Even though Python is a very high-level language, LISP is far less intimidating for those without experience coding given how similar short scripts in it can be to commands in everyday speech, e.g.: "Get [the contents of] Google's homepage" -> `(get "https://www.google.com")`, "Add 23 [and] 64" -> `(+ 23 64)`, etc. Additionally, many OSINT libraries are available for Python which means they can be easily incorporated into the "standard library" of a DSL interpreted using Python. 

Wystlan as it currently stands derives from the source code provided in Karim Hamidou's excellent [*LISP.PY*](https://khamidou.com/compilers/lisp.py/) article as well as the Peter Norvig articles [*(How to Write a (Lisp) Interpreter (in Python))*](http://norvig.com/lispy.html) and [*(An ((Even Better) Lisp) Interpreter (in Python))*](http://norvig.com/lispy2.html) that inspired it.

### Disclaimer

Wystlan is far from being a complete language or even of having pretensions to being an OSINT DSL at present. 

Unless otherwise separately undertaken by the Licensor, to the extent possible, the Licensor offers the Licensed Material as-is and as-available, and makes no representations or warranties of any kind concerning the Licensed Material, whether express, implied, statutory, or other. This includes, without limitation, warranties of title, merchantability, fitness for a particular purpose, non-infringement, absence of latent or other defects, accuracy, or the presence or absence of errors, whether or not known or discoverable. Where disclaimers of warranties are not allowed in full or in part, this disclaimer may not apply to You. 

To the extent possible, in no event will the Licensor be liable to You on any legal theory (including, without limitation, negligence) or otherwise for any direct, special, indirect, incidental, consequential, punitive, exemplary, or other losses, costs, expenses, or damages arising out of this Public License or use of the Licensed Material, even if the Licensor has been advised of the possibility of such losses, costs, expenses, or damages. Where a limitation of liability is not allowed in full or in part, this limitation may not apply to You. 

The disclaimer of warranties and limitation of liability provided above shall be interpreted in a manner that, to the extent possible, most closely approximates an absolute disclaimer and waiver of all liability.
