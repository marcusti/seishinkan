#-*- coding: utf-8 -*-

from datetime import date, time
from models import Artikel, Bild, Kategorie, Konfiguration, Termin, Training, Trainingsart, Wochentag
from seishinkan import settings
from seishinkan.news.models import News
import os

class Import():
    def __init__( self ):
        heute = date.today()

        mo = Wochentag( name = 'Montag', index = 0 )
        mo.name_en = 'Monday'
        mo.name_ja = '月'
        mo.save()

        di = Wochentag( name = 'Dienstag', index = 1 )
        di.name_en = 'Tuesday'
        di.name_ja = '火'
        di.save()

        mi = Wochentag( name = 'Mittwoch', index = 2 )
        mi.name_en = 'Wednesday'
        mi.name_ja = '水'
        mi.save()

        do = Wochentag( name = 'Donnerstag', index = 3 )
        do.name_en = 'Thursday'
        do.name_ja = '木'
        do.save()

        fr = Wochentag( name = 'Freitag', index = 4 )
        fr.name_en = 'Friday'
        fr.name_ja = '金'
        fr.save()

        sa = Wochentag( name = 'Samstag', index = 5 )
        sa.name_en = 'Saturday'
        sa.name_ja = '土'
        sa.save()

        so = Wochentag( name = 'Sonntag', index = 6 )
        so.name_en = 'Sunday'
        so.name_ja = '日'
        so.save()

        kat1 = Kategorie()
        kat1.position = 0
        kat1.name = u'Startseite'
        kat1.name_en = u'Home'
        kat1.name_ja = u'ホーム'
        kat1.save()

        kat2 = Kategorie()
        kat2.position = 1
        kat2.name = u'Aikido'
        kat2.name_ja = u'合気道'
        kat2.save()

        kat3 = Kategorie()
        kat3.position = 2
        kat3.name = u'Tendo'
        kat3.name_en = u'Tendo'
        kat3.name_ja = u'天道'
        kat3.save()

        kat4 = Kategorie()
        kat4.position = 3
        kat4.name = u'Seishinkan'
        kat4.name_ja = u'清心館'
        kat4.save()

        kat5 = Kategorie()
        kat5.position = 4
        kat5.name = u'Training'
        kat5.name_ja = u'けいこ'
        kat5.save()

        kat6 = Kategorie()
        kat6.position = 5
        kat6.name = u'Links'
        kat6.name_ja = u'リンク'
        kat6.save()

        kat7 = Kategorie()
        kat7.position = 6
        kat7.name = u'Kontakt'
        kat7.name_en = u'Contact'
        kat7.name_ja = u'コンタクト'
        kat7.public = True
        kat7.save()

        kat8 = Kategorie()
        kat8.position = 0
        kat8.name = u'Anfahrt'
        kat8.public = True
        kat8.parent = kat7
        kat8.save()

        kat9 = Kategorie()
        kat9.position = 0
        kat9.name = u'Anfänger'
        kat9.name_en = u'Beginners'
        kat9.name_ja = u''
        kat9.public = True
        kat9.parent = kat5
        kat9.save()

        kat10 = Kategorie()
        kat10.position = 1
        kat10.name = u'Kinder'
        kat10.name_en = u'Children'
        kat10.name_ja = u''
        kat10.public = True
        kat10.parent = kat5
        kat10.save()

        konf = Konfiguration( name = u'Standard', trainingskategorie = kat5 )
        konf.save()

        artikel = Artikel( kategorie = kat1 )
        artikel.title = u'Tendoryu Aikido – Energie in Bewegung'
        artikel.title_en = u'Tendoryu Aikido – Energy in Motion'
        artikel.title_ja = u'天道流合気道 – 動きの中のエネルギー'
        artikel.text = u'''Aikido ist eine gewaltfreie Budo-Kampfkunst voller Harmonie und Eleganz, welche auf der Philosophie des Miteinander basiert. Das Aikido-Dojo-Seishinkan in Hamburg praktiziert Aikido nach dem Tendoryu-Stil (“Himmelsweg-Schule”). Dieses wurde nach dem Tod des Aikido-Begründers O´Sensei Morihei Ueshiba durch den japanischen Meister Kenji Shimizu geprägt. Meister Shimizu war es auch, der der traditionellen Übungsstätte in Hamburg Eilbek den Namen Seishinkan-Dojo (“Raum des reinen Herzens”) verliehen hat. Der Dojo-Leiter Eckhardt Hemkemeier ist ein direkter Schüler von Meister Shimizu und trägt den 4. Dan.\n\nKommen Sie doch einfach zum Probetraining vorbei und lernen die moderne Budo-Kunst Aikido kennen! Oder besuchen Sie unseren regelmäßig durchgeführten Anfängerkurs. Dieser findet immer Mittwochs und Freitags um 18.30 Uhr statt und umfasst fünf Trainingsabende. Interessenten melden sich bitte bei Eckhardt Hemkemeier oder kommen direkt zum Kurs! Kostenbeitrag für alle fünf Einheiten: 15 € (auch als Geschenkgutschein erhältlich!) Wir bieten auch Workshops für Schulen und Betriebe an. Bitte kontaktieren Sie uns.'''
        artikel.text_en = u'''Aikido is a non-violent budo martial art full of harmony and elegance, which is based on a philosophy of cooperation. The Aikido Dojo Seishinkan in Hamburg is practicing Aikido of the Tendoryu-Style (“School of the Heavenly Way”), which was founded by the japanese master Kenji Shimizu after the death of the founder of Aikido O'Sensei Morihei Ueshiba. It was master Shimizu who gave our traditional dojo in Hamburg-Eilbek the name “Seishinkan-Dojo” (“Room of the Pure Heart”). Head of the dojo Eckhardt Hemkemeier, who holds the 4th Dan grade, is a direct student of master Shimizu.\n\nYou are welcome to visit our training and get to know us and the modern Budo-art Aikido! You can also visit our beginners course which is held every Wednesday and Friday evening from 18:30 to 20:00h. The beginners course takes 5 lessons and costs only 15 € (gift vouchers available!). If you are interested please contact Eckhard Hemkemeier or come directly to the course!'''
        artikel.text_ja = u'''合気道は調和と動作の美しさからなる武道芸術で、力任せなものではありません。ハンブルクの合気道道場清心館では天道流を実践しています。この流派は合気道創始者である植芝盛平先生の死後、清水健二先生により創始されたものです。ハンブルクEilbekの道場に「清心館（清い心の館）」という名を授けて下さったのは清水先生であります。道場で指導を担当するEckhardt　Hemkemeier（エックハート・ヘムケマイヤー）は清水先生の直弟子で現在 4段です。\n\n皆さんも是非お試しに道場に来て武道芸術である合気道と触れてみて下さい。又は定期的に行っている初心者コースに来てみて下さい。当初心者コースは毎水曜・毎金曜（全5回）の18時半から行われております。興味のある方は是非Eckhardt　Hemkemeierのところまでお問い合わせ頂くか、道場に直接来て下さい。コースの参加費用は１５ユーロです。（プレゼントとしてのクーポン券としてもお求め頂けます。）'''
        artikel.save()

        artikel = Artikel( kategorie = kat2 )
        artikel.title = u'Aikido ist Harmonie'
        artikel.title_en = u'Aikido is Harmony'
        artikel.title_ja = u'合気道とはハーモニーです'
        artikel.text = u'''“Aikido ist, den Gegner so zu führen, dass er freiwillig seine feindliche Einstellung aufgibt”, so O´Sensei Morihei Ueshiba, der Begründer dieser modernen japanischen Kampfkunst. Dieses spiegelt sich auch im Begriff des Aikido wider: Aikido ist der Weg (“Do”) zur Harmonisierung (“Ai”) der eigenen Lebensenergie mit der kosmischen Energie (“Ki”). Aikido ist eine noch junge Budo-Kunst, hat jedoch alte Wurzeln: Von Indien und China kamen im 9. Jahrhundert zusammen mit dem Buddhismus hauptsächlich waffenlose Kampfkünste nach Japan. Auch Morihei Ueshiba studierte diese traditionellen Techniken und entwickelte in Jahrzehnten - er lebte von 1883 bis 1969 - aus Altem und Neuem Aikido. Wie in vielen klassischen Budo-Disziplinen wird beim Aikido kein Wettkampf betrieben. Es geht um die persönliche Entwicklung und nicht um das alltägliche “Schneller-Höher-Weiter”. Aikido ist eine ebenso sanfte wie effektive Form der Selbstverteidigung, eine Kampfkunst, die nicht auf Siegen fixiert ist, sondern Vertrauen schafft. Beim Aikido geht es darum, die Angriffsenergie des Gegners dynamisch umzuleiten. Dies geschieht gewaltfrei und benötigt wenig Kraft.'''
        artikel.text_en = u'''As O´Sensei Morihei Ueshiba (1883 – 1969), founder of this modern martial art, said, “Aikido means, leading the opponent in such a way that he (or she) gives up his hostile attidute.” This is also reflected in the word Aikido itself: Aikido is the way (“Do”) of harmonizing (“Ai”) the energy of oneself with the energy of the universe (“Ki”). Although Aikido is a rather modern art, its roots are quite old: During the 9th century Buddhism and mainly weaponless martial arts came from India and China to Japan. Morihei Ueshiba studied these traditional forms. In the course of decades he merged old and new elements to create Aikido Like many of the classic Budo-disciplines, Aikido ist a non-competitive art. Instead it aims at personal developement – not a mentality of rivalty. Aikido is as gentle as well as an effective form of self-defense – a martial art that ist not focussed on winning but in creating harmony and confidence. Aikido is about redirecting the kinetic energy of the opponent's attack. This is done without any violence and needs little strength.'''
        artikel.text_ja = u'''「合気道は相手が敵意ある態度を自発的に放棄するよう相手を導いていくことです。」と日本の現代武道芸術、つまり合気道創始者である植芝盛平先生は語っていました。これは正しく「合気道」という言葉を反映しています：自分のエネルギー「気」と自分を取り巻く環境、延いては宇宙のエネルギー「気」の調和・ハーモニー「合」を目指す「道」。合気道はまだ歴史の浅い武道芸術ではありますが、基となる根は古いものです。9世紀にインド・中国から日本に仏教が伝わって来たとき、武器を使わない武道芸術がいっしょにやって来ました。植芝盛平先生（1883～1969）はこの伝統的なテクニックを学び、それを新しい合気道に発展させたのです。他の武道分野と違って合気道には試合がありません。というのは合気道では個人的な発展が目標なのであって、人よりも速く・高く・遠くと競うものではないからです。合気道はまた護身術でもあり、勝敗にこだわらない武道芸術です。合気道で大事なのは相手の攻撃エネルギーを動的に迂回することです。これは力ずくでなされるのではないので、力持ちである必要はないのです。'''
        artikel.save()

        artikel = Artikel( kategorie = kat3 )
        artikel.title = u'Tendo – Der Himmelsweg'
        artikel.title_en = u'Tendo – The Heavenly Way'
        artikel.title_ja = u'天道 – 天への道'
        artikel.text = u'''Einer der größten Schüler von O´Sensei Morihei Ueshiba ist Kenji Shimizu Sensei. Geboren im Jahre 1940 war Shimizu Sensei von 1962 bis 1967 Uchideshi - ein beim Meister lebender Schüler. Dort lernte er Aikido in seiner fortgeschrittensten Form kennen. Nach dem Tod von O´Sensei Morihei Ueshiba begründete Shimizu Sensei Anfang der siebziger Jahre das Tendoryu Aikido (“Himmelsweg-Schule”) und lehrt dies seither in seiner Aikidoschule - dem Tendokan - in Tokyo. Seit mittlerweile 1978 kommt Meister Shimizu mehrmals im Jahr nach Deutschland und Europa, um hier seinen Stil zu unterrichten, welcher sich durch Harmonie, Eleganz und Effektivität auszeichnet. Auch erhält er häufig von seinen deutschen Schülern in Tokyo Besuch.'''
        artikel.text_en = u'''One of the greatest students of O'Sensei Morihei Ueshiba is Kenji Shimizu Sensei. Born in 1940 Shimizu Sensei was “Uchideshi” – a student living with his master – between 1962 and 1967. During this time he learnt Aikido in its most advanced form. After O'Sensei Morihei Ueshiba's death Shimizu Sensei founded the Tendoryu (“School of the Heavenly Way”) style of Aikido in the early 70s. Since then Kenji Shimizu Sensei is teaching in his own Aikido school – the Tendokan in Tokyo. Since 1978 master Shimizu is visiting Germany and Europe several times a year to teach his style which is characterized by harmony, elegance and efficiency. A lot of his German students return this honour by visiting Shimizu Sensei in Tokyo.'''
        artikel.text_ja = u'''植芝盛平先生の弟子の中でも最も偉大な一人が清水健二先生です。1940年に生まれ1962年から1967年までの間、植芝先生の内弟子でした。植芝先生の死後、清水先生は70年代前半に天道流合気道を創始し、東京の合気道道場「天道館」で以後指導されています。1978年以来、清水先生は年に数回この流派伝授のためにドイツを始めヨーロッパ各地へ来られています。また一方ドイツからの訪問も東京で頻繁に受け入れられています。'''
        artikel.save()

        artikel = Artikel( kategorie = kat4 )
        artikel.title = u'Das Aikido Dojo Seishinkan'
        artikel.title_en = u'The Aikido Dojo Seishinkan'
        artikel.title_ja = u'合気道道場　清心館'
        artikel.text = u'''1986 kam der Begründer des Aikido Dojo Seishinkan, Eckhardt Hemkemeier, nach diversen anderen Kampfkünsten mit dem Aikido in Kontakt und lernte im Jahr 1989 Shimizu Sensei und den Tendo-Stil kennen. Seit dieser Zeit ist er ein direkter Schüler von Shimizu Sensei und begleitet ihn auf fast all dessen Lehrgängen in Europa. Eckhardt Hemkemeier leitet und besucht regelmäßig Lehrgänge in Deutschland, Benelux, Frankreich, Jugoslavien und Mexiko und ist seit 1997 jährlich Gast im Tendokan in Tokyo. Er trägt den 4. Dan. Im Jahr 2000 gründete Eckhardt Hemkemeier das Aikido Dojo Seishinkan und zog im Januar 2003 mit seinen Schülern in die tradionellen Räumlichkeiten in Hamburg-Eilbek. Neben seinem Engagement als Aikido-Lehrer arbeitet er als Orchestermusiker im NDR Sinfonieorchester. '''
        artikel.text_en = u'''After studying other martial arts, Eckhardt Hemkemeier, founder of the Aikido Dojo Seishinkan, had his first encounter with Aikido in 1986. In 1989 he met Shimizu Sensei and thus got to know the Tendo style. Since then Eckhard Hemkemeier is directly taught by Shimizu Sensei whom he is accompanying to most of his European training courses. As well as attending, Hemkemeier is teaching Aikido at courses in Germany, Benelux, France, former Jugoslavia, and Mexico on a regular basis. Since 1997 he is a regular guest in the Tendokan Dojo in Tokyo. In the year 2000 Eckhardt Hemkemeier founded the Aikido Dojo Seishinkan. In January 2003 he and his students moved to the new and now traditional location in Hamburg-Eilbek. Beside his dedication as an Aikido teacher Eckhard Hemkemeier who now holds the 4th Dan grade works as a musician with the NDR (Norddeutscher Rundfunk) Symphonic Orchestra. '''
        artikel.text_ja = u'''合気道道場清心館の設立者、Eckhardt　Hemkemeier（エックハート・ヘムケマイヤー）はいろいろな武道を経験した後、1986年に合気道と出会い1989年に清水先生の天道流派を知るようになりました。そのときから清水先生の直弟子となり、ヨーロッパでの清水先生の稽古にはほとんど付き添っています。Eckhardt　Hemkemeierは定期的にドイツ、ベネルクス、フランス、ユーゴスラヴィア、メキシコでの稽古で指導しています。現在4段で、2000年に合気道道場清心館を設立し、2003年にハンブルクEilbekに道場を移動しました。合気道指導として力を注ぐ一方、北ドイツ放送（NDR）交響楽団員としても活躍しています。 '''
        artikel.save()

        artikel = Artikel( kategorie = kat8 )
        artikel.title = u'Anfahrt'
        artikel.text = u'''<iframe width="425" height="350" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="http://maps.google.de/maps?f=q&amp;hl=de&amp;geocode=&amp;time=&amp;date=&amp;ttype=&amp;q=Aikido+Dojo+Seishinkan,+Wandsbeker+Chaussee+62,+22089+Eilbek,+Hamburg&amp;ie=UTF8&amp;ll=53.57355,10.043306&amp;spn=0.007964,0.017917&amp;z=14&amp;iwloc=A&amp;om=1&amp;cid=53566274,10039140,1568376711813045872&amp;output=embed&amp;s=AARTsJpRoGh87HLU9lz6ZQ2vGX-009v7Nw"></iframe><br /><small><a href="http://maps.google.de/maps?f=q&amp;hl=de&amp;geocode=&amp;time=&amp;date=&amp;ttype=&amp;q=Aikido+Dojo+Seishinkan,+Wandsbeker+Chaussee+62,+22089+Eilbek,+Hamburg&amp;ie=UTF8&amp;ll=53.57355,10.043306&amp;spn=0.007964,0.017917&amp;z=14&amp;iwloc=A&amp;om=1&amp;cid=53566274,10039140,1568376711813045872&amp;source=embed" style="color:#0000FF;text-align:left">Größere Kartenansicht</a></small>'''
        artikel.save()

        artikel = Artikel( kategorie = kat9 )
        artikel.title = u'Aikido für Anfänger'
        artikel.title_en = u'Aikido for Beginners'
        artikel.title_ja = u'初心者のための合気道'
        artikel.text = u'''Anfänger genießen im Aikido Dojo Seishinkan eine besondere Stellung. Das Training am Mittwoch und Freitag (18.30 – 20.00 Uhr) ist speziell auf sie ausgerichtet. Die fortgeschrittenen Schüler stehen ihnen jederzeit gern hilfreich zur Seite, schließlich war jeder einmal ein Anfänger. Später werden es die Anfänger von heute sein, die neuen Anfängern helfen und von ihren Erfahrungen berichten können. Jugend oder körperliche Fitness sind nicht notwendig um Aikido zu üben. Ob jung oder alt, Mann oder Frau, Anfänger oder Fortgeschrittener, beim Aikido trainieren alle gemeinsam und lernen voneinander. Durch Aikidoübungen bekommt der Körper und Geist ganz neues Bewußtsein, manch ein Anfänger staunt, zu welchen Bewegungen er nach einiger Zeit fähig ist. Die harmonischen Bewegungen erzeugen einen ausgeglichenen Geist. Die Muskulatur und das Herz-Kreislaufsystem werden stabilisiert, die Konzentration gefördert. Aikidoka, so der Begriff für die Aikido-Lernenden, gewinnen an Selbstbewusstsein und Vertrauen in sich, den anderen und die Situation. Man lernt, mit Schwierigkeiten geduldig umzugehen und findet neue Möglichkeiten. Ein Anfängerkurs im Dojo Seishinkan geht über fünf Termine. Das Gute daran: Man muss nicht unbedingt an fünf aufeinander folgenden Trainingseinheiten kommen, sondern kann auch mal eine Woche aussetzen. Die Kursgebüren betragen 15 € pro Teilnehmer. Der Anfängerkurs eignet sich auch sehr gut als Geschenk, zum beispiel für Freunde, die schon lange mal etwas für ihre Gesundheit tun wollen. Fragen Sie einfach nach dem Geschenkgutschein!'''
        artikel.text_en = u'''Beginners have a special status in the Aikido Dojo Seishinkan. On Wednesday and Friday evenings (between 18:30 and 20:00 h) we hold a special training for beginners. During this the advanced students are always willing to take special care of beginners, stand by their side and assist them in their first steps. After all, we all were beginners once. Later the beginners of today will be the advanced students who help the new beginners and tell of their experiences. You do not have to be young or physically strong to train Aikido. In Aikido young and old, male and female, beginner and advanced student train together and learn from each other. By way of practicing Aikido, body and mind gain a new level of consciousness. Especially beginners are surprised about what kind of movements they are able to perform after a while. The harmonic movements balance the mind. Aikido stabilizes muscles and the cardiovascular system, and strengthens the ability to concentrate. Aikidoka (people who practice Aikido) gain in self-confidence and trust in themselves, others, and the situation. They learn to deal patiently with difficulties and find new ways to solve conflicts. A beginners course In the Seishinkan Dojo consists of five lessons. The good thing about it: You do not have to attend on five consecutive dates. You can skip a week and continue the next. The fee for the beginner's course is 15 € per person. The beginners course is also a great present – e.g. for friends who always wanted to do something for their health. Just ask for our gift voucher!'''
        artikel.text_ja = u'''合気道道場清心館での練習は毎水曜日・毎金曜日（18時半～20時）は初心者のために特別に設定されています。上級者がいつでも喜んでお助けします。上級者自身も昔は初心者だったのですから。初心者として入ったあなたが、いつかは初心者に自分の学んだことを教えてあげることができるようになるでしょう。合気道を学ぶにあたって若いかどうかなどは関係ありません。老若男女、初心者、上級者、みないっしょに練習します。合気道を学ぶことによって、体・精神に新しい意識をもたらします。調和の取れた動きはバランスの取れた精神状態をつくります。筋肉と循環器系が強化され、集中力もついてきます。合気道家は自意識と自信を得ることが出来ます。難しいことにも忍耐強く取り組んでいく姿勢と、問題解決のための新しい可能性を見出だす力もついてきます。清心館道場での初心者コースは全5回の練習から成っています。5回連続でなくても1週おいて練習に来るのでも構いません。コース参加費は15ユーロです。これはクーポン券としてプレゼントにもなります！例えば、体のために何かやりたいとずっと思っているお友達のためにどうですか。'''
        artikel.save()

        artikel = Artikel( kategorie = kat10 )
        artikel.title = u'Aikido für Kinder'
        artikel.title_en = u'Aikido for Children'
        artikel.title_ja = u'子供のための合気道'
        artikel.text = u'''An zwei Tagen in der Woche (Dienstag und Donnerstag, jeweils von 16.30 – 18.00 Uhr) bieten wir Kindertraining an. Der Schwerpunkt liegt hier nicht auf der Technik, vielmehr lernen die Kinder im Aikido spielerisch, mit ihrem Körper umzugehen. Sie entdecken und schulen neue Fähigkeiten, die sich auch auf ihre Geisteshaltung auswirkt. Äußere und innere Ordnung stärken den Charakter, senken Aggressionen und führen zu mehr Toleranz. Die Konzentrationsfähigkeit wie die körperliche Kondition verbessern sich, auch das Gruppenverhalten wird positiv verstärkt.'''
        artikel.text_en = u'''Two days a week (Tuesday and Thursday from 16:30h to 18:00 h) we offer a special training for children. This training is not focussed on technique but rather on learning in a playful way to gain consciousness in the body. By training Aikido children discover and train new abilities that also affect their mental posture. Outer and inner order strengthen the character, lower aggressiveness, and lead to more tolerance. The ability to concentrate as well as the physical fitness are improved; behaviour within a group is positively enhanced.'''
        artikel.text_ja = u'''週2回火曜・木曜（16時半～18時）は子供向け練習です。重点はここではテクニックを学ぶというより、合気道を遊び感覚で学ぶことです。子供たちも自分の精神状態に作用する新しい能力を見出すでしょう。自分の外と内の「気」が精神を強化し、また攻撃的な気持ちが和らぎ寛容になっていきます。健康にいいだけでなく集中力もつき、また集団の中での振舞いもポジティヴになっていきます。'''
        artikel.save()


        t_alle = Trainingsart( name = u'Training für alle' )
        t_alle.name_en = u'General training'
        t_alle.name_ja = u'全体練習'
        t_alle.save()

        t_frueh = Trainingsart( name = u'Frühtraining' )
        t_frueh.name_en = u'Morning training'
        t_frueh.name_ja = u'早朝練習'
        t_frueh.save()

        t_kinder = Trainingsart( name = u'Kindertraining' )
        t_kinder.name_en = u'Childrens training'
        t_kinder.name_ja = u'子供'
        t_kinder.save()

        t_basis = Trainingsart( name = u'Anfängerkurs' )
        t_basis.name_en = u'Beginners course'
        t_basis.name_ja = u'初心者 '
        t_basis.save()

        t_frei = Trainingsart( name = u'Freies Training' )
        t_frei.name_en = u'Free exercise '
        t_frei.name_ja = u'自由練習'
        t_frei.save()

        t = Training()
        t.wochentag = mo
        t.art = t_alle
        t.von = time( 20, 15 )
        t.bis = time( 21, 30 )
        t.save()

        t = Training()
        t.wochentag = di
        t.art = t_frueh
        t.von = time( 8, 0 )
        t.bis = time( 9, 0 )
        t.save()

        t = Training()
        t.wochentag = di
        t.art = t_kinder
        t.von = time( 16, 30 )
        t.bis = time( 18, 0 )
        t.save()

        t = Training()
        t.wochentag = di
        t.art = t_alle
        t.von = time( 18, 15 )
        t.bis = time( 19, 45 )
        t.save()

        t = Training()
        t.wochentag = mi
        t.art = t_basis
        t.von = time( 18, 30 )
        t.bis = time( 20, 00 )
        t.save()

        t = Training()
        t.wochentag = mi
        t.art = t_alle
        t.von = time( 20, 00 )
        t.bis = time( 21, 30 )
        t.save()

        t = Training()
        t.wochentag = do
        t.art = t_frueh
        t.von = time( 8, 0 )
        t.bis = time( 9, 0 )
        t.save()

        t = Training()
        t.wochentag = do
        t.art = t_kinder
        t.von = time( 16, 30 )
        t.bis = time( 18, 0 )
        t.save()

        t = Training()
        t.wochentag = do
        t.art = t_alle
        t.von = time( 20, 30 )
        t.bis = time( 21, 45 )
        t.save()

        t = Training()
        t.wochentag = fr
        t.art = t_frei
        t.von = time( 18, 00 )
        t.bis = time( 18, 30 )
        t.save()

        t = Training()
        t.wochentag = fr
        t.art = t_basis
        t.von = time( 18, 30 )
        t.bis = time( 20, 00 )
        t.save()

        t = Termin()
        t.title = 'kurzer Termin'
        t.ort = 'Hamburg'
        t.beginn = date( heute.year - 1, heute.month, heute.day )
        t.ende = date( heute.year + 1, heute.month, heute.day )
        t.save()

        t = Termin()
        t.title = 'alter Termin'
        t.ort = 'Berlin'
        t.beginn = date( heute.year - 2, heute.month, heute.day )
        t.ende = date( heute.year - 1, heute.month, heute.day )
        t.save()

        t = Termin()
        t.title = 'Termin heute'
        t.ort = 'Tokio'
        t.beginn = heute
        t.ende = heute
        t.save()

        t = Termin()
        t.title = 'Termin mit einem Namen, der länger als eine Zeile ist'
        t.ort = 'New York'
        t.beginn = date( heute.year + 1, heute.month, heute.day )
        t.ende = date( heute.year + 2, heute.month, heute.day )
        t.save()

        news = News()
        news.title = 'Tendoryu-Aikido im Umbruch'
        news.einleitung = 'oder \n\nLehrer und Schüler – ein immer währender Widerspruch?\n\nErfahrungen aus beiden Positionen'
        news.beginn = date( 2007, 12, 10 )
        news.autor = 'Eckhardt Hemkemeier'
        news.text = '''In der letzten Zeit wird viel übers Tendoryu gesprochen. Es wird von Geldgier, Despotismus, kritikloser Gefolgschaft, Bloßstellung in der Öffentlichkeit und von vielem mehr gesprochen. Es findet eine Stimmungskampagne statt, die vielleicht einer Beleuchtung bedarf.

Einige Lehrer trennen sich von einem Schüler, der nach seinen Vorstellungen nicht das wirkliche Ziel verfolgt. Manch Schüler trennt sich vom Lehrer, weil dieser nicht mehr seinen Vorstellungen entspricht. Das sollte so sein, wenn da nicht manchmal ein Egoismus im Spiel ist. Ist ein Lehrer „idealtypisch“, wird dieser, sobald er nicht mehr dem Ideal entspricht, enttäuschend sein. Er erfüllt also nicht mehr das Maß, welches man an ihn anlegt. Ist es nun am Schüler, den Lehrer zu messen, oder sollte er sich nicht besser bemühen zu verstehen, was der Lehrer ihm vermitteln will? Soll der Lehrer sich den Bedürfnissen der Schüler anpassen, oder soll er seine Sache vermitteln. Und wie er es vermitteln will? Wie vielen Schülern oder welchen Schülern soll er sich anpassen? Wie viele Ideale erfüllen? Ist das nicht absurd?

Muss der andere Mensch, wer auch immer, so sein wie wir es wollen? Eltern und Lehrer spielen da eine besondere Rolle. Wir sollten Abstand nehmen vom Maßnehmen an unsereren Eltern und Lehrer. Sie haben eine besonders schwierige Aufgabe mit großer Verantwortung. Fehler gehören auch zu ihrem Leben, wir sollten sie nicht wiederholen. Eines Tages könnten wir auch Lehrer und Eltern sein und stünden denselben Tatsachen gegenüber. „Uns hört keiner mehr zu. Jeder glaubt, er oder sie wisse besser was sie tun sollen, und wie. Schließlich macht es jeder so!“ Tatsächlich?

Shimizu Sensei ist ein Mensch, der auf große Erfahrung im Leben und im Budo zurück blickt und diese uns weiter vermittelt. Er ist weder ein Idol noch ein Ideal, noch glaube ich, dass er dies sein möchte. Er unterrichtet Tendoryu-Aikido und beschränkt sich nicht nur auf Technik, sondern versucht, wie jeder Lehrer, auch Verständnis für Charakterbildung zu vermitteln. Er ist strikt, direkt und offen.

Deswegen möchte ich eine Weile über meine Erfahrungen sprechen. Ich glaube, wer denkt, ein Lehrer sollte so sein, wie man es selber möchte, braucht keinen Lehrer. Ich beobachte immer wieder, in der letzten Zeit besonders, dass Menschen mehr selbstsüchtig sind, denn auf der Suche nach sich selbst. In den Geschlechterbeziehungen wie auch Freundschaften und in diesem speziell gesehenen Fall der Lehrer-Schülerbeziehung.

Zunächst möchte ich über meine Erfahrung mit meinen Instrumentallehrern berichten. Ich begann im Kindergarten mit der Blockflöte, und die Diakonistin, die den Unterricht leitete, war sehr nett. Dennoch gab es für uns keine große Wahl: Üben und mitmachen dürfen oder nicht üben und nicht mitmachen dürfen.

Meine Eltern arbeiteten schwer dafür, mich anschließend Klavierunterricht nehmen zu lassen und meinen drei Brüdern ebenfalls die Möglichkeit zu erschließen, ein anspruchsvolles Instrument erlernen zu können. Mein Klavierlehrer, der Organist unserer Kirche, kam wöchentlich zu uns, um mich zu unterrichten. Er sah dies nicht als Dienstleistung an, sondern als Möglichkeit für uns, von ihm etwas zu lernen. Hatte ich mich also nicht vorbereitet, sagte er nie etwas meinen Eltern, sondern schimpfte nur mit mir. Er warf mir vor, das Geld meiner Eltern zu verschwenden und riet mir, besser mit dem Unterricht aufzuhören. Das war mir immer äußerst peinlich, und ich begann fleißiger zu sein und aufzuhören mich vor meinen Freunden zu rechtfertigen, dass ich wieder nicht mit ihnen spielen konnte. Mein Klavierlehrer lud mich nun immer zu sich nach Haus zum Unterricht ein, wo ich auf einem neuen Flügel spielen durfte. Das war wohl eine Ausnahme.

Die Faszination Musik überlagerte allmählich alles. Ich lernte autodidaktisch Gitarre, Bassgitarre, Bassflöte. Ich gründete eine Schulband und mit 15 Jahren eine Tanzband.

Dann wechselte ich die Stadt und auf eine musisch ausgerichtete Schule. Mein Bruder war bereits im angeschlossenen Internat und empfahl mir Kontrabass zu lernen, da es genug Pianisten gäbe und die Chance, beruflich erfolgreich zu sein, bedeutend schwieriger sei. Da ich immer bequem und auf anderer Seite neugierig auf ein neues Instrument(da es angeblich leicht zu lernen sei) war, nahm ich Unterricht bei einem Schulkollegen meines Bruders, der auch Gitarre und Bassgitarre in Rock und Pop beeindruckend spielte.

Begeistert nahm ich den Unterricht auf, und mein Lehrer übte jeden Tag 2 Stunden mit mir, ich durfte nicht eher Gitarre spielen oder mit der Band proben, wenn ich nicht vorher Kontrabass geübt hatte. Nach drei Monaten offenbarte er mir, dass ich mich zur Aufnahmeprüfung an der Musikhochschule als Jungstudent anzumelden hätte und er mich am folgenden Tag mit zu seinem Lehrer nehmen würde. Mir rutschte ein wenig das Herz in die Hose, nun sollte ich einen Meister des Basses kennen lernen.

Anfangs war es ein wenig enttäuschend. Wir betraten den schönen aber sehr verqualmten Unterrichtsraum des Professors, welcher mich kurz begrüßte und uns anwies Platz zu nehmen. Ein älterer Student bekam gerade eine Stunde. Ich traute meinen Augen nicht, der Student hatte eine Zigarette im Mund, der Lehrer eine Pfeife. Dieser sang gleichzeitig leidenschaftlich die Stimme des Stücks mit, welches der Student spielte. Dann brach er ab und schimpfte. "Herr Soundso, ich mache ihnen gleich Feuer unter dem Hintern, wenn Sie nicht üben und ein wenig engagierter spielen". Der Student antwortete, dass er das wohl nötig habe, und der Professor zog sein riesiges Gasfeuerzeug hervor, drehte es auf die höchste Stufe und hielt es dem Studenten brennend an den Hintern. Der musste mit seinem Bass einen Satz machen, dennoch war die Cordhose an der Stelle schwarz. Alle lachten, nur ich war schockiert. So vornehm ging das hier wohl doch nicht her.

Darauf hin spielte er uns auf dem Instrument des Studenten das Stück vor. Ich fiel aus allen Wolken, so etwas hatte ich noch nie gehört. Selbst jede Schallplatte konnte mich nicht mehr beeindrucken als diese kleine Livedemonstration. Dann sagte er zu mir, ich solle ein paar Töne spielen, und ich kratzte nervös meine kleine Etude herunter. "Gut", war der Kommentar, "ich nehme Sie". Damit war ich entlassen und durfte gehen. Zwei Wochen später bestand ich in Anwesenheit des Direktors und des Professors die Aufnahmeprüfung. Der Direktor schaute sehr enttäuscht drein und sagte: „ Herr Professor, ich lasse diesen jungen Mann in Ihren Händen und bin sicher, dass er es schafft“. Mein Professor sagte: „Sicherlich“!

Es begann eine Zeit, in der ich vergaß zu schlafen, es gab nur Schule, Bass und Partys. Dann Jazzband und Rockband. Mein Professor gab mir den Spiegel zu lesen, Eugen Herrigels „Zen in der Kunst des Bogenschießens“ und Artikel über Politik und Bildung jeglicher Art. Er schimpfte nur, wenn ich nicht geübt hatte und hätte mich auch einmal fast rausgeworfen. Ich verstand allmählich seine Art zu unterrichten. Strenge, Vertrauen, Hingabe, Selbstbewusstsein und Respekt. Geduld und immer wieder Geduld. Ich hatte keinen eigenen Stundenplan mehr. Wenn er es wollte, hatte ich 3 Stunden nacheinander Unterricht, alle Anderen mussten warten, beziehungsweise waren einige Studenten ein Magnet für die anderen Studenten und ein Muss, deren Unterricht zu folgen. So saßen immer einige Studenten im Unterricht.

Ich musste später andere Vorlesungen schwänzen, weil ich Bassunterricht hatte. Ich „durfte" in den Ferien nicht verreisen, weil mein Professor in meine Wohnung kam, um dort die anwesenden Studenten zu unterrichten. Seine japanische Frau begleitete ihn öfter, und so bekam ich immer mehr Kontakt und Verständnis für seine Art zu unterrichten. Er war Lehrer, Vater, Freund und Erzieher. Zwei der japanischen Studenten sind heute noch meine Freunde. Auch sie verdeutlichten mir eine vollkommen andere Art der Beziehung zu einem Lehrer. Es gab kein Aber beim Lernen, Zuhören oder Spielen. Kritik übten wir nur in einer stillen Studentenrunde. Manchmal fühlten wir uns ungerecht behandelt, benachteiligt aber auch bevorzugt. Es gab auch Neid und Eifersucht. In seiner Gegenwart allerdings trat das alles zurück, wir wollten alles lernen, was er wusste und konnte.

Noch heute betrachte ich ihn als Lehrer, auch als Freund und Ratgeber. Wir duzen uns erst seit 20 Jahren, was aber dem Respekt nicht geschadet hat. Sogar als ich selbst Lehrer an der Hochschule wurde, beobachtete er meinen Unterricht und ich konnte ihn jederzeit um Rat fragen. Als ich Stil und Art ein wenig veränderte, sagte er nur, es sei ihm gleichgültig, solange es Musik bleibe und nicht von der Basis abweiche. Meine Mitstudenten und ich spielen auch nach so langer Zeit noch im Stil unseres Lehrers, verändert auf unseren Körper und Geist, eine natürliche Entwicklung.

Als ich anfing, Aikido zu üben, merkte ich ihm zum ersten Mal richtig an, wie stolz er auf mich war. Kurz zuvor hatte ich eine gute Stelle bekommen, ich war neben ihm Lehrer der Hochschule und begann nun mit Aikido. Seine Frau bemerkte, dass Aikido wie Musik sei, der gleiche Weg. Ich begann in einer Aikikaischule, die ich nach einiger Zeit verließ, da ich den Lehrer als rau und rüde empfand.

Ich wechselte zu einer Schule, die dem Tendoryu ähnlich war, aber auf einer anderen Seite wirkliches Straßenkampfaikido war. Trotzdem ließ mich die Herzlichkeit dieser Leute lange bei ihnen verweilen. Einer der Lehrer sagte mir: „ wenn du wirklich Aikido lernen willst, musst du nach Tokyo zu Shimizu Sensei gehen“. Ich hatte bereits Kontakt zur Hamburger Tendoryugruppe und zu Peter Haase, dessen langjähriger Schüler ich wurde. Dann lernte ich Shimizu Sensei in Tokyo in seinem Dojo besser kennen.

Mir wurde die Parallelen zu meinen vorherigen Lehrern sehr deutlich. Mein Vater, mein Basslehrer, nun Sensei. Bis heute vergleiche ich die Striktheit, die gelegentliche Härte, die Offenheit, Herzlichkeit, Fürsorge und Bereitschaft. Manch ein asiatischer Lehrer sagt, dass ein Europäer asiatische Kultur und Budo doch nicht lernen könne, Shimizu Sensei aber wehrt sich solchen Vorurteilen gegenüber vehement, es liegt am Einzelnen, was er aus den Lehren macht. Viele Lehrer unterrichten nicht wirklich, sie kommen und gehen ohne Verantwortung für die Sache und den Menschen.

All das bestätigte mich mich von meinen Lehrern zu lernen, als Lehrer selbst so zu sein, sich nicht zu verleugnen, anzupassen und zu gefallen, um meine Vorteile zu wahren. Wenn das Aikido manchmal mehr verlangt als ein Freizeitsport-viele Leute haben Familie und einen harten Job-sind die Kosten doch eher gering, außer man fährt jedes Jahr ein bis zwei Mal nach Japan. Die Ansprüche sind eher anderer Natur: äußerste Aufmerksamkeit, Bereitschaft, Benehmen, Wachheit und Achtsamkeit zu jeder Zeit.

Jeder ist frei, sich dafür oder dagegen zu entscheiden. Jemanden aber zu verunglimpfen, zu verleumden und schlechte Dinge nachzusagen, entspricht wirklich nicht der Ehre eines Samurai, auch nicht eines Deutschen, obwohl wir ja damit Geschichte gemacht haben. Wir brauchen nicht unsere Familie zu vernachlässigen oder gar zu töten.

Ein offenes Wort von Angesicht zu Angesicht ist manchmal peinlich, denn in unserer Wellnesswelt brauchen wir doch so etwas nicht mehr. Ich denke aber, lieber manchen peinlichen Moment, als langes stilles Schämen.

Wenn wir ein Problem haben, sollten wir es lösen, dazu gehört eben Mut. Mehr Mut als aus dem Hintergrund zu schießen.

„Nobody is perfect“, dieser Satz wird nur allzu gern auf einen selbst angewendet, Toleranz genießen wir gern, all die Tugenden empfangen wir gern. Wir sollten anfangen sie zu erlernen und zu leben.

Auf ewige Veränderung, unermüdliches Lernen und Verstehen.

Mit lieben Grüßen,
Euer Eckhardt '''
        news.save()

        news = News()
        news.title = 'Bundeslehrgang Herzogenhorn'
        news.einleitung = '24.06. - 30.06.2007'
        news.beginn = date( 2007, 11, 26 )
        news.autor = 'Thomas Koslowski'
        news.text = '''Am Sonntag den 24.06.2007 kam ich zusammen mit Eckhardt und Christian in Herzhogenhorn an. Zur allgemeinen Information, der genannte Ort liegt im tiefsten Schwarzwald, etwa 25 km südlich von Freiburg und 30 km nördlich der Schweiz. Seit über 20 Jahren wird dort vom Tendoryo-Aikiko-Deutschland alljährlich ein Lehrgang mit Shimizu Sensei veranstaltet, zu dem aktive Aikidokas aus ganz Europa kommen. Der gleichnamige Ort liegt etwa 150 Meter tiefer, und ist ein Bundesleistungszentrum der Biatlethen. Die Unterkunft liegt in etwa 1330 m Höhe, entsprechend häufig wechselte es die Woche über zwischen Hochnebel und Dauerregen.

Wir erreichten unser Ziel gegen halb fünf. Das Wetter hatte mitgespielt und so gingen wir mit mehreren Personen auf den Herzogenhorn, den zweithöchsten Berg des Schwarzwaldes. Von dort hatten wir einen Panoramaausblick auf die französischen und schweizerischen Alpen.

Am Sonntag fand kein Training statt, so konnten wir alte und neue Bekannte begrüßen. Der Lehrgangsablauf sah folgendermaßen aus: Von Montag bis Freitag gab es jeweils eine Einheit vormittags von 10:00 bis 11:15 und eine nachmittags von 16:00 bis 17:00 von Montag bis Freitag. Dadurch hat man nach der ersten Einheit mehrere Stunden Zeit um sich anderweitig zu beschäftigen. Nach dem die zweite Einheit abgeschlossen war, erfolgte ab 18:00 das Abendessen, dass in geselliger Runde weiter geführt wurde.

Vor Beginn des Lehrgangs übernahmen die Teilnehmer selbständig die Lockerungs- und Aufwärmübungen, wie dies auch im Tendokan üblich ist. Die Übungen fangen meist mit Shiho-nage, bzw. Nikyo an, so dass man sich darauf konzentriert, die Grundlagenübungen? sauber? und technisch korrekt durchzuführen.

Da das Wetter nicht mitspielte, konnten wir in der unmittelbaren Umgebung nicht viel unternehmen. Eigentlich Schade, denn die Umgebung dort ist sehr reizvoll, mit vielen Wanderwegen, und Treckingmöglichkeiten ohne Ende, auch im Winter ist die Region für die Skifahrer und Snowboarder interessant, davon zeugen die zahlreichen Seilbahnen.

Im Gegensatz zu vorangegangenen Veranstaltungen konnte man diesmal bei einer durchschnittlichen Tagestemperatur von 16 °C konditionell ganz gut überstehen. Zum Abschluss des Lehrgangs wurden durch Shimizu Sensei zahlreiche Graduierungen ausgesprochen, unter anderem für Hamburger Aikidokas, wie: Peter Prehm zum 3. Dan, Klaus Marten 2. Dan, Volker Mros 2. Dan, Martin Rosik, 2. Dan.

Am Samstag nach dem Frühstück haben wir uns verabschiedet, und sind abgereist.'''
        news.save()

        news = News()
        news.title = 'Das Dojo – Ort der zeitlosen Begegnung'
        news.beginn = date( 2006, 4, 14 )
        news.autor = 'Eckhardt Hemkemeier'
        news.text = '''Das Dojo (jap. 道場, dōjō; dt. Ort des Weges), gesprochen Doodschoo, vielmehr die Bedeutung des Dojo, muß man vor dem Hintergrund der asiatischen, shintoistischen und buddhistischen Geschichte Asiens betrachten.

In der Entwicklung des Shintoismus und des Buddhismus suchten die Gläubigen nach Orten, die für ihre Gebete und Übungen geeignet erschienen. Sie schufen in ihren Kultstätten Räume, in denen sie ihre Riten ungestört ausüben konnten. In Europa kennen wir so etwas als Kirchen und Klöster. Auch hier ist der Grund für die Bildung eines solchen Ortes die Suche nach einer Zeit der Ruhe und Unantastbarkeit von der Außenwelt. Eine Zeitlang waren solche Gebäude sogar unantastbar für die weltlichen Herren. Die Autorität des Glaubens an unberührbare Orte war sehr stark. Natürlich stand im Hintergrund die Kirche, eine Sekte oder Ähnliches, aber auch in den Menschen war die Kraft dieses Respekts. Die Aussage: „Vor Gott ist jeder gleich“ war ein Grundsatz in vielen religiösen Vereinigungen. Es sollte vermitteln, dass sich niemand sich auf Geld, Herkunft oder Beziehungen verlassen kann, sondern dass nur seine Taten und sein reiner Geist zählen. Das trifft auch auf das Dojo zu. Im Dojo sind alle gleich, es existieren keine Standesdünkel, weder reich noch arm werden bevorzugt.

Es ist eine heilige Stätte, nicht unbedingt im religiösen Sinn, aber ähnlich einer Kirche oder einem Tempel. An diesen Orten steht die Zeit still, Sorgen bleiben an der Tür zurück, auch die Bedeutung des Standes einer Person bleibt an der Tür zurück. Alles bleibt an der Tür zurück, bis auf das Sein. Ideell betrachtet! Das Ausüben der Kampfkünste an solchen Orten zu Erhebung des menschlichen Seins kam in Japan erst sehr viel später. Aus Indien allerdings, ist so etwas schon lange bekannt. Die Bedeutung eines stillen Ortes, unantastbar für die alltägliche Welt, wurde bald für die Kampfkünstler Asiens sehr wichtig. Hier konnten sie sich zurückziehen, in Ruhe, ohne Beobachtung und ohne Zeitdruck studieren und sich entwickeln.

Natürlich wurden und werden Dojo korrumpiert, Jede Art von Kirche oder Sekte hat dies erlebt. Menschen von außen bestechen, benutzen oder zerstören eine Kirche, einen Tempel oder Dojo. Die „Eigner“ eines Dojo, die Führer einer Kirche oder Sekte, benutzen ihre Position, sie benutzen den Geist des Dojo zur Aufwertung ihres Egos, zur Mehrung ihres Besitzes. Das wissen wir, aber das ist der schlimmste Fall.

Der Leiter, im Budojo der Sensei, bestimmt zwar das Wirken im Dojo, seine Meisterschüler oder älteren Schüler unterstützen ihn dabei, aber er herrscht nicht über die Schüler. Sie sind frei, sie wählen ihn für sich als Lehrer. Ein Lehrer ohne Schüler lehrt nicht, also ist er auch kein Lehrer. Der Lehrer kann einen Schüler ausschließen, wenn er den Geist des Dojo gefährdet sieht, nein, er ist sogar verpflichtet dies zu tun. Tut er es nicht, gefährdet er den Geist und somit die Existenz des Dojo, welches ja so vielen anderen helfen soll. Der Sensei lehrt, er lernt gleichzeitig an seinen Schülern und bereichert sich und seine Schüler mit einem besseren Ego und besseren Fähigkeiten. Der Sinn des Dojo nimmt ihn in diese Pflicht.

Hier betrachten wir einen anderen Aspekt des Dojo: Die Pflicht. Die Pflichten des Dojobesuchers, besser Dojogängers, können sehr verschieden sein. Wenig oder vielfältig. Das spielt keine Rolle, es ist die Anwesenheit von Pflichten, die wichtig ist. Freiheit und Gleichheit existieren nicht ohne Pflichten. Es gilt das Dojo zu erhalten, man muß bezahlen, es instand halten und pflegen, man muß die anderen Dojogänger fürsorglich behandeln und behüten. Selbst wenn man denkt, man muß mehr tun als andere, tut man es. Man beachtet den Sensei wie einen geistigen Führer. Er ist eine respektable Person besonderer Art. Man muß offen sein für die Lehre die einem dort begegnet, für die Fragen die sich einem selbst stellen. Man muß gewillt sein auf sein alltägliches Ego zu verzichten, auf seine Privilegien. Erst dann ist man förderlich für das Dojo, somit für alle. Erst dann kann man lernen und vielleicht sogar diese Erkenntisse mit ins alltägliche Leben nehmen.

Wie ensteht ein Dojo?
Ich denke, ich kann nicht erklären, wie so ein Ort wirklich entsteht, aber vielleicht aus meiner Erfahrung beschreiben. Ich bin katholisch erzogen worden, war bis zum Ausscheiden aus der Kirche auch Ministrant. Ich habe mich viel in der Kirche aufgehalten und diese Athmosphäre stark in mich aufgenommen. Als ich das erste Mal in Japan ein buddhistisches Kloster besucht habe, fühlte ich eine ähnliche Athmosphäre. In diesem Zenkloster war auch ein Dojo für ZaZen (jap. 座禅 / 坐禅 zazen), Zen Meditation im Sitzen). Durch eine Spalte in der Tür konnte ich die Mönche beim Sitzen sehen und fühlte, dass ich hier nur eintreten oder fortgehen kann. Als bloßer Zuschauer hatte ich das Gefühl zu stören, was sehr unhöflich gewesen wäre. Auch als ich einmal durch eine Hecke beim Kyudo (jap. 弓道, kyûdô, japanisches Bogenschießen) zusah, hatte ich ein ähnliches Gefühl. Nicht die Personen selbst weisen einen fort oder ziehen einen an, es war der Ort oder die Tätigkeit, die mich fortwies oder anzog. Das hieß für mich: Störe nicht den Raum dieser Menschen, bedränge sie nicht durch deine Anwesenheit. Geh im selben Geist mit ihnen oder geh. Als ich im vergangenen Dezember im Tendokan war erlebte ich dies so: Auf Grund einer Knieoperation konnte ich nicht am Training teilnehmen. Sensei bedeutete mir mich statt dessen auf einen kleinen Hocker zu setzen. Ich fühlte mich diese Stunde sehr unwohl. Beim nächsten Training saß ich im Dogi und Hakama am Rand der Matte und fühlte mich sehr wohl, mehr noch als Takahashi San mich bat, ihn einige Male zu werfen, damit ich doch ein wenig vom Training hätte.

Durch meine Reisen habe ich viele Orte dieser Art kennengelernt, ob Kirchen, Klöster, Tempel oder Schreine. Ich werde mich hier aber auf ein Budojo beziehen. Das erste Dojo, welches ich betrat, war wohl eher ein Sportraum. Das Gefühl war, obwohl dort Aikido und Karate praktiziert wurde, kein „Dojogefühl". Auch andere Dojo in Hamburg vermittelten mir nicht das gleiche Gefühl wie das Zendojo in Japan. Als ich Peter und Olaf aus Lüneburg ein wenig half, etwas in ihrem neuen Dojo einzurichten, und als die ersten Trainingseinheiten stattfanden, bekam ich das erste „deutsche“ Dojogefühl. Eine „freie“ Ernsthaftigkeit, eine Präsenz des Budogedanken war zu spüren. Shimizu Sensei sagte einmal: „Jede Begebenheit, die in einem Dojo stattfindet, trägt zum Geist des Dojo bei. Alles Gute und Schlechte, jeder Gedanke wird Teil des Dojo.“ Deswegen habe er Abstand davon genommen, andere Gruppen in seinem Dojo trainieren zu lassen.

Vor einigen Jahren haben wir, eine Gruppe Aikidotrainierender, den Entschluss gefasst, ein „eigenes“ Dojo zu errichten. Eigenes habe ich in Anführungsstriche gesetzt, weil man ein Dojo nicht besitzen kann. Man kann den Raum besitzen, aber nicht den geistigen Inhalt. Ich kann sagen, dass die meisten von denen, die daran beteiligt waren, den Geist des Dojo erzeugt zu haben und damit auch die Bedeutung eines Dojo erkannt haben. Sie haben nicht nur darin gearbeitet, es gebaut, sondern anschließend auch trainiert, die ersten Reparaturen durchgeführt und neue Mitglieder eingeführt. Sensei und sein Sohn Kenta sagten bei ihrem ersten Besuch des Dojo diese Qualität sofort zu: „Richtiger und guter Geist“! Viele andere Lehrer gaben ähnliche Äußerungen von sich. Massimo Abate (Karatelehrer), Pascal Olivier, Walter Krinner, Birgit Lauenstein, Christian Haller (Tendoryu-Aikidolehrer).

Der Sinn des Dojo
Der Sinn ist, das Ego von allen Vorstellungen und Lasten zu befreien, um es für eine neue Entwicklung zu befähigen. Wie ein altes buddhistisches Sprichwort sagt: „Ein volles Glas kann man nicht füllen". Das Betreten eines Dojo bedeutet sich zu befreien, für eine kurze Zeit frei zu sein. Natürlich frei zu sein, nicht um zu machen was man will.

Lehren wie die Kampfkünste, ZaZen oder andere Zenmethoden, benötigen nicht unbedingt einen Raum, es könnte auch ein Platz oder Halle sein, aber es ist ungleich schwieriger an anderen Orten diese Stimmung zu erzeugen. Ich las einmal über einen Karateschüler in Japan, dass sein Dojo ein Hof einer Schule war. Vor jedem Training fegten die Schüler den Platz, nahmen in einer Reihe vor dem Sensei Platz. So kann auch ein Dojo entstehen. In unserem Fall, dem Aikido Dojo Seishinkan, wollten wir einen Raum, der uns Platz zum Training gibt, aber auch zur Begegnung dienen kann, für weitere Kurse, die das Training fördern.

Ich sehe die Veränderung unseres Dojo und seiner Besucher. Manch einer verändert sich bald. er oder sie reflektieren ihre Umgebung, ihre Arbeit, ihr Benehmen und Aikido, und verändern es zum Besseren. Manch einer scheint für ein Dojoleben geboren, ein anderer tut sich schwer, aber jeder macht eine Entwicklung durch. Durch eigene Reflektion, durch die der Partner im Dojo oder des Lehrers. Einige geben auf, sie wollen nicht ihr Ego preisgeben oder fühlen sich fehl am Platz. Aber immer denke ich, ein wenig nehmen sie mit, auch wenn sie es nicht wollen. Andere kehren nach Jahren zurück und fühlen das Bedürfnis nach Veränderung, oder sie suchen Halt nach einem schlimmen Erlebnis. Das Dojo, in diesem Fall alles was dort ist, kann einem Kraft geben, mehr noch, die eigene Kraft wiederzuentdecken, das Ki wieder zum Fließen zu bringen. Das spürt jeder, der eine Zeitlang in einem Dojo war.

Stärke, Toleranz, Flexibilität, Vertrauen, Kraft, Ausdauer, Selbstsicherheit, viele Ausdrücke für eine Sache, für das fließendes Ki. Darum denke ich, dass ein Dojo nötig ist für die Menschen, es ist nötig um Aikido zu üben, es ist nie Selbstzweck. Ein schön dekorierter Raum, edel ausgestattet, kann dieselbe spirituelle Aussage wie ein U-Bahntunnel haben. Auch das fühlt man.

Letztlich kann man das alles in die esoterische Ecke schieben, realistisch betrachtet sind solche Dinge nicht beweisbar, wissenschaftlich gesehen alles Placebo, spiritistischer Unfug... Aber Aikido lehrt einen, sich selbst besser kennenzulernen. Der Eine in mir weiß mittlerweise sehr genau was gut für ihn ist.

Zum Beispiel ins Dojo zu gehen und zu trainieren.'''
        news.save()

        news = News()
        news.title = 'Schnee, Eis und Schweiß – Shimizu Sensei in Oberhaching und Deggendorf'
        news.einleitung = 'Aikido im Jahrhundertwinter, 6. – 12.03.2006'
        news.beginn = date( 2006, 3, 15 )
        news.autor = 'Gaëlle und Eckhardt Hemkemeier'
        news.text = '''Gaëlle und ich wollten eigentlich mit dem Auto am Montag nach Oberhaching, Nähe München fahren. Aber am Sonntag, Senseis Abreise von Berlin nach München, wurde vor Eis und Schnee, Staus und großen Problemen gewarnt. Also buchten wir in letzer Sekunde einen Flug für Dienstag in der Früh, um pünktlich zum Training in der Sportschule Oberhaching zu sein.

Um 5.30 Uhr waren wir am Flughafen und warteten dann doch eine halbe Stunde länger als geplant. Auch die S-Bahn in München fuhr ein wenig langsamer als gewohnt. Überall waren Schnee- und Eisberge zu sehen, festgefahrene Schneedecken, meterhoch eingeschneite Autos. Eine weiße Traumlandschaft zog an uns vorbei, für die Bayern nun wohl eher eine Alptraumlandschaft.

Etwas zu spät waren wir dann doch, aber Sensei nahm es uns nicht übel, tags zuvor hatte er selbst 2 Stunden auf seinen Flieger warten dürfen. Der Lehrgang, organisiert von Matze aus Bad Kitzingen, unterstützt von engagierten Gröbenzellern, hatte schon am Nachmittag zuvor begonnen und die 100 Aikidoka waren schon gut eingestimmt. Sensei war voll des Lobes über die Lehrgänge in Genk und Berlin zuvor und erwartete dies auch hier. Die Teilnehmer enttäuschten ihn nicht. Seine Einstellung zum Budo und unermüdliche Inspiration sprang wie so oft auf uns über.

Trotz der unglaublich schlechten Klimaanlage(die Erbauer sollten mal nach Japan fahren), der weich und hart gemischten Matten, ließen sich die Teilnehmer die Freude nicht nehmen. Aber 1 1/4 Stunden morgens und 2 Stunden nachmittags, verlangten ihren Tribut. Husten und Atemnot erklang überall, einige Mägen konnten sich wohl auch nicht mit der Großküchenkost anfreuden.

Immer wieder unterbrach Sensei das Training, um von seinen Erfahrungen im Judo, dann im Aikido mit O'Sensei zu berichten. Immer wieder ermahnte er uns, und damit auch auch sich selbst, wie er betonte, nicht den Budogeist zu vergessen, den Kampf mit sich selbst zu führen, nicht aufzugeben wenn es hart wird und zu wachsen an der Konzentration und Anstrengung.

Stock- und Schwertraining, auch eine Stunde mit dem Messer, brachten eine interessante Abwechslung. Immer wieder wies Sensei uns darauf hin, dass wir kein Yaido, Kendo oder ähnliches machen, sonder Aikiken, Aikijo.

Von Zeit zu Zeit führte er dann auch das Ukemi vor, welches immer wieder faszinierend ist. Ich selbst hatte das Vergnügen Sensei mit einem Kokyunage werfen zu dürfen. Solch einen Uke wünscht man sich für alle Tage. Unglaublich gleichmäßig und Timing folgte er meiner Technik.

Das wurde für mich das Motto der restlichen Aikidotage dieser Lehrgänge.

Am Ende des Lehrgangs war Sensei voll des Lobes über die Teilnehmer, sie haben nicht aufgegeben und sind gewachsen an der Herausforderung. Auch war wieder überrascht über die Leidenschaft und die Verbesserung des Aikido der gemischten Gruppe aus ganz Deutschland.

Am Sonnabend mußten wir dann leider unseren gasfreundlichen Freunde Carolina und Bert verlassen und es ging mit der lustigen Jugengruppe von Großhadern, die uns freundlicherweise aufnahm, mit dem Zug nach Deggendorf. Das kurzfristige Tief und damit Schmelzwasser, hatte schon viele Flüsse über die Ufer treten lassen und so sahen wir bei der Ankunft in Deggendorf die Donau schon in einigen Vorgärten. Aber es wurde schon wieder kälter und schneite auch auch schon wieder. Fast wäre auch der Lehrgang abgesagt worden, da hier die Hallen alle mit meterdicken Schneedecken bedeckt waren. Robert Hundshammer, Aikidourgestein und humorvoller Organisator des zum 30jährigen Bestehens des Aikido in Deggendorf Festslehrgang, begrüßte Teilnehmer und Sensei mit freundlichen Worten.

Am nächsten Morgen begrüßte uns auch die Oberbürgemeisterin von Deggendorf mit salbungsvoller Stimme, und wir erfuhren was wir im Aikido eigentlich machen, und wie schön das doch ist. Da war für Robert der richtige Zeitpunkt gekommen. wie er es vertanden hätte, sei zum Beispiel die Halle für die Aikidoka immer offen, was dann die geehrte Frau Bürgermeisterin nicht bestreiten wollte, sondern auch noch bekräftigte. Begeistert ablaudierten ihr die Teilnehmer und auch Sensei war voll des Lobes für solch ein Engagement und Verständis des Aikido.

Zum Schluß gab es auch großen Ablaus für Sensei und Birgit, die wieder einmal 3 Wochen an Senseis Seite dolmetschte und Ukemi für ihn machte.

Gaëlle und ich bedanken uns auf diesem Wege auch noch einmal bei Stefan, der uns so komfortabel aufnahm, bei den fleißigen Organisatoren und den Teilnehmern der beiden Lehrgänge, für die schönen Techniken und Ukemi, die schönen Gespäche und die lustigen Abende.

Auf ein baldiges Wiedersehen'''
        news.save()

        for filename in os.listdir( os.path.join( settings.MEDIA_ROOT, 'bilder' ) ):
            if filename.lower().endswith( 'jpg' ):
                bild = Bild()
                bild.name, ext = os.path.splitext( filename )
                bild.bild = os.path.join( 'bilder', filename )
                bild.save()

