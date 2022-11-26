

# .wav ses dosyasını okumak ve yazmak için yerel Python kurulumunda bulunan wave paketini kullanacağız.
import wave
# Ses dosyasını oku
song = wave.open("sansi.wav", mode='rb')
# Frameleri oku ve byte dizisine dönüştür
frame_bytes = bytearray(list(song.readframes(song.getnframes())))

# Gizli mesajım
string='Ayşe tatile çıksın.'
# Bytların geri kalanını doldurmak için sahte veriler ekle.Alıcı karakterkeri algılar ve kaldırır.
string = string + int((len(frame_bytes)-(len(string)*8*8))/8) *'#'
# Metni bit dizisine dönüştür.
bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string])))

# Ses verilerinin her baytının LSB'sini metin biti dizisinden bir bit ile değiştirdim.
for i, bit in enumerate(bits):
    frame_bytes[i] = (frame_bytes[i] & 254) | bit
# Değiştirilen bytları aldım.
frame_modified = bytes(frame_bytes)

# Yeni bir wave ses dosyasına bayt yaz
with wave.open('song_embedded.wav', 'wb') as fd:
    fd.setparams(song.getparams())
    fd.writeframes(frame_modified)
song.close()