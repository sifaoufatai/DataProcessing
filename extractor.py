

"""
 programe de 4 eme Benin 
 
 chaque chunk est un ensemble de  
 - situation d'apprentissage : str 
         - list sequence 
         -
       
 -sequence : str 
    - content : str
     - propritets :listes 
     - NB : 
     - vocabulaire autorisé 
     - non autorisé 
     - prerequis  
  
 
 
"""

from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("CV_2025-08-06_Hissam Traoré_SALIFOU.pdf")
text = result.text_content
with open('hissam.txt','w') as f:
    f.write(text)
