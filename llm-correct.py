import os,click,pyperclip,pathlib
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

@click.command()
@click.option('-m','message')
@click.option('-c','--clipboard', is_flag=True)
@click.option('-s','--save',help='filename of the corrected text',
              type=click.Path(path_type=pathlib.Path))
@click.option('-i','--input',help='filename of the entry file to be corrected '
              ,type=click.Path(path_type=pathlib.Path))
@click.option('-v','--verbose',help='verbosity of the mistakes you made.'
              ,is_flag = True)

def correct(message,clipboard,save,input,verbose):
    f = open("./api",'r')
    api_key = f.readline()
    api_key= str(api_key).strip()
    model = "mistral-large-latest"
    prompt,flag = '',''
    client = MistralClient(api_key=api_key)
    
    print(f"[+] Correcting the file {input}\n")
    if input:
        if verbose:

            prompt = """
            tu es un professeur de francais qui est capable d'expliquer les fautes,
            problemes de sythaxes et de grammaire pour le text ci donnee:
                        """

        else:
            prompt = """
                Tu es maintenant un correcteur automatique, tu es capable de
                garder le contexte du message intitial ainsi que la langue   
                et retournera uniquement le texte corrige sans explication :
                """
        file = open(input,"r")
        file_content = file.readlines()
        prompt = prompt + f"{file_content}"

    if message:
        if verbose:
            print(f"[+] Correcting the input{message}\n")
            prompt = """
            tu es un professeur de francais qui est capable d'expliquer les fautes,
            problemes de sythaxes et de grammaire pour le text ci donnee:
                            """
            prompt = prompt + f"{message}"
        else:
            prompt = """
                            Tu es maintenant un correcteur automatique, tu es capable de
                            garder le contexte du message intitial ainsi que la langue   
                            et retournera uniquement le texte corrige sans explication :
                            """
            prompt = prompt + f"{message}"

    chat_response = client.chat(
        model=model,
        messages=[
            ChatMessage(
                role    = "user",
                content = prompt
            )
        ]
    )
    correct_answer = chat_response.choices[0].message.content
    if clipboard:
        pyperclip.copy(correct_answer)
        
    print(correct_answer)
    #print(chat_response.choices[0].message.content)
    if save:
        print(f"[+] Your file will be save under ./export/{save}")
        file = open(f"./export/{save}","w+")
        file.writelines(correct_answer) 

if __name__ == "__main__":
    correct()
