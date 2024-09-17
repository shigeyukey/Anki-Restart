
ANKI_RESTART = "Anki Restart"

def clink(name, text,url=None):
    if not url:
        return f'{name} : {text}<br>'
    return f'{name} : <a href="{url}">{text}</a><br>'

credits = """
<br><br><br>
<b>[ CREDIT ]</b>
<br><br><br>
""".replace('\n', '<br>')

patreon = """
Special Thanks
<b>[ PATRONS ]</b>
Arthur Bookstein
Haruka
Luis Alberto, Letona Quispe
GP O'Byrne
Tobias Klös
07951350313540
Douglas Beeman
Ernest Chan
Haley Schwarz
Daniel Kohl-Fink
Ketan Pal
Lily
Gabriel Vinicio Guedes
Tim
Oleksandr Pashchenko
Alba Grecia Suárez Recuay
Kurt Grabow
Alex D
Kyle Mondlak
Jesse Asiedu
Renoaldo Costa Silva Junior
Felipe Dias
NamelessGO
Fahim Shaik
Corentin
Yitzhak Bar Geva
龍星 武田
Muneeb Khan
Hikori
Lê Hoàng Phúc
ElAnki
oiuhroiehg
Tae Lee
Ashok Rajpurohit
Tobias Günther
NoirHassassin
Jk
Jake Stucki
Ansel Ng
Victor Evangelista
Moritz Bluhm
Maik C.
Ricardo Escobar
Daniel Valcárcel Málaga
Lerner Alcala
Jason Liu
Blake
Rogelio Rojas
Bunion Bandit
ifjymk
Cole Krueger
K
Aaron Buckley
KM
Melchior Schilling
Адріан Недбайло
철수 박
Lisette Lerma
Natalia Ostaszewska
Jordyn Kindness
Wa sup
Patrick Lee
Jacob Royce
Mattia Adami
Gregory Dance
Carlos Garcia
cedox
Jonny MacEachern
🌠
Martin Gerlach
Knightwalker
Lukas Hammerschmidt
HORUS ™
as cam
Richard Fernandez
K Chuong Dang
Hashem Hanaktah
Justin Skariah
Marli
Ella Schultz
Ali Abid
Siva Garapati
Nitin Chetla
hubert tuyishime
J
Dan S
Salman Majid
C
Maduka Gunasinghe
Marcin Skic
Andreas China
anonymous
Chanho Youne
Dhenis Ferisco
Wave
Foxy_null
WolfsForever
César Flores
Abufit Club
JB Eyring
Yazan Bouchi
Corey
mootcourt
Peter McCabe
Daniel Chien
D N
Mrudang
Yon Uni
Saad
Jared
Mohull Mehta
Abhi S
Robert Malone
On The Path Of Righteousness
Wei
Xeno G
Theodore Addo
Robert Balisong
Tyler Schulte
Jonathan Contreras
Greg
Philly
Đen Trắng
Osasere Osula
Morgan Torres
Rae Hanna
Natalie
Michael Pekala
Fraol Feye
Cameron M
Omar Toro
Keeler Kime
Melvin Ezennia
Nailah Kahotep
Sean Voiers



""".replace('\n', '<br>')

sound =("<b>[ SOUNDS & BGM ]</b><br>"+
clink("Sound Effect", "Koukaon lab","https://soundeffect-lab.info/",)+
clink("Music" , "MaouDamashii","https://maou.audio/",)+
clink("Catgirl Voice","Cici Fyre","https://cicifyre.itch.io/")+
clink("Robot Voice","Charlie Pennell Productions©","https://www.charliepennellproductions.com/")
)


caractor = ("<b>[ IMAGE&3D MATERIALS ]</b><br>" +
clink("Knight","rvros","https://rvros.itch.io/") +
clink("Hooded","Penzilla","https://penzilla.itch.io/")+
clink("CatGirl","(Unity-chan)Kanbayashi Yuko<br>© Unity Technologies Japan/UCL","https://unity-chan.com/contents/guideline/")+
clink("Monsters","RPG dot(R-do) monta!","http://rpgdot3319.g1.xrea.com/")+
clink("Sushi","Ichika","https://www.ac-illust.com/main/profile.php?id=23341701&area=1")+
clink("Textures","PiiiXL","https://piiixl.itch.io/")+
clink("Banner Materials,Lock on cursor<br>","Nanamiyuki's Atelier","https://nanamiyuki.com/")+
clink("Sniper animated","DJMaesen","https://sketchfab.com/3d-models/sniper-animated-eae1ba5b43ae4bc89b0647fb5d8a2d27")+
clink("Parasite Zombie","Mixamo","https://www.mixamo.com/")+
clink("MiniZombie&RedHat","Fkgcluster","https://fkgcluster.itch.io/survivaltowerdefense")+
clink("BloodEffect","XYEzawr","https://xyezawr.itch.io/gif-free-pixel-effects-pack-5-blood-effects")+
clink("Cats","girlypixels","https://girlypixels.itch.io/")+
clink("Terminator-Core","Fred Drabble","https://sketchfab.com/3d-models/fusion-core-f717683d5502496d9e1ef1f1e1d1cb45" )+
clink("Terminator-Robo","Threedee","https://www.threedee.design/cartoon-robot")
            )


addons = """<b>[ INSPIRED BY ADD-ONS ]</b>
Fanfare
Anki Habitica for 2.1
Life Drain
Progress Bar
Progress Bar original
Progress Bar, cards...
Speed Focus Mode
Hitmarkers
HUMBLE PIE

""".replace('\n', '<br>')

budle = ("<b>[ BUNDLE SOURCE CODE ]</b><br>"+
clink ("BGM","Pyglet","https://pyglet.readthedocs.io/en/latest/index.html")+
clink ("webp","dwebp","https://developers.google.com/speed/webp/download")

)

thankYou = ("""
<br><br><br>
<h3>%s</h3><br>""" % ANKI_RESTART +
clink("Created by", "Shigeyuki","https://www.patreon.com/Shigeyuki")+
"""
<br>
Thank you very much!
<br><br>
""")