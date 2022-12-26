
import wave
# Ses dosyasını oku
song = wave.open("sansi.wav", mode='rb')
# Frameleri oku ve byte dizisine dönüştür
frame_bytes = bytearray(list(song.readframes(song.getnframes())))

# Gizli mesajım
string='aysetatileciksin'
# Bytların geri kalanını doldurmak için sahte veriler ekle.Alıcı karakterkeri algılar ve kaldırır.
liste=list(string)
sahteveri=int((len(frame_bytes)-(len(string)*8*8))/8) *'#'
liste2=list(sahteveri)
# şifreyi for döngüsü oluşturarak istediğim bitlere atadım.Şifrenin her bir bitini ses dosyasında kendinden 2 fazla olan bitine gizledim.
for i in range(len(liste)):
    liste2[i+2]=liste[i]
    

#stringe çevirdim.
mystring=''.join(map(str,liste2))

# Metni bit dizisine dönüştürdüm.
bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in mystring])))

# Ses verilerinin her baytını metin biti dizisinden bir bit ile değiştirdim.
for i, bit in enumerate(bits):
    frame_bytes[i] = (frame_bytes[i] & 254) | bit #or işlemi
# Değiştirilen bytları aldım.
frame_modified = bytes(frame_bytes)

# Yeni bir wave ses dosyasına bayt yaz
with wave.open('song_embedded.wav', 'wb') as fd:
    fd.setparams(song.getparams())
    fd.writeframes(frame_modified)
song.close()



#------------------------------Şifreli Metni Açığa çıkarma
song = wave.open("sansi.wav", mode='rb')
# sesi arraye dönüştürdüm.
frame_bytes = bytearray(list(song.readframes(song.getnframes())))

# şifrenin olmadığı bytler çıkarıldı.
extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
# bytlar stringe çevrildi
string = "".join(chr(int("".join(map(str,extracted[i:i+8])),2)) for i in range(0,len(extracted),8))
# '#' karakterinden kurtarıyorum
decoded = string.split("###")[0]

# yazdırdım.
print("Sucessfully decoded: "+decoded[2:])#2.karakterden başlayarak yazdırdım.Yoksa ##Aysetatileciksin seklinde çıktı alıyodum.Bunu engellemek için
song.close()
