import ollama
import pyperclip
import click

# on récupère le texte copié dans le presse-papier
text = pyperclip.paste()

# si le texte est vide, on demande à l'utilisateur de saisir le texte
if not text:
    text = click.prompt("Enter text to correct", type=str)


def main(text):

    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": f""" Tu es un correcteur de texte, peux-tu corriger le texte suivant s'il te plaît retourne le texte corrige sans m'expliquer. Tu respecteras les 4 regles suivantes.
                Regle 1 : Ne rajoute aucune description qui montre que tu as corriger (type "Version corrige")->
                Regle 2 : Garder le texte le plus proche possible de l'original.
                Regle 3 : Ne pas changer le ton du texte original.
                Regle 4 : Garder la langue dans laquelle le texte t'a ete tranmis.
                ->
      {text}
            """,
            }
        ],
    )
    click.echo(response["message"]["content"])


if __name__ == "__main__":
    main(text)
