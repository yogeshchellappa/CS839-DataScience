'''
Pruning rules -
1. remove stopwords
'''
from stop_words import get_stop_words
import pandas as pd

class Prune(object):
    def __init__(self, filename):
        self.pronouns = set(["i", "you", "he", "she", "it", "we", "they", "what","time","staff","menu","waitress","waiter",
                         "who", "me", "him", "her", "it", "us", "you", "them","even", "order", "ordered","I",'im',"Im",
                         "whom", "mine", "yours", "his", "hers", "ours", "theirs", "know", "never","customer","Ive","ive",
                         "this", "that", "these", "those", "who", "whom", "which", "always","love","like","Ill","ill",
                         "what", "whose", "whoever", "whatever", "whichever", "whomever","eat","ate",
                         "myself", "yourself", "himself", "herself", "itself", "ourselves","diet","vegan",
                         "themselves", "each other", "one another", "anything", "everybody", "special",
                         "another", "each", "few", "many", "none", "some", "all", "any","hungry","fast","slow",
                         "anybody", "anyone", "everyone", "everything", "no one", "nobody","service",
                         "nothing", "none", "other", "others", "several", "somebody", "someone",
                         "something", "most", "enough", "little", "more", "both", "either",
                         "neither", "one", "much", "such"])

        self.nonDescWords = set({'think', 'fact', 'good', 'will', 'last', 'The', 'places', 'better', 'just', 'thick',
                                 'area', 'really', 'want', 'best', 'slightly', 'free', 'oh', 'definitely', 'loved',
                                 'watch','We', 'got', 'looking', 'overall', 'experience', 'get', 'fun', 'run', 'inside',
                                 'outside','mall', 'style', 'top', 'instead', 'somehow', 'certainly', 'ten', 'five',
                                 'option','four', 'very', 'very', 'just', 'awesome', 'choices', 'changes', 'strikes', 'shows',
                                 'showed', 'business', 'overly', 'To', 'start', 'stop', 'split', 'We', 'pool', 'fall',
                                 'Dont','bring', 'dont', 'why', 'juicy', 'exact', 'opposite', 'songs', 'saving', 'lung','scare',
                                 'high', 'setup', 'place', 'may', 'let', 'rave', 'cheap', 'end', 'weekends','weekdays', 'weekend',
                                 'weekday', 'take', 'crowd', 'crowded', 'went', 'go', 'husband', 'door', 'wife', 'girlfriend',
                                 'boyfriend', 'gf', 'bf', 'door', 'huge','wait', 'sign', 'seat', 'seated', 'pay', 'meant',
                                 'people', 'coming', 'going','table', 'told', 'took', 'may', 'lacked', 'lack', 'arrive',
                                 'ready','give', 'gave', 'also', 'asked', 'without', 'Its', 'its', 'made', 'warm', 'though','id',
                                 'great', 'though', 'mall', 'goes', 'ok', 'come', 'life', 'lifeless','removed', 'thought', 'huge',
                                 'small', 'wait', 'came', 'back', 'table', 'said','guys', 'put', 'It', 'minute', 'realize',
                                 'three', 'iphone', 'scrabble', 'of','quite', 'quiet', 'ask', 'almost', 'usually', 'go', 'price',
                                 'honestly', 'taste', 'tastes', 'can', 'Oh', 'disagree', 'make', 'group', 'couple',
                                 'recommend', 'recommended', 'decent', 'options', 'good', 'surprised', 'nice',
                                 'average', 'location', 'darn', 'shame', 'is', 'your', 'news', 'found',
                                 'different', 'size', 'given', 'seating', 'worth', 'post', 'airport',
                                 'ritual', 'family', 'restaurant', 'reservation', 'tried', 'sold', 'happy',
                                 'sad', 'lovely', 'big', 'fantastic', 'eaten', 'expectations', 'twice', 'prices'
                                 'neither', 'nor', 'only', 'once', 'time', 'whether', 'either', 'both', 'guys'
                                 'outside', 'taking', 'rounds', 'straight', 'finally', 'done', 'way', 'actually'
                                 'read', 'reviews', 'bit', 'part', 'less', 'solid', 'idea', 'rating',
                                 'ratings', 'idea', 'lot', 'maybe', 'lack', 'lacks', 'things', 'left', 'right',
                                 'visit', 'incredibly', 'unpleasant', 'hit', 'every', 'around', 'alas',
                                 'usual', 'color', 'friends', 'plate', 'making', 'long', 'bad', 'thing',
                                 'pretty', 'try', 'pumped', 'sort', 'my', 'pick', 'brought', 'two', 'sure',
                                 'guy', 'girl', 'every', 'person', 'near', 'see', 'work', 'based', 'likely',
                                 'feels', 'feel', 'flavour', 'assumption', 'skirt', 'duplicate', 'flavour', 'flavor', 'so', 'dying', 'basic', 'large', 'need', 'needs',
                                 'time', 'times', 'lucky', 'managed', 'street', 'summer', 'winter', 'fix',
                                 'keep', 'mind', 'future', 'wish', 'healthy', 'unhealthy', 'since',
                                 'wish', 'ended', 'sharing', 'see', 'say', 'change', 'vegas',
                                 'next', 'would', 'gotten', 'fifth', 'world', 'famous', 'finish', 'paid',
                                 'wandering', 'music', 'provided', 'lost', 'easy', 'totally', 'intimate',
                                 'vibe', 'jazz', 'real', 'rather', 'night', 'day', 'piano', 'singers',
                                 'expensive', 'cheap', 'plan', 'cover', 'charge', 'remember', 'bring',
                                 'credit', 'card', 'excellent', 'especially', 'located', 'ton',
                                 'add', 'adds', 'choice', 'town', 'perform', 'met', 'ladies', 'perfect',
                                 'ambiance', 'date', 'first', 'las', 'vegas', 'extremely', 'diligent',
                                 'dad', 'mom', 'sister', 'brother', 'team', 'favorite', 'score', 'scores',
                                 'football', 'team', 'check', 'checked', 'open', 'see', 'actually', 'shout',
                                 'hear', 'bring', 'bringing', 'look', 'wall', 'walls', 'celeb', 'super',
                                 'consider', 'far', 'still', 'loud', 'telling', 'cheaper', 'No', 'no',
                                 'wanted', 'basically', 'evidence', 'bland', 'wrapped', 'saw', 'lift', 'blow',
                                 'else', 'if', 'main', 'course', 'understand', 'quick', 'Yes', 'moved',
                                 'specific', 'courses', 'prepared', 'Ordered', 'ordered', 'order', 'Order',
                                 'fan', 'metal', 'wall', 'bellagio', 'bill', 'largest', 'homeless', 'tables', 'for', 'negative', 'positive',
                                 'concern', 'furniture', 'dining', 'take', 'out', 'home', 'fake',
                                 'Well', 'well', 'leaned', 'ultimately', 'horrible', 'remotely', 'bite',
                                 'bother', 'although', 'anniversary', 'prices', 'term', 'price', 'terms'
                                 'room', 'multiple', 'flat', 'screens', 'screen', 'smile', 'smiles', 'loft',
                                 'majority', 'lake', 'patio', 'bitch', 'benefit', 'pipe', 'travel', 'less'
                                 'filling', 'tasty', 'Dont', 'dont', 'suits', 'variation', 'lung', 'pearl',
                                 'pearls', 'scare', 'garbage', 'tacked', 'onto', 'but',
                                 'this', 'their', 'delicious', 'if', 'what',
                                 'Only', 'only', 'taste', 'tasty', 'tasted', 'decided', 'so',
                                 'positively', 'One', 'then', 'oil', 'guys' , 'texture', 'did', 'sample',
                                 'sampling', 'delish', 'superb', 'Wowzer', 'smell', 'everywhere',
                                 'part', 'parted', 'suburb', 'suburbs', 'among', 'amongst', 'smother',
                                 'buttery', 'crisp', 'crispy', 'highlight', 'highlighted', 'spicy',
                                 'hint', 'spiciness', 'listening', 'bucks', 'catch', 'relax', 'appointed',
                                 'Four', 'dig', 'dug', 'succulent', 'One', 'one', 'Two', 'two', 'Three',
                                'three', 'same', 'Same', 'host', 'hostess', 'yes', 'no', 'said', 'server', 'servers',
                                 'answer', 'disappointment', 'disppointment', 'streetcar', 'galaxy', 'pricier', 'hype', 'gulten', 'glutenfree', 'items', 'friend',
                                 'friends', 'piece', 'month', 'Yelp', 'hubby', 'website', 'use', 'takeout',
                                 'specials', 'variety', 'fluffy', 'reservations', 'ingredients', 'favourite', 'polite', 'mood'
                                 'portion', 'bed', 'sink', 'bedroom', 'environment', 'seemed', 'walked', 'problem', 'heat', 'television',
                                 'televisions', 'decor', 'room', 'rooms', 'edge', 'outer', 'inner', 'chair', 'chairs', 'hotel',
                                 'hotels', 'word', 'convo', 'monkey', 'flavor', 'guess', 'sum', 'seven', 'apps', 'layer', 'lightbulb',
                                 'smothered', 'mid', 'neighbourhood', 'neighborhood', 'Toronto', 'enjoy', 'enjoyed',
                                 'atmosphere', 'quirky', 'husbands', 'wifes', 'girlfriends', 'boyfriends', 'gfs', 'bfs',
                                 'waiting', 'flavours', 'flavors', 'half', 'find', 'whim', 'craving', 'pub', 'bar', 'bars',
                                 'pubs', 'drive', 'slowest', 'job', 'combo', 'cart', 'push', 'pushing', 'gluten', 'supernova', 'order',
                                 'ordering', 'sheet', 'depth', 'onestop', 'store', 'minutes', 'space', 'seat', 'seats', 'flaky',
                                 'window', 'windows', 'cozy', 'bunch', 'pricey', 'years', 'colour', 'color', 'light', 'toilet',
                                 'elevators', 'elevator', 'rates', 'rate', 'minimum', 'maximum', 'minimums', 'maximums',
                                 'suggestion', 'try', 'trying', 'offer', 'lust', 'info', 'age', 'tip', 'expired', 'view',
                                 'bartender', 'minutes', 'minute', 'chewy', 'generous', 'comfort', 'restroom',
                                 'restrooms', 'spice', 'savory', 'savoury', 'rest', 'realm', 'pile',
                                 'floor', 'celiing', 'blah', 'sense', 'thrilled', 'bins', 'bin',
                                 'mixture', 'risk', 'bottom', 'vibrant', 'mood', 'temp', 'reg', 'amount',
                                 'quantity', 'ambience', 'phenomenal', 'deluxe', 'treat', 'seeing', 'liberty', 'dinein', 'structure',
                                 'refill', 'manager', 'okay', 'courteous', 'corteous', 'yum', 'checks', 'check', 'name', 'chef', 'stars',
                                 'star', 'rage', 'golf', 'mild', 'rush', 'counter', 'toenails', 'cafe', 'call', 'toss',
                                 'ingenuity', 'soak', 'everclear', 'nuclear', 'backup', 'vocals', 'quality', 'follow', 'following',
                                 'alright', 'country', 'selection', 'flack', 'diversity', 'attentive', 'dime',
                                 'comment', 'disappointed', 'giving', 'parents', 'anniversary', 'baby', 'groupon',
                                 'sorts', 'mistakes', 'mistake', 'knocked', 'knock', 'fork', 'spoon', 'plate',
                                 'forks', 'spoons', 'plates', 'favs', 'portions', 'fav', 'portion', 'delivery',
                                 'point', 'reason', 'inspired', 'uninspired', 'visual', 'visually', 'impair', 'impaired',
                                 'notch', 'photo', 'photos', 'highlights', 'deal', 'break', 'breaker', 'couch', 'tv',
                                 'headboard', 'trip', 'size', 'sized', 'locations', 'flavorful', 'play', 'frequency',
                                 'line', 'bathroom', 'system', 'look', 'looks', 'mirage', 'soccer', 'mom', 'moms', 'lard',
                                 'nation', 'zing', 'john', 'wayne', 'floating', 'smiling', 'fifty', 'stiff',
                                 'add', 'added', 'expense', 'greet', 'woman', 'man', 'district', 'balcony', 'midwest',
                                 'conveniently', 'convenient', 'smaller', 'bigger', 'refill', 'refilled',
                                 'issue', 'mediocre', 'goingson', 'portal', 'building', 'roosevelt', 'cardboard', 'watered',
                                 'teeth', 'asu', 'portion', 'portions', 'deal', 'strip', 'face', 'hair', 'broadway',
                                 'equation', 'socks', 'cook', 'cooked', 'undercooked', 'overcooked', 'moving',
                                 'pics', 'attentive', 'excited', 'plaza', 'lights', 'hectic', 'customer', 'customers',
                                 'number', 'toronto', 'case', 'watch', 'watching', 'diner', 'diners', 'sit', 'panelling',
                                 'case', 'origin', 'lot', 'lots', 'presentation', 'stopped', 'client', 'clientele', 'challenge',
                                 'call', 'called', 'firm', 'firmness', 'prompt', 'merchandise', 'come', 'comes', 'lights',
                                 'foot', 'shower', 'painless', 'entrance', 'exit', 'casino', 'self', 'layout',
                                 'hallway', 'shop', 'shops', 'lobby', 'casinos', 'flooded', 'flood', 'apologized',
                                 'urine', 'carpet', 'calories', 'calorie', 'touching', 'touch', 'ability', 'god', 'gods',
                                 'floral', 'note', 'notes', 'dive', 'novice', 'involve', 'involved', 'prompt', 'waiters',
                                 'workers', 'handy', 'serving', 'recliners', 'combination', 'munch', 'mucnhing',
                                 'males', 'females', 'numbers', 'number', 'lick', 'shop', 'quarter', 'quartered', 'rock',
                                 'rocks', 'weakness', 'weak', 'strength', 'shape', 'chefs', 'tvs', 'music', 'musiscians',
                                 'musician', 'palace', 'lounge', 'conceptLots', 'nonbusy', 'busy', 'non', 'section',
                                 'flaw', 'flawed', 'flaws', 'rounded','running', 'errands', 'goto', 'gone', 'establishment',
                                 'limit', 'limited', 'kid', 'scream', 'screaming', 'hanker', 'hankering', 'compliment',
                                 'worst', 'best', 'reviewed', 'tend', 'bartenders', 'phone', 'behold',
                                 'arrive', 'arrived', 'arrives', 'freezer', 'overhaul', 'disregard', 'reflection',
                                 'staffs', 'staff', 'ineffective', 'ineffectiveness', 'glimpse', 'show', 'casual',
                                'game', 'games', 'escalator', 'visit', 'visits', 'annoyance', 'bland', 'blandest', 'sucker',
                                 'sneeze', 'shitty', 'edge', 'edges', 'member', 'appetite', 'rude', 'hunt',
                                 'mechanical', 'protesting', 'kickin', 'kicking', 'drunkenness', 'sociability', 'ratio',
                                 'mass', 'members', 'trend', 'indulge', 'sing', 'singer', 'lead', 'combos', 'combo',
                                 'opinion', 'formula', 'variables', 'variable', 'spotty', 'spot', 'tempe', 'yummyThe',
                                 'musicians', 'accommodate', 'share', 'split', 'melt', 'melts', 'cost', 'sweetness',
                                 'bench', 'etc', 'converse', 'spaces', 'trendy', 'yelp', 'orders', 'platter', 'task',
                                 'hour', 'hours', 'wee', 'tasteless', 'tasty', 'search', 'speed', 'cutter', 'cut',
                                 'vday', 'sport', 'sports', 'test', 'ultimate', 'suzie', 'must', 'granted',
                                 'Frys', 'cooking', 'fee', 'e', 'cook', 'nightclub', 'nosh', 'disappointing', 'guarantee',
                                 'finest', 'varieties', 'hunger', 'trade', 'squares', 'seasoned', 'oven', 'melange', 'version',
                                 'penchant', 'community', 'granted', 'box', 'including', 'mouth', 'watering', 'decadent', 'display',
                                 'polymer', 'model', 'models', 'garnished', 'garnish', 'creamy', 'sigh', 'depend',
                                 'depending', 'depressing', 'depressed', 'prepare', 'preparing', 'delectable', 'deliciosity', 'university',
                                 'nosh', 'rowthe', 'row', 'conceptlots', 'serve', 'served', 'placethe', 'moroco', 'present',
                                 'presented', 'pretentious', 'pretentiously', 'singing', 'eminem', 'buffet', 'center',
                                 'convention', 'dealers', 'value', 'bathtub', 'wicked', 'caribbean', 'kraft', 'frys', 'saturday',
                                 'friday', 'nights', 'yelling', 'kids', 'banned', 'class', 'overkill', 'shriveled', 'mushy',
                                 'accommodating', 'gta', 'freshsqueezed', 'fave', 'spot', 'spots', 'look', 'looked', 'caliber',
                                 'sad', 'sadly', 'peeling', 'good', 'goodness', 'afloat', 'soak', 'soaked', 'thirst', 'mushy', 'dancing',
                                 'monstrosity', 'circle', 'k', 'work', 'works', 'moist', 'greasy', 'meal', 'quicker', 'fountains', 'goods',
                                 'longest', 'coupon', 'personable', 'need', 'needless', 'fancy', 'steal', 'stealing', 'planning',
                                 'chaos', 'include', 'romantic', 'impressed', 'include', 'expecting', 'gets', 'surprise', 'appetizing',
                                 'deals', 'shots', 'meals', 'ingredient', 'make', 'makes', 'lingering', 'gig',
                                 'corporate', 'purchase', 'atomic', 'filling', 'pieces', 'architecture', 'path', 'mexico', 'soggy',
                                 'orderd', 'puzzling', 'clad', 'barfly', 'venezias', 'mound', 'edibility', 'edible',
                                 'toppings', 'topped', 'tabs', 'iceberg', 'kinks', 'book', 'bowl', 'atrias', 'arcadia', 'angelsservice',
                                 'curried', 'refills', 'refill', 'twin', 'th', 'munching', 'mightly', 'large', 'cerratas', 'nutty', 'art'
                                 'killed', 'expected', 'suburbanite', 'pola', 'toasted', 'painting', 'accompanying', 'bits', 'cashier', 'cashiers',
                                 'magic', 'pixie', 'dust', 'odb', 'washrooms', 'washroom', 'cuisine', 'epic', 'pupusas',
                                 'dinners', 'cheesy', 'side', 'bottle', 'bottles', 'rolling', 'freshly', 'valley', 'panasian', 'starter', 'strange',
                                 'stanger', 'damn', 'upon', 'mixed', 'grill', 'platters', 'platter', 'overpowering'})

        self.stopwords = set(['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'any',
                              'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below',
                              'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did',
                              "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each',
                              'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have',
                              "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's",
                              'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll",
                              "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself',
                              "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not',
                              'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours',
                              'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll",
                              "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's",
                              'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's",
                              'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those',
                              'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't",
                              'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's",
                              'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom',
                              'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "youd", "you'll",
                              "you're", "you've", 'your', 'yours', 'yourself', 'yourselves'])

        self.adjectives = set(line.strip() for line in open('adjectives.txt'))
        self.adverbs = set(line.strip() for line in open('adverbs.txt'))
        self.data = pd.read_csv(filename)

    def removeStopwords(self):
        #stopwords = get_stop_words('en')
        #print (stopwords)
        self.stopwords = [i.replace("'","") for i in self.stopwords]
        
        todrop = []
        print(len(self.data))

        for term in self.data['term']:
            parts = term.split(" ")

            flag = False
            for p in parts:
                p = p.lower()
                if p in self.stopwords or p in self.nonDescWords or p in self.adjectives or p in self.adverbs:
                    flag = True
                    break
                else:
                    flag = False

            if flag:
                todrop.append(term)
        self.data = self.data[~self.data.term.isin(todrop)]

        print (len(self.data))
        #data.to_csv('trainingdata_nostopwords.csv')

    def removePronouns(self):
        todrop = []

        for term in self.data['term']:
            parts = term.split(" ")

            flag = False
            for p in parts:
                p = p.lower()
                if p in self.pronouns:
                    flag = True
                    break
                else:
                    flag = False

            if flag:
                todrop.append(term)
        self.data = self.data[~self.data.term.isin(todrop)]
        print(len(self.data))

    def saveData(self):
        self.data.to_csv('trainingdata_nostopwords_nopronouns_2.csv')


