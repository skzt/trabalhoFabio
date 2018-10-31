
'''
Created on 26 de agosto de 2016

@author: Pedro Vaz
'''

def getPathLocation():
    
    with open("Config.cfg", 'r') as file:
        for line in file:
            if line[0] == '-':
                continue
            elif "Main Folder:" in line:
                pathLocation = line.rstrip()[13:]
                file.close()
                return pathLocation

def getDBinfo():
    
    result = []
    with open("Config.cfg", 'r') as file:
        for line in file:
            
            if len(result) == 4:
                file.close()
                return tuple(result)
            if line[0] == '-':
                continue
            
            elif "Host:" in line:
                result.append(line.rstrip()[6:])
                continue
            
            elif "Utilizador:" in line:
                result.append(line.rstrip()[12:])
                continue            
            
            elif "Senha:" in line:
                result.append(line.rstrip()[7:])
                continue         
            
            elif "Banco:" in line:
                result.append(line.rstrip()[7:])
                continue
          
        if len(result) == 4:
            file.close()
            return tuple(result)   
        else:
            raise IOError           
                
    
    