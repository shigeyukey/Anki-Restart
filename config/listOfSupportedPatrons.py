
ANKI_RESTART = "Anki Restart"

from ..shige_pop.patreons_list import PATRONS_LIST

re_patreons_list = PATRONS_LIST.replace(",", "<br>")

def clink(name, text,url=None):
    if not url:
        return f'{name} : {text}<br>'
    return f'{name} : <a href="{url}">{text}</a><br>'

credits = """
<br><br><br>
<b>[ CREDIT ]</b>
<br><br><br>
""".replace('\n', '<br>')

patreon = f"""
Special Thanks
<b>[ PATRONS ]</b>
{re_patreons_list}



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