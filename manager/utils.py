import urllib.parse
from user_agents import parse

from django.conf import settings
from django.http import HttpResponseRedirect

from mfo.models import Offer as MFOOffer
from credit.models import Offer as CreditOffer
from manager.models import TeaserClick, TeaserLead


def get_rating(offer):
    rating = 0
    rating_list = []
    for comment in offer.comments.all():
        rating_list.append(comment.rating)
    if rating_list != []:
        rating = "%.2f" % ((sum(rating_list) / len(rating_list)) * 2)
    return float(rating)


def get_count(offer):
    count = len(offer.comments.all())
    return count


def get_choices():
    choices = ()
    for app in settings.APP_LIST:
        inner_tuple = (app, app)
        choices += (inner_tuple, )
    return choices


def get_app_offer(app_name):
    if app_name == 'мфо':
        return MFOOffer
    elif app_name == 'кредитные_карты':
        return CreditOffer


def referrer(self):
    if 'r' in self.request.GET:
        click = TeaserClick()
        click.link = urllib.parse.unquote(self.request.get_full_path())
        click.banner = self.request.GET.get('r')
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        click.ip = ip
        user_agent = parse(self.request.META.get('HTTP_USER_AGENT', ''))
        click.useragent = str(user_agent)
        referer = self.request.META.get('HTTP_REFERER')
        if not referer:
            referer = 'Нет реферера'
        click.referer = referer
        self.request.session['r'] = self.request.GET.get('r')
        if 'r_c' not in self.request.session:
            self.request.session['r_c'] = '1'
        else:
            self.request.session['r_c'] = str(int(self.request.session['r_c']) + 1)
        click.cookie_counter = int(self.request.session['r_c'])
        if 'geo' in self.request.GET:
            geo = self.request.GET.get('geo')
            if geo in regions:
                geo = regions[geo]
            click.geo = geo
        if 'age' in self.request.GET:
            click.age = self.request.GET.get('age')
        if 'gender' in self.request.GET:
            gender = self.request.GET.get('gender')
            if gender == 'f':
                click.gender = 'Женский'
            if gender == 'm':
                click.gender = 'Мужской'
        if 'search' in self.request.GET:
            click.searh = self.request.GET.get('search')
        click.save()


def referrer_count(request, app_name, pk):

    offer = get_app_offer(app_name).objects.get(pk=pk)
    offer.clicked += 1
    offer.save()

    if 'r' in request.GET:
        click = TeaserClick()
        click.link = urllib.parse.unquote(request.get_full_path()) + ' / ' + offer.title
        click.banner = request.GET.get('r')
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        click.ip = ip
        user_agent = parse(request.META.get('HTTP_USER_AGENT', ''))
        click.useragent = str(user_agent)
        referer = request.META.get('HTTP_REFERER')
        if not referer:
            referer = 'Нет реферера'
        click.referer = referer
        request.session['r'] = request.GET.get('r')
        if 'r_c' not in request.session:
            request.session['r_c'] = '1'
        else:
            request.session['r_c'] = str(int(request.session['r_c']) + 1)
        click.cookie_counter = int(request.session['r_c'])
        click.save()

    if 'r_c' in request.session:
        lead = TeaserLead()
        lead.offer = offer.title
        if 'r' in request.session:
            lead.banner = request.session['r']
        else:
            lead.banner = 'Отсутствует'
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        lead.ip = ip
        lead.save()

    return HttpResponseRedirect(offer.link)

