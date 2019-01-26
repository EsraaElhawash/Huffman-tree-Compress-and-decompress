test = "Well, there's egg and bacon; egg sausage and bacon, egg and spam; egg bacon and spam; egg bacon sausage and spam; spam bacon sausage and spam; spam egg spam spam bacon and spam; spam sausage spam spam bacon spam tomato and spam."
import binascii
import pickle

#import bitarray
def bitstrings_to_bytes(s):
    return int(s, 2).to_bytes(len(s) // 8, byteorder='big')
    
def bitstring_to_bytes(s):
    i=0
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
        print(i)
        i+=1
    return bytes(b[::-1])

class Node:
    
    def __init__(self, char, freq, left=None, right=None, is_leaf=False):
        self.left = left
        self.right = right
        self.char = char
        self.freq = freq
        self.is_leaf = is_leaf
        
    def __lt__(self, other):
        return (self.freq < other.freq)
   
     
class Huffman_Code:
    
    def frequencies(self, message):
        freqs = {}
        for char in message:
            if not char in freqs :
                freqs[char] = 0
            freqs[char] += 1
        return freqs
    
    def get_minimal_node(self, tree):
        if len(tree) == 1:
            return 0
        if len(tree) == 0:
            return -1
        
        min_a = 0
        for i,v in enumerate(tree):
            if v<tree[min_a] :
                min_a = i
        return min_a
    
    def Tree(self, freqs):
        tree = list()
        for char in freqs:
            tree.append(Node(char, freqs[char], is_leaf=True))
        
        while(len(tree)>1):
            min_a = self.get_minimal_node(tree)
            node1 = tree.pop(min_a)
            min_b = self.get_minimal_node(tree)
            node2 = tree.pop(min_b)
            new_node = Node(node1.char + node2.char, node1.freq + node2.freq,
                            node1, node2)
            tree.append(new_node)
            
        return tree[0]
    
    def code(self, tree, freqs):
        code = {}
        for key in freqs:
            current_node = tree
            sequence = ''
            while not(current_node.is_leaf) :
                if key in current_node.left.char :
                    sequence += '0'
                    current_node = current_node.left

                elif key in current_node.right.char :
                    sequence += '1'
                    current_node = current_node.right
                else :
                    raise Exception
            code[key] = sequence
            #print(code[key],sequence," ");
        
        return code
    
    def encode(self, codex, text):
        binary_code = ''
        zero="0"
        for char in text :
            binary_code += codex[char]
        print(len(binary_code)/8)    
        #print("\n",binary_code,"\n",len(binary_code))
        
        if len(binary_code) % 4 != 0 :
            ext=4-(len(binary_code)%4)
            binary_code=('0' * ext) + binary_code
            ext=str(ext)
            pickle.dump(ext,outputf)
            #pickle.dump("\n",outputf)
            #outputf.write(ext.encode('utf-8'))
            #outputf.write("\n".encode('utf-8'))
        else :
            pickle.dump(zero,outputf)
            #pickle.dump("\n",outputf)  
        print(binary_code[0:4])   
        if binary_code[0:4]=="0000":
            print("t")
            pickle.dump("T",outputf)
           # pickle.dump("\n",outputf) 
        else :
            pickle.dump("F",outputf)
           # pickle.dump("\n",outputf)            

        byte_array=bitstrings_to_bytes(binary_code)    
       
        print("d0ne")    
        return byte_array
        
        
    def decode(self, codex, binary_code,ext,zero):
        text = '' 
        #print(binary_code)
        bin_code=str(bin(int.from_bytes(binary_code, byteorder='big')))
        #print(bin_code)
        #bin_code.frombytes(binary_code)
        #print ("zzz",bin_code)
        bin_code=bin_code[2:]
        #print(bin_code)
        if zero=="T":
            bin_code=('0'*4)+ bin_code
            #print(bin_code)
        
        #bin_code=binary_code[int(ext):];
        if len(bin_code)%4 !=0 :
            
            add=4-(len(bin_code)%4)
            #print("hehh",add)
            bin_code=('0'* add ) + bin_code
            #print(bin_code)
            
        bin_code=bin_code[int(ext):]
        #if binary_code[0]=="0":
            #
        #bin_code=bin_code[int(ext):]
        #print(bin_code)
        i=0
        while len(bin_code)>0:
            index = 1
            next_char = False
            while not next_char:
                #print("ici")
                for key in codex:
                    #print(key)
                    if key[5:len(key)-1] == bin_code[:index]:
                    #if codex[key]==bin_code[:index]:
                        print (key[5:len(key)-1]+" tos "+key[1])
                        text += key[1]
                        #print(text)
                        next_char = True
                index += 1
            bin_code = bin_code[index-1:]
            print(bin_code[0:20])
            i+=1
        print("done")    
        return text
        
    
    def __init__(self, text):
        self.text = text


if __name__ =='__main__' :

    state = input('Voulez-vous coder ou decoder ?')
    if state=="compress": 
        #inputf =open("HuffmanInput.txt","r")
        inputf=open("demo.txt","r")
        outputf =open("zip.bin","wb")
        test=inputf.read()
        #print(test)
        hc = Huffman_Code(test)
        freqs = hc.frequencies(test)
        tree = hc.Tree(freqs)
        codex = hc.code(tree, freqs)
        temp=str(codex).replace(" ","")
        temp=temp.replace("''","' '")
        print(temp)
        pickle.dump(temp,outputf)
        #pickle.dump("\n",outputf)
        #outputf.write(temp.encode('utf-8'))
        #outputf.write("\n".encode('utf-8'))
        coded_text = hc.encode(codex, test)
        #coded_text=(binascii.hexlify(coded_text))
        print(coded_text)
        #coded_text=coded_text.replace('\x','')
        pickle.dump(coded_text,outputf)
        #outputf.write(coded_text)
        print("\n ktbt",len(coded_text),"\n") 
        #decoded_text = hc.decode(codex, coded_text)#,ext)
        print('length text :', len(hc.text),'; length coded_text :', len(coded_text))
        print('Compression rate =', len(coded_text)/(len(hc.text)*8))
        outputf.close()
    elif state == "0" :
        hc = Huffman_Code(test)
        outputf =open("demo.txt","w")
        inputf =open("zip.bin","rb")
        
        codex=pickle.load(inputf)
        codex=(codex).replace("{","").replace("}","").replace(",","~").replace("\\n","\n")
        
        codex=codex.replace("'~':","',':")
        codex=codex.split("~")
        print(codex)
        
        #codex[0]=" "+codex[0]
        codex[len(codex)-1]=(codex[len(codex)-1])[:len(codex[len(codex)-1])-2]+' '
        print(codex[len(codex)-1])
        
        #ext=pickle.load(inputf)
        ext=pickle.load(inputf)
        print("ext",ext)
        zero=pickle.load(inputf)
        #zero=pickle.load(inputf)
        coded_text=pickle.load(inputf)
        #coded_text=pickle.load(inputf)
        #print(coded_text)
        decoded_text = hc.decode(codex, coded_text,ext,zero)
        #print(decoded_text)
        outputf.write(decoded_text)
        outputf.close()
    #print('\nThe decoded text is the same as the original : ' + str(decoded_text == hc.text))