regions={'1': 'Чукотский автономный округ', '2': 'Еврейская автономная область', '3': 'Архангельская область', '4': 'Карачаево-Черкесская Республика', '5': 'Астраханская область', '6': 'Республика Калмыкия', '7': 'Алтайский край', '8': 'Белгородская область', '9': 'Чеченская Республика', '10': 'Амурская область', '11': 'Ханты-Мансийский автономный округ', '12': 'Республика Тыва', '13': 'Брянская область', '14': 'Новгородская область', '15': 'Ненецкий автономный округ', '16': 'Узбекистан', '17': 'Таджикистан', '18': 'Приморский край', '19': 'Республика Северная Осетия-Алания', '20': 'Владимирская область', '21': 'Волгоградская область', '22': 'Кировская область', '23': 'Вологодская область', '24': 'Воронежская область', '25': 'Эстония', '26': 'Латвия', '27': 'Литва', '28': 'Казахстан', '29': 'Грузия', '30': 'Объединенные Арабские Эмираты', '31': "'Кот-д''Ивуар'", '32': 'Свердловская область', '33': 'Туркменистан', '34': 'Кыргызстан', '35': 'Финляндия', '36': 'Португалия', '37': 'Польша', '38': 'Ивановская область', '39': 'Удмуртская Республика', '40': 'Иркутская область', '41': 'Республика Марий Эл', '42': 'Республика Татарстан', '43': 'Калининградская область', '44': 'Калужская область', '45': 'Италия', '46': 'Кемеровская область', '47': 'Франция', '48': 'Швеция', '49': 'Швейцария', '50': 'Великобритания', '51': 'Нидерланды', '52': 'Костромская область', '53': 'Краснодарский край', '54': 'Красноярский край', '55': 'Испания', '56': 'Курганская область', '57': 'Курская область', '58': 'Липецкая область', '60': 'Чехия', '61': 'Греция', '62': 'Магаданская область', '63': 'Норвегия', '64': 'Республика Адыгея', '65': 'Дания', '66': 'Республика Дагестан', '67': 'Мексика', '68': 'Республика Корея', '69': 'Саудовская Аравия', '70': 'Московская область', '71': 'Мурманская область', '72': 'Тайвань', '73': 'Гонконг', '74': 'Таиланд', '75': 'Кабардино-Балкарская Республика', '76': 'Турция', '77': 'Япония', '78': 'Коста-Рика', '79': 'Нижегородская область', '80': 'Куба', '81': 'Кипр', '82': 'Доминиканская Республика', '83': 'Эквадор', '84': 'Египет', '85': 'Новосибирская область', '86': 'Эритрея', '88': 'Эфиопия', '89': 'Фиджи', '90': 'Габон', '91': 'Гана', '92': 'Омская область', '93': 'Орловская область', '94': 'Оренбургская область', '95': 'Гибралтар', '96': 'Пензенская область', '97': 'Пермский край', '98': 'Камчатский край', '99': 'Гренландия', '100': 'Псковская область', '101': 'Гвинейская республика', '102': 'Гваделупа', '103': 'Республика Гватемала', '104': 'Ростовская область', '105': 'Рязанская область', '106': 'Самарская область', '107': 'Ленинградская область', '108': 'Республика Мордовия', '109': 'Саратовская область', '110': 'Гвинея-Бисау', '111': 'Гайана', '112': 'Смоленская область', '113': 'Гондурас', '114': 'Ставропольский край', '115': 'Хорватия', '116': 'Гаити', '117': 'Республика Коми', '118': 'Венгрия', '119': 'Индонезия', '120': 'Тамбовская область', '121': 'Ирландия', '122': 'Индия', '123': 'Тверская область', '124': 'Ирак', '125': 'Иран', '126': 'Томская область', '127': 'Тульская область', '128': 'Тюменская область', '129': 'Республика Бурятия', '130': 'Ульяновская область', '131': 'Исландия', '132': 'Ямайка', '133': 'Иордания', '134': 'Республика Башкортостан', '135': 'Хабаровский край', '136': 'Кения', '137': 'Корейская Народно-Демократическая Республика', '138': 'Кувейт', '139': 'Лаос', '140': 'Чувашская Республика', '141': 'Челябинская область', '142': 'Лихтенштейн', '143': 'Шри-Ланка', '144': 'Забайкальский край', '145': 'Сахалинская область', '146': 'Республика Саха (Якутия)', '147': 'Ярославская область', '148': 'Республика Хакасия', '149': 'Либерия', '150': 'Республика Ингушетия', '151': 'Лесото', '152': 'Великое Герцогство Люксембург', '153': 'Ливия', '154': 'Марокко', '155': 'Монако', '156': 'Черногория', '157': 'Мадагаскар', '158': 'Македония', '159': 'Мали', '160': 'Мьянма', '161': 'Монголия', '162': 'Мавритания', '163': 'Мальта', '164': 'Мальдивы', '165': 'Малави', '166': 'Малайзия', '167': 'Мозамбик', '168': 'Намибия', '169': 'Нигер', '170': 'Республика Карелия', '171': 'Нигерия', '172': 'Ямало-Ненецкий автономный округ', '173': 'Никарагуа', '174': 'Непал', '175': 'Новая Зеландия', '176': 'Оман', '177': 'Республика Панама', '178': 'Перу', '179': 'Папуа - Новая Гвинея', '180': 'Филиппины', '181': 'Пакистан', '182': 'Пуэрто-Рико', '183': 'Палестинская автономия', '184': 'Парагвай', '185': 'Катар', '186': 'Румыния', '187': 'Сербия', '188': 'Россия', '189': 'Руанда', '190': 'Сейшельские острова', '191': 'Молдова', '192': 'Судан', '193': 'Республика Сингапур', '194': 'Словения', '195': 'Словакия', '196': 'Украина', '197': 'Сьерра-Леоне', '198': 'Республика Сан-Марино', '199': 'Израиль', '200': 'Соединенные Штаты Америки', '201': 'Беларусь', '202': 'Германия', '203': 'Сенегал', '204': 'Афганистан', '205': 'Сомали', '206': 'Албания', '207': 'Алжирская Народная Демократическая Республика', '208': 'Суринам', '209': 'Андорра', '210': 'Ангола', '211': 'Сальвадор', '212': 'Сирия', '213': 'Того', '214': 'Аргентина', '215': 'Армения', '216': 'Тунисская Республика', '217': 'Австралия', '218': 'Австрия', '219': 'Азербайджан', '220': 'Багамские острова', '221': 'Бахрейн', '222': 'Бангладеш', '223': 'Королевство Тонга', '224': 'Тринидад и Тобаго', '225': 'Бельгия', '226': 'Белиз', '227': 'Бенин', '228': 'Танзания', '229': 'Бутан', '230': 'Боливия', '231': 'Босния и Герцеговина', '232': 'Ботсвана', '233': 'Уганда', '234': 'Бразилия', '235': 'Уругвай', '236': 'Государство-город Ватикан', '237': 'Болгария', '238': 'Буркина-Фасо', '239': 'Венесуэла', '240': 'Камбоджа', '241': 'Камерун', '242': 'Канада', '243': 'Вьетнам', '244': 'Йемен', '245': 'Центрально-Африканская Республика', '246': 'Чад', '247': 'Чили', '248': 'Китай', '249': 'Южно-Африканская Республика', '250': 'Замбия', '251': 'Колумбия', '252': 'Зимбабве', '253': 'Республика Конго', '254': 'Демократическая Республика Конго', '255': 'Острова Кука', '256': 'Симферополь', '257': 'Винницкая область', '258': 'Волынская область', '259': 'Днепропетровская область', '260': 'Донецкая область', '261': 'Житомирская область', '262': 'Закарпатская область', '263': 'Запорожская область', '264': 'Ивано-Франковская область', '265': 'Киевская область', '266': 'Кировоградская область', '267': 'Луганская область', '268': 'Львовская область', '269': 'Николаевская область', '270': 'Одесская область', '271': 'Полтавская область', '272': 'Ровенская область', '273': 'Севастополь', '274': 'Сумская область', '275': 'Тернопольская область', '276': 'Харьковская область', '277': 'Херсонская область', '278': 'Хмельницкая область', '279': 'Черкасская область', '280': 'Черниговская область', '281': 'Черновицкая область', '282': 'Республика Алтай', '285': 'Минская область', '286': 'Брестская область', '287': 'Витебская область', '288': 'Гомельская область', '289': 'Гродненская область', '290': 'Могилёвская область', '291': 'Айдахо', '292': 'Айова', '293': 'Алабама', '294': 'Аляска', '295': 'Аризона', '296': 'Арканзас', '297': 'Вайоминг', '298': 'Вашингтон', '299': 'Вермонт', '300': 'Вирджиния', '301': 'Висконсин', '302': 'Гавайи', '303': 'Делавэр', '304': 'Джорджия', '305': 'Западная Вирджиния', '306': 'Иллинойс', '307': 'Индиана', '308': 'Калифорния', '309': 'Канзас', '310': 'Кентукки', '311': 'Колорадо', '312': 'Коннектикут', '313': 'Луизиана', '314': 'Массачусетс', '315': 'Миннесота', '316': 'Миссисипи', '317': 'Миссури', '318': 'Мичиган', '319': 'Монтана', '320': 'Мэн', '321': 'Мэриленд', '322': 'Небраска', '323': 'Невада', '324': 'Нью-Джерси', '325': 'Нью-Йорк', '326': 'Нью-Мексико', '327': 'Нью-Хэмпшир', '328': 'Огайо', '329': 'Оклахома', '330': 'Орегон', '331': 'Пенсильвания', '332': 'Род-Айленд', '333': 'Северная Дакота', '334': 'Северная Каролина', '335': 'Теннесси', '336': 'Техас', '337': 'Федеральный округ Колумбия', '338': 'Флорида', '339': 'Южная Дакота', '340': 'Южная Каролина', '341': 'Юта', '342': 'Баден-Вюртемберг', '343': 'Бавария', '344': 'Бремен', '345': 'Гамбург', '346': 'Гессен', '347': 'Нижняя Саксония', '348': 'Северный Рейн-Вестфалия', '349': 'Рейнланд-Пфальц', '350': 'Саар', '351': 'Шлезвиг-Гольштейн', '352': 'Бранденбург', '353': 'Мекленбург - Передняя Померания', '354': 'Саксония', '355': 'Саксония-Анхальт', '356': 'Тюрингия', '357': 'Берлин', '362': 'Мангистауская область', '363': 'Актюбинская область', '364': 'Алматы', '365': 'Атырауская область', '366': 'Карагандинская область', '367': 'Костанайская область', '368': 'Кызылординская область', '369': 'Павлодарская область', '370': 'Северо-Казахстанская область', '372': 'Южно-Казахстанская область', '373': 'Жамбылская область', '374': 'Западно-Казахстанская область', '375': 'Восточно-Казахстанская область', '378': 'Астана', '379': 'Акмолинская область', '383': 'Алматинская область', '386': 'Альберта', '387': 'Квебек', '388': 'Британская Колумбия', '389': 'Онтарио', '390': 'Манитоба', '391': 'Нью-Брансуик', '392': 'Саскачеван', '393': 'Новая Шотландия', '394': 'Остров Принца Эдварда', '395': 'Юкон', '396': 'Северо-Западные территории', '397': 'Нунавут', '398': 'Абхазия', '399': 'Сухумский район', '401': 'Маврикий', '402': 'Ливан', '403': 'Бруней', '404': 'Свазиленд', '405': 'Самоа', '406': 'Сент-Винсент и Гренадины', '407': 'Гамбия', '408': 'Кабо-Верде', '409': 'Республика Джибути', '410': 'Вануату', '411': 'Науру', '412': 'Доминика', '413': 'Антарктика', '414': 'Экваториальная Гвинея', '415': 'Восточный Тимор', '416': 'Бурунди', '417': 'Кирибати', '418': 'Коморские острова', '419': 'Сан-Томе и Принсипи', '443': 'Либерецкий край', '444': 'Среднечешский край', '445': 'Устецкий край', '446': 'Краловеградецкий край', '447': 'Высочина', '448': 'Карловарский край', '449': 'Пардубицкий край', '450': 'Пльзенский край', '451': 'Оломоуцкий край', '452': 'Моравскосилезский край', '453': 'Злинский край', '454': 'Южночешский край', '455': 'Южноморавский край', '456': 'Прага', '468': 'Республика Крым', '1755': 'Балви', '1756': 'Вентспилс', '1757': 'Даугавпилс', '1758': 'Краслава', '1759': 'Ливаны', '1760': 'Лиепая', '1761': 'Лудза', '1762': 'Прейли', '1763': 'Резекне', '1764': 'Рига', '1765': 'Цесис', '1766': 'Юрмала', '1775': 'Вильнюс', '1776': 'Друскининкай', '1777': 'Каунас', '1778': 'Клайпеда', '1780': 'Паланга', '1781': 'Тракай', '1782': 'Шяуляй', '2015': 'Анкоридж', '2018': 'Балтимор', '2019': 'Берлингтон', '2020': 'Биллингс', '2021': 'Бирмингем', '2024': 'Вирджиния-Бич', '2028': 'Даллас', '2029': 'Детройт', '2030': 'Джексонвилл', '2035': 'Лас-Вегас', '2038': 'Лос-Анджелес', '2039': 'Луисвилл', '2040': 'Майами', '2041': 'Манчестер', '2042': 'Мемфис', '2043': 'Милуоки', '2044': 'Миннеаполис', '2046': 'Новый Орлеан', '2048': 'Нью-Йорк', '2049': 'Ньюарк', '2058': 'Сан-Франциско', '2059': 'Сан-Хосе', '2061': 'Сент-Луис', '2062': 'Сиэтл', '2065': 'Филадельфия', '2067': 'Хьюстон', '2069': 'Чикаго', '2326': 'Валгамаа', '2328': 'Сааремаа', '2331': 'Нарва', '2334': 'Пярнумаа', '2336': 'Харьюмаа', '2337': 'Тартумаа', '2338': 'Ляэнемаа', '3391': 'Киров', '4791': 'Благовещенск', '4814': 'Сан-Диего', '4895': 'Бриджпорт', '4907': 'Омаха', '4919': 'Шарлотт', '4930': 'Сан-Антонио', '4939': 'Форт-Уэрт', '4942': 'Эль-Пасо', '4952': 'Су-Фолс', '4978': 'Портленд', '4984': 'Иваново', '4993': 'Фарго', '5223': 'Вильяндимаа', '5224': 'Ида-Вирумаа', '5225': 'Ярвамаа', '5227': 'Ляэне-Вирумаа', '5228': 'Рапламаа', '5315': 'Айзкраукле', '5316': 'Алуксне', '5317': 'Бауска', '5318': 'Валка', '5319': 'Валмиера', '5320': 'Гулбене', '5321': 'Добеле', '5322': 'Екабпилс', '5323': 'Елгава', '5324': 'Кулдига', '5325': 'Лимбажи', '5326': 'Мадона', '5327': 'Огре', '5328': 'Салдус', '5329': 'Талси', '5330': 'Тукумс', '5331': 'Алитус', '5332': 'Аникщяй', '5333': 'Биржай', '5335': 'Варена', '5336': 'Вилкавишкис', '5337': 'Висагинас', '5338': 'Зарасай', '5339': 'Игналина', '5340': 'Йонишкис', '5341': 'Казлу-Руда', '5342': 'Калвария', '5343': 'Кедайняй', '5344': 'Кельме', '5345': 'Кретинга', '5346': 'Кайшядорис', '5347': 'Купишкис', '5348': 'Лаздияй', '5349': 'Мажейкяй', '5350': 'Мариямполе', '5351': 'Молетай', '5352': 'Науйойи-Акмяне', '5355': 'Пакруойис', '5356': 'Паневежис', '5357': 'Пасвалис', '5358': 'Плунге', '5359': 'Пренай', '5360': 'Радвилишкис', '5361': 'Расейняй', '5362': 'Ретавас', '5363': 'Рокишкис', '5364': 'Скуодас', '5365': 'Таураге', '5366': 'Тельшай', '5367': 'Утена', '5368': 'Шакяй', '5369': 'Шальчининкай', '5371': 'Шилале', '5372': 'Шилуте', '5373': 'Ширвинтос', '5374': 'Электренай', '5375': 'Юрбакркас', '5505': 'Псков', '5506': 'Москва', '5507': 'Анадырь', '5508': 'Биробиджан', '5509': 'Архангельск', '5510': 'Черкесск', '5511': 'Астрахань', '5512': 'Элиста', '5513': 'Барнаул', '5514': 'Белгород', '5515': 'Грозный', '5516': 'Благовещенск', '5517': 'Ханты-Мансийск', '5518': 'Кызыл', '5519': 'Брянск', '5520': 'Великий Новгород', '5521': 'Нарьян-Мар', '5522': 'Владивосток', '5523': 'Владикавказ', '5524': 'Владимир', '5525': 'Волгоград', '5526': 'Киров', '5527': 'Вологда', '5528': 'Воронеж', '5529': 'Екатеринбург', '5530': 'Иваново', '5531': 'Ижевск', '5532': 'Иркутск', '5533': 'Йошкар-Ола', '5534': 'Казань', '5535': 'Калининград', '5536': 'Калуга', '5537': 'Кемерово', '5538': 'Кострома', '5539': 'Краснодар', '5540': 'Красноярск', '5541': 'Курган', '5542': 'Курск', '5543': 'Липецк', '5544': 'Магадан', '5545': 'Майкоп', '5546': 'Махачкала', '5547': 'Мурманск', '5548': 'Нальчик', '5549': 'Нижний Новгород', '5550': 'Новосибирск', '5551': 'Омск', '5552': 'Орел', '5553': 'Оренбург', '5554': 'Пенза', '5555': 'Пермь', '5556': 'Петропавловск-Камчатский', '5557': 'Ростов-на-Дону', '5558': 'Рязань', '5559': 'Самара', '5560': 'Санкт-Петербург', '5561': 'Саранск', '5562': 'Саратов', '5563': 'Смоленск', '5564': 'Ставрополь', '5565': 'Сыктывкар', '5566': 'Тамбов', '5567': 'Тверь', '5568': 'Томск', '5569': 'Тула', '5570': 'Тюмень', '5571': 'Улан-Удэ', '5572': 'Ульяновск', '5573': 'Уфа', '5574': 'Хабаровск', '5575': 'Чебоксары', '5576': 'Челябинск', '5577': 'Чита', '5578': 'Южно-Сахалинск', '5579': 'Якутск', '5580': 'Ярославль', '5581': 'Абакан', '5582': 'Магас', '5583': 'Петрозаводск', '5584': 'Салехард', '5585': 'Горно-Алтайск', '100001': 'Бывший СССР', '100002': 'Европа', '100003': 'Азия', '100004': 'Африка', '100005': 'Северная Америка', '100006': 'Латинская Америка', '100007': 'Австралия и Океания', '100008': 'Антарктика', '100009': 'Остальной мир'}
